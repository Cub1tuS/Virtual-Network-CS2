# I. DHCP

🌞 **Setup de la machine `dhcp.net1.tp3`**

```bash
[dorian@dhcpnet1 ~]$ sudo ip route add default via 10.3.1.254 dev enp0s3

[dorian@dhcpnet1 ~]$ sudo dnf install -y dhcp-server
```

```bash
[dorian@dhcpnet1 ~]$ sudo !!
sudo cat /etc/dhcp/dhcpd.conf
[sudo] password for dorian: 
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
option domain-name-servers 1.1.1.1;
}
```

🌞 **Preuve !**

```bash
[dorian@node1net1 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:da:11:76 brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.50/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 3515sec preferred_lft 3515sec
    inet6 fe80::a00:27ff:feda:1176/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

```bash
[dorian@node1net1 ~]$ ip r s
default via 10.3.1.254 dev enp0s3 proto dhcp src 10.3.1.50 metric 100 
10.3.1.0/24 dev enp0s3 proto kernel scope link src 10.3.1.50 metric 100 
192.168.56.0/24 dev enp0s8 proto kernel scope link src 192.168.56.2 metric 101 
```

```bash
[dorian@node1net1 ~]$ nmcli dev show | grep 'IP4.DNS'
IP4.DNS[1]:                             1.1.1.1
```



# II. Serveur Web

- [II. Serveur Web](#ii-serveur-web)
  - [1. Installation](#1-installation)
  - [2. Page HTML et racine web](#2-page-html-et-racine-web)
  - [3. Config de NGINX](#3-config-de-nginx)
  - [4. Firewall](#4-firewall)
  - [5. Test](#5-test)

## 1. Installation

> **L'install et la config sont à réaliser sur la machine `web.net2.tp3`.**

🌞 **Installation du serveur web NGINX**

```bash
[dorian@webnet2 ~]$ sudo dnf install -y nginx
```

## 2. Page HTML et racine web

🌞 **Création d'une bête page HTML**

```bash
[dorian@webnet2 var]$ sudo mkdir -p www/efrei_site_nul

[dorian@webnet2 www]$ sudo chown nginx efrei_site_nul/

[dorian@webnet2 www]$ ls -al
total 4
drwxr-xr-x.  3 root  root   28 Oct  7 16:29 .
drwxr-xr-x. 20 root  root 4096 Oct  7 16:29 ..
drwxr-xr-x.  2 nginx root    6 Oct  7 16:29 efrei_site_nul

[dorian@webnet2 www]$ sudo nano efrei_site_nul/index.html

[dorian@webnet2 efrei_site_nul]$ sudo chown nginx index.html

[dorian@webnet2 efrei_site_nul]$ ls -l
total 4
-rw-r--r--. 1 nginx root 13 Oct  7 16:32 index.html

[dorian@webnet2 efrei_site_nul]$ cat index.html 
coucou EFREI
```

## 3. Config de NGINX

🌞 **Création d'un fichier de configuration NGINX**

```bash
[dorian@webnet2 ~]$ sudo cat /etc/nginx/conf.d/webnet2.conf 
```
```nginx
  server {
      # on indique le nom d'hôte du serveur
      server_name   webnet2;

      # on précise sur quelle IP et quel port on veut que le site soit dispo
      listen        10.3.2.101:80;

      location      / {
          # on indique l'endroit où se trouve notre racine web
          root      /var/www/efrei_site_nul;

          # et on indique le nom de la page d'accueil, pour pas que le client ait besoin de le préciser explicitement
          index index.html;
      }
  }
```

## 4. Firewall

🌞 **Ouvrir le port nécessaire dans le firewall**

```bash
[dorian@webnet2 ~]$ sudo firewall-cmd --add-port=80/tcp --permanent
success

[dorian@webnet2 ~]$ sudo firewall-cmd --reload
success

[dorian@webnet2 ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3 enp0s8
  sources: 
  services: cockpit dhcpv6-client ssh
  ports: 80/tcp
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```

## 5. Test

🌞 **Démarrez le service NGINX !**

```bash
[dorian@webnet2 ~]$ sudo systemctl start nginx
[dorian@webnet2 ~]$ sudo systemctl enable nginx
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /usr/lib/systemd/system/nginx.service.
```

```bash
[dorian@webnet2 ~]$ sudo systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: disabled)
     Active: active (running) since Sat 2023-10-07 16:46:28 CEST; 46s ago
   Main PID: 11709 (nginx)
      Tasks: 2 (limit: 4611)
     Memory: 2.0M
        CPU: 13ms
     CGroup: /system.slice/nginx.service
             ├─11709 "nginx: master process /usr/sbin/nginx"
             └─11710 "nginx: worker process"
