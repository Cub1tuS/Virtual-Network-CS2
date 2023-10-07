# III. Serveur DNS

- [III. Serveur DNS](#iii-serveur-dns)
  - [1. Install](#1-install)
  - [2. Config](#2-config)
  - [3. Firewall](#3-firewall)
  - [4. Test](#4-test)
  - [5. DHCP my old friend](#5-dhcp-my-old-friend)

## 1. Install

> **L'install et la config sont à réaliser sur la machine `dnsnet2`.**
>
> **J'ajoute au préalable une route par défaut vers `router2` pour permettre à ma machine de rejoindre internet mais aussi un un serveur DNS dans sa conf réseau.**

```bash
[dorian@dnsnet2 ~]$ sudo ip route add default via 10.3.2.254 dev enp0s3

[dorian@dnsnet2 ~]$ ip r s
default via 10.3.2.254 dev enp0s3 
10.3.2.0/24 dev enp0s3 proto kernel scope link src 10.3.2.102 metric 102 
192.168.56.0/24 dev enp0s8 proto kernel scope link src 192.168.56.10 metric 101 
```

```bash
[dorian@dnsnet2 ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s3

NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.3.2.102
NETMASK=255.255.255.0

DNS1=1.1.1.1
```

```bash
[dorian@dnsnet2 ~]$ ping google.com
PING google.com (142.250.75.238) 56(84) bytes of data.
64 bytes from par10s41-in-f14.1e100.net (142.250.75.238): icmp_seq=1 ttl=117 time=13.3 ms
64 bytes from par10s41-in-f14.1e100.net (142.250.75.238): icmp_seq=2 ttl=117 time=50.1 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 13.300/31.699/50.099/18.399 ms
```

```bash
sudo dnf install -y bind bind-utils
```

## 2. Config

La configuration du serveur DNS va se faire dans 3 fichiers essentiellement :

- **un fichier de configuration principal**
  - `/etc/named.conf`
  - on définit les trucs généraux, comme les adresses IP et le port où le serveur DNS sera disponible
  - on définit aussi un chemin vers les autres fichiers, les fichiers de zone
- **un fichier de zone**
  - `/var/named/net1.tp3.db`
  - je vous préviens, la syntaxe fait mal
  - on peut y définir des correspondances `nom ---> IP`
- **un fichier de zone inverse**
  - `/var/named/net1.tp3.rev`
  - on peut y définir des correspondances `IP ---> nom`

➜ **Allooooons-y, fichier de conf principal**

```bash
[dorian@dnsnet2 ~]$ sudo cat /etc/named.conf

options {
    listen-on port 53 { 127.0.0.1; };
    listen-on-v6 port 53 { ::1; };
	directory 	"/var/named";
	dump-file 	"/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	memstatistics-file "/var/named/data/named_mem_stats.txt";
	secroots-file	"/var/named/data/named.secroots";
	recursing-file	"/var/named/data/named.recursing";
	allow-query     { localhost; };
        allow-query-cache { localhost; any; };

	recursion yes;

	dnssec-validation yes;

	managed-keys-directory "/var/named/dynamic";
	geoip-directory "/usr/share/GeoIP";

	pid-file "/run/named/named.pid";
	session-keyfile "/run/named/session.key";

	/* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
	include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "net2" IN {
     type master;
     file "net2.db";
     allow-update { none; };
     allow-query {any; };
};

zone "2.3.10.in-addr.arpa" IN {
     type master;
     file "net2.rev";
     allow-update { none; };
     allow-query { any; };
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

➜ **Et pour les fichiers de zone**

```bash

[dorian@dnsnet2 ~]$ sudo cat /var/named/net2.db
$TTL 86400
@ IN SOA dnsnet2. adminnet2. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dnsnet2.

; Enregistrements DNS pour faire correspondre des noms à des IPs
dns        IN A 10.3.2.102
web        IN A 10.3.2.101
```

```bash

[dorian@dnsnet2 ~]$ sudo cat /var/named/net2.rev
$TTL 86400
@ IN SOA dnsnet2. adminnet2. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dnsnet2.

;Reverse lookup for Name Server
102   IN PTR dnsnet2.
101   IN PTR webnet2.
```

➜ **Une fois ces 3 fichiers en place, démarrez le service DNS**

```bash
[dorian@dnsnet2 ~]$ sudo systemctl start named

[dorian@dnsnet2 ~]$ sudo systemctl enable named
Created symlink /etc/systemd/system/multi-user.target.wants/named.service → /usr/lib/systemd/system/named.service.

[dorian@dnsnet2 ~]$ sudo systemctl status named
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; preset: disabled)
     Active: active (running) since Sat 2023-10-07 18:49:36 CEST; 5min ago
   Main PID: 12418 (named)
      Tasks: 5 (limit: 4611)
     Memory: 19.4M
        CPU: 38ms
     CGroup: /system.slice/named.service
             └─12418 /usr/sbin/named -u named -c /etc/named.conf
```

## 3. Firewall

🌞 **Ouvrir le port nécessaire dans le firewall**

```bash
[dorian@dnsnet2 ~]$ sudo firewall-cmd --add-port=53/udp --permanent
success
```

```bash
[dorian@dnsnet2 ~]$ sudo firewall-cmd --reload
success
```

```bash
[dorian@dnsnet2 ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3 enp0s8
  sources: 
  services: cockpit dhcpv6-client ssh
  ports: 53/udp
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```

## 4. Test

Depuis une machine cliente du réseau, utilisez la commande `dig` pour faire des requêtes DNS à la main.

La commande `dig` sert à effectuer des requêtes DNS à la main depuis une machine Linux (on l'a obtenu en téléchargeant le paquet `bind-utils` quand on a install Rocky ensemble). Elle s'utilise comme suit :

```bash
# faire une requête DNS en utilisant le serveur DNS connu par l'OS
$ dig efrei.fr

# faire une requête DNS en précisant à quel serveur DNS on pose la question
$ dig efrei.fr @1.1.1.1

# faire une requête DNS inverse (trouver le nom qui correspond à une IP)
$ dig -x 10.3.2.101
```

🌞 **Depuis l'une des machines clientes du réseau 1** (par exemple `node1.net1.tp3`)

- utiliser `dig` pour trouver à quelle IP correspond le nom `web.net2.tp3`
- utiliser `curl` pour visiter le site web sur `web.net2.tp3` en utilisant son nom
  - assurez-vous de purger votre fichier `hosts` de vos éventuelles précédentes modifications

## 5. DHCP my old friend

🌞 **Editez la configuration du serveur DHCP sur `dhcp.net1.tp3`**

- l'adresse du serveur DNS qui est donnée au client doit désormais être celle de `dns.net2.tp3` (il faut bien préciser une IP, pas le nom)
- prouvez que ça fonctionne avec un `dig` depuis un client qui a fraîchement récupéré une IP
