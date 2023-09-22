# TP2 : Routage, DHCP et DNS

# Sommaire

- [TP2 : Routage, DHCP et DNS](#tp2--routage-dhcp-et-dns)
- [Sommaire](#sommaire)
- [I. Routage](#i-routage)
- [II. Serveur DHCP](#ii-serveur-dhcp)
- [III. ARP](#iii-arp)
  - [1. Les tables ARP](#1-les-tables-arp)
  - [2. ARP poisoning](#2-arp-poisoning)

# I. Routage

☀️ **Configuration de `router.tp2.efrei`**
```bash
[dorian@router ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
NAME=enp0s8
DEVICE=enp0s8

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.2.1.254
NETMASK=255.255.255.0

```

```bash
[dorian@router ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:28:1d:b8 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.9/24 brd 192.168.122.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2816sec preferred_lft 2816sec
    inet6 fe80::a00:27ff:fe28:1db8/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:22:de:5b brd ff:ff:ff:ff:ff:ff
    inet 10.2.1.254/24 brd 10.2.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe22:de5b/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

```bash
# On active le forwarding IPv4
[dorian@router ~]$ sudo sysctl -w net.ipv4.ip_forward=1 
net.ipv4.ip_forward = 1

# Petite modif du firewall qui nous bloquerait sinon
[dorian@router ~]$ sudo firewall-cmd --add-masquerade
success

# Et on tape aussi la même commande une deuxième fois, en ajoutant --permanent pour que ce soit persistent après un éventuel reboot
[dorian@router ~]$ sudo firewall-cmd --add-masquerade --permanent
success
```

☀️ **Configuration de `node1.tp2.efrei`**

```bash
[dorian@node1 ~]$ sudo nano /etc/sysconfig/network-scripts/ifcfg-enp0s3 
NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.2.1.1
NETMASK=255.255.255.0
```

```bash
[dorian@node1 ~]$ ping 10.2.1.254
PING 10.2.1.254 (10.2.1.254) 56(84) bytes of data.
64 bytes from 10.2.1.254: icmp_seq=1 ttl=64 time=2.21 ms
64 bytes from 10.2.1.254: icmp_seq=2 ttl=64 time=1.71 ms
```

```bash
[dorian@node1 ~]$ sudo cat /etc/sysconfig/network
# Created by anaconda
GATEWAY=10.2.1.254
```

```bash
[dorian@node1 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=113 time=31.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=113 time=31.0 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=113 time=31.6 ms
```

```bash
[dorian@node1 ~]$ traceroute 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  _gateway (10.2.1.254)  1.537 ms  1.597 ms  1.508 ms
 2  192.168.122.1 (192.168.122.1)  1.372 ms  1.554 ms  1.515 ms
 3  10.100.0.1 (10.100.0.1)  7.081 ms  7.032 ms  6.904 ms
 4  10.100.255.11 (10.100.255.11)  5.668 ms  5.619 ms  5.120 ms
 5  185.176.176.10 (185.176.176.10)  32.149 ms  32.030 ms  31.977 ms
 6  100.126.127.254 (100.126.127.254)  30.292 ms  27.643 ms  27.584 ms
 7  100.126.127.253 (100.126.127.253)  27.547 ms  27.237 ms  28.771 ms
 8  185.181.155.200 (185.181.155.200)  29.922 ms  28.660 ms  29.856 ms
 9  linkt-2.par.franceix.net (37.49.238.52)  29.819 ms  29.691 ms  29.702 ms
10  google2.par.franceix.net (37.49.236.2)  29.498 ms  29.453 ms  29.225 ms
11  108.170.244.225 (108.170.244.225)  28.937 ms 108.170.245.1 (108.170.245.1)  28.833 ms 108.170.244.193 (108.170.244.193)  29.583 ms
12  142.250.234.41 (142.250.234.41)  29.348 ms 216.239.48.139 (216.239.48.139)  32.816 ms 142.251.253.35 (142.251.253.35)  29.119 ms
13  dns.google (8.8.8.8)  28.927 ms  28.868 ms  30.861 ms
```

# II. Serveur DHCP

![Topo 2](./img/topo2.png)

➜ **Tableau d'adressage**

| Nom                | IP              |
| ------------------ | --------------- |
| `router.tp2.efrei` | `10.2.1.254/24` |
| `node1.tp2.efrei`  | `N/A`           |
| `dhcp.tp2.efrei`   | `10.2.1.253/24` |

☀️ **Install et conf du serveur DHCP** sur `dhcp.tp2.efrei`

- pour l'install du serveur, il faut un accès internet... il suffit d'ajouter là encore une route par défaut, qui passe par `router.tp2.efrei`
- référez-vous au [TP1](../1/README.md)
- cette fois, dans la conf, ajoutez une option DHCP pour donner au client l'adresse de la passerelle du réseau (c'est à dire l'adresse de `router.tp2.efrei`) en plus de leur proposer une IP libre

☀️ **Test du DHCP** sur `node1.tp2.efrei`

- enlevez toute config IP effectuée au préalable
- vous pouvez par exemple `sudo nmcli con del enp0s3` s'il s'agit de l'interface `enp0s3` pour supprimer la conf liée à `enp0s3`
- configurez l'interface pour qu'elle récupère une IP dynamique, c'est à dire avec DHCP
- vérifiez que :
  - l'IP obtenue est correcte
  - votre table de routage a bien été mise à jour automatiquement avec l'adresse de la passerelle en route par défaut (votre option DHCP a bien été reçue !)
  - vous pouvez immédiatement joindre internet

![DHCP](img/dhcp_server.png)

🌟 **BONUS**

- ajouter une autre ligne dans la conf du serveur DHCP pour qu'il donne aussi l'adresse d'un serveur DNS (utilisez `1.1.1.1` comme serveur DNS : c'est l'un des serveurs DNS de CloudFlare, un gros acteur du web)

☀️ **Wireshark it !**

- je veux une capture Wireshark qui contient l'échange DHCP DORA
- vous hébergerez la capture dans le dépôt Git avec le TP

> Si vous fouillez un peu dans l'échange DORA? vous pourrez voir les infos DHCP circuler : comme votre option DHCP qui a un champ dédié dans l'un des messages.

➜ A la fin de cette section vous avez donc :

- un serveur DHCP qui donne aux clients toutes les infos nécessaires pour avoir un accès internet automatique

# III. ARP

## 1. Les tables ARP

ARP est un protocole qui permet d'obtenir la MAC de quelqu'un, quand on connaît son IP.

On connaît toujours l'IP du correspondant avant de le joindre, c'est un prérequis. Quand vous tapez `ping 10.2.1.1`, vous connaissez l'IP, puisque vous venez de la taper :D

La machine va alors automatiquement effectuer un échange ARP sur le réseau, afin d'obtenir l'adresse MAC qui correspond à `10.2.1.1`.

Une fois l'info obtenue, l'info "telle IP correspond à telle MAC" est stockée dans la **table ARP**.

> Pour toutes les manips qui suivent, référez-vous au [mémo réseau Rocky](../../memo/rocky_network.md).

☀️ **Affichez la table ARP de `router.tp2.efrei`**

- vérifiez la présence des IP et MAC de `node1.tp2.efrei` et `dhcp.tp2.efrei`
- s'il manque l'une et/ou l'autre : go faire un `ping` : l'échange ARP sera effectuée automatiquement, et vous devriez voir l'IP et la MAC de la machine que vous avez ping dans la table ARP

☀️ **Capturez l'échange ARP avec Wireshark**

- je veux une capture de l'échange ARP livrée dans le dépôt Git
- l'échange ARP, c'est deux messages seulement : un ARP request et un ARP reply

## 2. ARP poisoning

☀️ **Exécuter un simple ARP poisoning**

- pas de man in the middle ici ou quoique ce soit, rien d'extrêmement poussé, mais simplement : écrire arbitrairement dans la table ARP de quelqu'un d'autre
- il "suffit" d'envoyer un seul message ARP pour forcer l'écriture dans la table ARP de la machine qui reçoit votre message
- je vous laisse vous renseigner par vous-mêmes un peu pour cette partie !
- le but : écrivez dans la table ARP de `node1` que l'adresse `10.2.1.254` correspond à l'adresse MAC de votre choix
  - **cela a pour conséquence que vous pouvez usurper l'identité de `10.2.1.254` (c'est le routeur) auprès de `node1`**. Stylish.

> C'est faisable super facilement en une seule commande shell : `arping`. Je recommande pas Rocky pour utiliser ça, ce sera chiant de l'installer je pense. Et bien sûr, n'hésitez pas à me contacter.

![APR sniffed ?](img/arp_sniff.jpg)
