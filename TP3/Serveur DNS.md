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

> J'ai eu des problèmes au niveau de la configuration du serveur dû aux noms de mes machines, j'ai donc préférer les renommer exactement comme dans le TP.

```bash
[dorian@dns ~]$ sudo cat /etc/named.conf
[sudo] password for dorian: 
options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
	dump-file	"/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	memstatistics-file "/var/named/data/named_mem_stats.txt";
	secroots-file	"/var/named/data/named.secroots";
	recursing-file	"/var/named/data/named.recursing";
        
	allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };

        recursion yes;

	dnssec-validation yes;

	managed-keys-directory "/var/named/dynamic";
	geoip-directory "/usr/share/GeoIP";

	pid-file "/run/named/named.pid";
	session-keyfile "/run/named/session.key";

	include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "net2.tp3" IN {
	type master;
	file "net2.tp3.db";
	allow-update { none; };
	allow-query {any; };
};

zone "2.3.10.in-addr.arpa" IN {
     type master;
     file "net2.tp3.rev";
     allow-update { none; };
     allow-query { any; };
};
```

➜ **Et pour les fichiers de zone**

```bash
[dorian@dns ~]$ sudo cat /var/named/net2.tp3.db
$TTL 86400
@ IN SOA dns.net2.tp3. admin.net2.tp3. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns.net2.tp3.

; Enregistrements DNS pour faire correspondre des noms à des IPs
dns        IN A 10.3.2.102
web        IN A 10.3.2.101
```

```bash
[dorian@dns ~]$ sudo cat /var/named/net2.tp3.rev
$TTL 86400
@ IN SOA dns.net2.tp3. admin.net2.tp3. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns.net2.tp3.

;Reverse lookup for Name Server
102   IN PTR dns.net2.tp3.
101   IN PTR web.net2.tp3.
```

➜ **Une fois ces 3 fichiers en place, démarrez le service DNS**

```bash
[dorian@dns ~]$ sudo systemctl start named

[dorian@dns ~]$ sudo systemctl enable named
Created symlink /etc/systemd/system/multi-user.target.wants/named.service → /usr/lib/systemd/system/named.service.

[dorian@dns ~]$ sudo systemctl status named
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
[dorian@dns ~]$ sudo firewall-cmd --add-port=53/udp --permanent
success
```

```bash
[dorian@dns ~]$ sudo firewall-cmd --reload
success
```

```bash
[dorian@dns ~]$ sudo firewall-cmd --list-all
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

🌞 **Depuis l'une des machines clientes du réseau 1** (par exemple `node1.net1.tp3`)

```bash
[dorian@node1 ~]$ dig web.net2.tp3 @10.3.2.102

; <<>> DiG 9.16.23-RH <<>> web.net2.tp3 @10.3.2.102
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 27675
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 8cc46a6c44559fcd010000006522f2b99e5bbf2169ff777f (good)
;; QUESTION SECTION:
;web.net2.tp3.			IN	A

;; ANSWER SECTION:
web.net2.tp3.		86400	IN	A	10.3.2.101

;; Query time: 2 msec
;; SERVER: 10.3.2.102#53(10.3.2.102)
;; WHEN: Sun Oct 08 20:19:37 CEST 2023
;; MSG SIZE  rcvd: 85
```

```bash
[dorian@node1 ~]$ curl web.net2.tp3
coucou EFREI
```

```bash
[dorian@node1 ~]$ cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
```

## 5. DHCP my old friend

🌞 **Editez la configuration du serveur DHCP sur `dhcp.net1.tp3`**

```bash
[dorian@dhcp ~]$ sudo cat /etc/dhcp/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#

default-lease-time 3600;
max-lease-time 86400;
authoritative;

subnet 10.3.1.0 netmask 255.255.255.0 {
range 10.3.1.50 10.3.1.99;
option subnet-mask 255.255.255.0;
option routers 10.3.1.254;
option domain-name-servers 10.3.2.102;
}
```

```bash
[dorian@node1 ~]$ nmcli dev show | grep 'IP4.DNS'
IP4.DNS[1]:                             10.3.2.102
```

```bash
[dorian@node1 ~]$ dig web.net2.tp3

; <<>> DiG 9.16.23-RH <<>> web.net2.tp3
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 38967
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 86415b795fb36eae010000006522f5ac049e9a8b87b6d3bd (good)
;; QUESTION SECTION:
;web.net2.tp3.			IN	A

;; ANSWER SECTION:
web.net2.tp3.		86400	IN	A	10.3.2.101

;; Query time: 1 msec
;; SERVER: 10.3.2.102#53(10.3.2.102)
;; WHEN: Sun Oct 08 20:32:13 CEST 2023
;; MSG SIZE  rcvd: 85
```
