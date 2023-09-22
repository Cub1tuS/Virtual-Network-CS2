# TP1

## Sommaire

- [I. Most simplest LAN](#i-most-simplest-lan)
- [II. Ajoutons un switch](#ii-ajoutons-un-switch)
- [III. Serveur DHCP](#iii-serveur-dhcp)


# I. Most simplest LAN


☀️ **Déterminer l'adresse MAC de vos deux machines**

```bash
dorian@node1:~$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:58:fb:e9 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 3286sec preferred_lft 3286sec
    inet6 fe80::a00:27ff:fe58:fbe9/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

```bash
dorian@node2 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:38:0a:0d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.12/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 3170sec preferred_lft 3170sec
    inet6 fe80::a00:27ff:fe38:a0d/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

☀️ **Définir une IP statique sur les deux machines**

```bash
sudo nano /etc/sysconfig/network-scripts/ifcfg-enp0s3

NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.1.1.2
NETMASK=255.255.255.0
```
```bash
dorian@node2 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:38:0a:0d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.2/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 3170sec preferred_lft 3170sec
    inet6 fe80::a00:27ff:fe38:a0d/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```
```bash
sudo nmcli con reload
sudo nmcli con up enp0s3
```

☀️ **Effectuer un `ping` d'une machine à l'autre**

```bash
[dorian@node2 ~]$ ping 10.1.1.1
PING 10.1.1.12 (10.1.1.12) 56(84) bytes of data.
64 bytes from 10.1.1.12: icmp_seq=1 ttl=64 time=0.044 ms
64 bytes from 10.1.1.12: icmp_seq=2 ttl=64 time=0.135 ms
64 bytes from 10.1.1.12: icmp_seq=3 ttl=64 time=0.098 ms
```

☀️ **A l'aide de Wireshark lancé sur votre PC**

[Résultat Wireshark](./wireshark/pingtp1.pcapng)


- visualiser le `ping` entre les deux machines
- enregistrez la capture avec Wireshark (format `.pcap` ou `.pcapng`), et vous la joindrez au compte-rendu dans le dépôt git
- précisez dans le compte-rendu quel protocole est utilisé pour envoyer le message `ping`

🌟 **BONUS**

- est-ce qu'un échange ARP a été nécessaire pour que le `ping` fonctionne ?
- utilisez une commande depuis `node1.tp1.efrei` pour connaître la MAC de son correspondant `node2.tp1.efrei`

# II. Ajoutons un switch

![Topologie n°2](./img/topo2.png)

Un switch vient résoudre une problématique simple : comment relier + de deux machines entre elles ? Le switch agit comme une simple multiprise réseau (dans son fonctionnement basique du moins ; un switch moderne possède des fonctionnalités plus avancées).

Le switch n'est pas vraiment un membre du réseau : il n'a pas d'adresse IP, on ne peut pas directement lui envoyer de message. Il se charge simplement de faire passer les messages d'une machine à une autre lorsqu'elles souhaitent discuter.

On va commencer simple : GNS3 fournit des switches tout nuls, prêts à l'emploi.

> *Vous pouvez réutiliser les machines de la partie précédente.*

| Machine           | Adresse IP    |
| ----------------- | ------------- |
| `node1.tp1.efrei` | `10.1.1.1/24` |
| `node2.tp1.efrei` | `10.1.1.2/24` |
| `node3.tp1.efrei` | `10.1.1.3/24` |

☀️ **Déterminer l'adresse MAC de vos trois machines**

☀️ **Définir une IP statique sur les trois machines**

- prouver que votre changement d'IP est effectif, en une commande

☀️ **Effectuer des `ping` d'une machine à l'autre**

- vérifiez que tout le monde peut se joindre
  - `node1` à `node2`
  - `node2` à `node3`
  - `node1` à `node3`

> Le message `ping` attend une réponse : `pong`. Ainsi, dans un setup aussi simple, inutile de tester `node2` vers `node1` si on a déjà testé `node1` vers `node2`. En effet, lorsque `node2` a reçu le `ping` de `node1`, il a répondu par un `pong`. On est donc déjà assurés que ça fonctionne correctement dans les deux sens.

# III. Serveur DHCP

![Topologie n°3](./img/topo3.png)

Pour finir ce premier TP, on va mettre en place une 4ème machine : un serveur DHCP.

Le serveur DHCP est chargé d'attribuer des IPs à des clients qui le demandent. Ca évite la tâche fastidieuse de saisir une IP manuellement.

| Machine           | Adresse IP      |
| ----------------- | --------------- |
| `node1.tp1.efrei` | `N/A`           |
| `node2.tp1.efrei` | `N/A`           |
| `node3.tp1.efrei` | `N/A`           |
| `dhcp.tp1.efrei`  | `10.1.1.253/24` |

> Les IPs des trois nodes ne sont plus renseignées car le but de cette partie va être de faire en sorte qu'il puisse obtenir automatiquement une IP disponible, qui n'est pas déjà utilisée au sein du réseau, grâce au serveur DHCP.

☀️ **Donner un accès Internet à la machine `dhcp.tp1.efrei`**

- pour ce faire, ajoutez une carte réseau NAT à la machine dans VirtualBox
- une fois la machine démarrée, assurez-vous en une commande que vous avez un accès internet

Cet ajout de carte NAT est temporaire : c'est juste pour installer le paquet nécessaire pour le serveur DHCP. Dès que vous avez passer votre commande `dnf install`, **IL FAUDRA** enlever la carte NAT et retourner dans le setup normal.

> Très vite dans les TPs, on mettra un accès internet direct à l'aide de notre topologie, en incluant des routeurs. On trick pour ce TP1 en passant par une carte NAT :)

☀️ **Installer et configurer un serveur DHCP**

- à réaliser sur `dhcp.tp1.efrei`
- je n'aime pas ré-écrire la roue, et préfère pour vous renvoyer vers des ressources dispos en ligne quand elles sont suffisantes
- go google "rocky linux 9 dhcp server" ou utilisez [**cet article**](https://www.server-world.info/en/note?os=Rocky_Linux_8&p=dhcp&f=1)
- ne tapez les commandes que si vous comprenez à quoi elles servent

> **N'oubliez pas d'enlever la carte NAT et remettre dans le setup initial une fois que vous avez passé votre commande `dnf install`.**

☀️ **Récupérer une IP automatiquement depuis les 3 nodes**

- là encore, montrez toutes les commandes réalisées
- et le contenu des fichiers que vous éditez, si vous en éditez
- prouver que votre changement d'IP est effectif, en une commande

☀️ **A l'aide de Wireshark lancé sur votre PC**

- mettez en évidence l'échange qui est réalisé pour qu'une machine récupère une IP en DHCP
- l'échange est constitué de 4 messages, échangés entre le client et le serveur DHCP
- *hint* : on appelle souvent cet échange DORA
- une fois que vous avez visualisé cet échange, enregistrez la capture avec Wireshark, et joignez-la au compte rendu