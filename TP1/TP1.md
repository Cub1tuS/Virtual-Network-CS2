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

```bash
[dorian@node2 ~]$ ping 10.1.1.1
PING 10.1.1.12 (10.1.1.12) 56(84) bytes of data.
64 bytes from 10.1.1.12: icmp_seq=1 ttl=64 time=0.044 ms
64 bytes from 10.1.1.12: icmp_seq=2 ttl=64 time=0.135 ms
64 bytes from 10.1.1.12: icmp_seq=3 ttl=64 time=0.098 ms
```
- Le protocole est icmp.

🌟 **BONUS**

[Un échange ARP est nécessaire pour que le ping fonctionne.](./wireshark/pingtp1.pcapng)

```bash
[dorian@node1 ~]$ ip n s
10.1.1.2 dev enp0s3 lladdr 08:00:27:38:0a:0d STALE 
192.168.56.100 dev enp0s8 lladdr 08:00:27:2e:2d:6c STALE 
192.168.56.1 dev enp0s8 lladdr 0a:00:27:00:00:00 REACHABLE 
```

# II. Ajoutons un switch
☀️ **Déterminer l'adresse MAC de vos trois machines**

```bash
[dorian@node1 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:58:fb:e9 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2580sec preferred_lft 2580sec
    inet6 fe80::a00:27ff:fe58:fbe9/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

```bash
[dorian@node2 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:38:0a:0d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.12/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2483sec preferred_lft 2483sec
    inet6 fe80::a00:27ff:fe38:a0d/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

```bash
[dorian@node3 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:fc:16:07 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.10/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2425sec preferred_lft 2425sec
    inet6 fe80::a00:27ff:fefc:1607/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

☀️ **Définir une IP statique sur les trois machines**

```bash
sudo nano /etc/sysconfig/network-scripts/ifcfg-enp0s3

NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.1.1.2
NETMASK=255.255.255.0
```
 - Définir une adresse ip différente pour chaque machine.
```bash
[dorian@node1 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:58:fb:e9 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.1/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2580sec preferred_lft 2580sec
    inet6 fe80::a00:27ff:fe58:fbe9/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

```bash
[dorian@node2 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:38:0a:0d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.2/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2483sec preferred_lft 2483sec
    inet6 fe80::a00:27ff:fe38:a0d/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

```bash
[dorian@node3 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:fc:16:07 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.3/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2425sec preferred_lft 2425sec
    inet6 fe80::a00:27ff:fefc:1607/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

☀️ **Effectuer des `ping` d'une machine à l'autre**

```bash
[dorian@node1 ~]$ ping 10.1.1.2
PING 10.1.1.2 (10.1.1.2) 56(84) bytes of data.
64 bytes from 10.1.1.2: icmp_seq=1 ttl=64 time=1.34 ms
```
```bash
[dorian@node2 ~]$ ping 10.1.1.3
PING 10.1.1.3 (10.1.1.3) 56(84) bytes of data.
64 bytes from 10.1.1.3: icmp_seq=1 ttl=64 time=1.86 ms
```

```bash
[dorian@node3 ~]$ ping 10.1.1.1
PING 10.1.1.1 (10.1.1.1) 56(84) bytes of data.
64 bytes from 10.1.1.1: icmp_seq=1 ttl=64 time=0.778 ms
```

# III. Serveur DHCP

☀️ **Donner un accès Internet à la machine `dhcp.tp1.efrei`**

```bash
[dorian@dhcp ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=25.7 ms
```

☀️ **Installer et configurer un serveur DHCP**

```bash
[dorian@dhcp ~]$ sudo dnf -y install dhcp-server
```

```bash
[dorian@dhcp ~]$ sudo nano /etc/dhcp/dhcpd.conf

default-lease-time 3600;
max-lease-time 86400;
authoritative;

subnet 10.1.1.0 netmask 255.255.255.0 {
range 10.1.1.10 10.1.1.100;
option subnet-mask 255.255.255.0;
}
```

☀️ **Récupérer une IP automatiquement depuis les 3 nodes**

```bash
[dorian@node1 ~]$ nano /etc/sysconfig/network-scripts/ifcfg-enp0s3

NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=dhcp
ONBOOT=yes
```

```bash
[dorian@node2 ~]$ nano /etc/sysconfig/network-scripts/ifcfg-enp0s3

NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=dhcp
ONBOOT=yes
```

```bash
[dorian@node3 ~]$ nano /etc/sysconfig/network-scripts/ifcfg-enp0s3

NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=dhcp
ONBOOT=yes
```

```bash
[dorian@node1 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:58:fb:e9 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 2923sec preferred_lft 2923sec
    inet6 fe80::a00:27ff:fe58:fbe9/64 scope link 
       valid_lft forever preferred_lft forever
```

```bash
[dorian@node2 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:38:0a:0d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.12/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 3006sec preferred_lft 3006sec
    inet6 fe80::a00:27ff:fe38:a0d/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

```bash
[dorian@node3 ~]$ ip a
[...]
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:fc:16:07 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.10/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 3109sec preferred_lft 3109sec
    inet6 fe80::a00:27ff:fefc:1607/64 scope link 
       valid_lft forever preferred_lft forever
[...]
```

☀️ **A l'aide de Wireshark lancé sur votre PC**

```bash
sudo dnf -y install dhclient
```

```bash
sudo dhclient -r 
sudo dhclient
```

[Résultat Wireshark pour l'échange DORA](./wireshark/doratp1.pcapng)