[...]
```

🌞 **Test local**

```bash
[dorian@webnet2 ~]$ curl http://10.3.2.101
coucou EFREI
```

🌞 **Accéder au site web depuis un client**

```bash
[dorian@node1net1 ~]$ curl http://10.3.2.101
coucou EFREI
```

🌞 **Avec un nom ?**

```bash
[dorian@node1net1 ~]$ sudo cat /etc/hosts 
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

10.3.2.101 webnet2
```

```bash
[dorian@node1net1 ~]$ curl http://webnet2
coucou EFREI
```

# III. Serveur DNS

- [III. Serveur DNS](#iii-serveur-dns)
  - [Intro](#intro)
  - [1. Install](#1-install)
  - [2. Config](#2-config)
  - [3. Firewall](#3-firewall)
  - [4. Test](#4-test)
  - [5. DHCP my old friend](#5-dhcp-my-old-friend)

## Intro

Dernier service qu'on va setup : **un serveur DNS.**

![Control](../img/controls.jpg)

En fin de la partie précédente vous avez utilisé le fichier `hosts`. C'est pratique. Comme vous l'avez sûrement compris, ça permet de définir localement sur une machine, et de façon arbitraire, une correspondance entre un nom et une IP. Il suffit de l'écrire dans ce fichier, and voilàààà n'importe quel nom de domaine peut être associé à une IP.

C'est un peu comme un répertoire perso où on note des numéros de tel ou des adresses : c'est local, chacun a le sien et fait ce qu'il veut avec.

Bon. C'est pratique. Mais on va pas faire ça partout : ajouter une ligne pour chaque machine, dans le fichier `hosts` de chaque machine, pour que nos serveurs se joignent avec un nom. Ce serait un enfer. Encore plus s'il fallait y ajouter la liste de toutes les adresses de tous les sites internet hehe.

**DNS à la rescousse.** Si le fichier `hosts` c'est un répertoire personnel, alors DNS c'est les pages jaunes : un répertoire central, unique, et public, que tout le monde peut consulter.

Allez, sur internet c'est un peu la jungle à ce sujet, je vous indique les étapes !

## 1. Install

> **L'install et la config sont à réaliser sur la machine `dns.net2.tp3`.**

Installation du serveur DNS :

```bash
# assurez-vous que votre machine est à jour
$ sudo dnf update -y

# installation du serveur DNS, son p'tit nom c'est BIND9
$ sudo dnf install -y bind bind-utils
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
# éditez le fichier de config principal pour qu'il ressemble à :
$ sudo cat /etc/named.conf
options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
[...] # je zappe les lignes pas importantes, vous pouvez les laisser dans votre fichier
        allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };

        recursion yes; # cette ligne autorise la recursion, voir la note en dessous de cette conf
[...]
# référence vers notre fichier de zone
zone "net2.tp3" IN {
     type master;
     file "net2.tp3.db";
     allow-update { none; };
     allow-query {any; };
};
# référence vers notre fichier de zone inverse (notez la notation à l'envers de l'IP)
zone "2.3.10.in-addr.arpa" IN {
     type master;
     file "net2.tp3.rev";
     allow-update { none; };
     allow-query { any; };
};
```

> **La *récursion*** pour un serveur DNS c'est le fait de poser la question à un autre serveur DNS si lui ne connaît pas la réponse. C'est à dire que si on demande à notre serveur DNS "à quelle IP se trouve `web.net2.tp3` ?", il saura répondre, car on va le définir un peu plus bas. En revanche si on lui demande "à quelle IP se trouve `www.google.com` ?", là il n'en sait rien. **Activer la *récursion* c'est l'autoriser à interroger un autre serveur DNS pour obtenir la réponse.** Une fois qu'il obtient la réponse, il répond au client, en indiquant que pour cette réponse, ce n'est pas lui le serveur qui fait **autorité** : il a juste relayé l'info. On dit que c'est un *DNS resolver*.

![I know a guy](../img/know_a_guy.jpg)

➜ **Et pour les fichiers de zone**

```bash
# Fichier de zone pour définir des correspondances nom -> IP
$ sudo cat /var/named/net2.tp3.db

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
# Fichier de zone inverse pour définir des correspondances IP -> nom
$ sudo cat /var/named/net2.tp3.rev

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
# Démarrez le service tout de suite
$ sudo systemctl start named

# Faire en sorte que le service démarre tout seul quand la VM s'allume
$ sudo systemctl enable named

# Obtenir des infos sur le service
$ sudo systemctl status named

# Obtenir des logs en cas de probème
$ sudo journalctl -xe -u named
```

## 3. Firewall

🌞 **Ouvrir le port nécessaire dans le firewall**

- le trafic DNS c'est encapsulé dans du UDP
- on a indiqué dans le fichier de conf principal le numéro de port à utiliser
- ouvrez donc à l'aide d'une commande ce port UDP dans le firewall de `dns.net2.tp3` (voir le [**mémo**](../../../memo/rocky_network.md))
- vérifiez avec une deuxième commande que le port est bien actuellement ouvert dans le firewall

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
