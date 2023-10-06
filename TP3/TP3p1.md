# Mise en place de la topologie et routage
  - [I. Setup GNS3](#i-setup-gns3)
  - [II. Routes routes routes](#ii-routes-routes-routes)

### Tableau d'adressage

| Machine          | Réseau 1        | Réseau 2        | Réseau 3        |
| ---------------- | --------------- | --------------- | --------------- |
| `node1.net1.tp3` | `10.3.1.11/24`  | nop             | nop             |
| `node2.net1.tp3` | `10.3.1.12/24`  | nop             | nop             |
| `router1.tp3`    | `10.3.1.254/24` | nop             | `10.3.100.1/30` |
| `router2.tp3`    | nop             | `10.3.2.254/24` | `10.3.100.2/30` |
| `node1.net2.tp3` | nop             | `10.3.2.11/24`  | nop             |
| `node2.net2.tp3` | nop             | `10.3.2.12/24`  | nop             |

## I. Setup GNS3

🌞 **Mettre en place la topologie dans GS3**

**Réseau 1**

```bash
[dorian@node1net1 ~]$ ping 10.3.1.12
PING 10.3.1.12 (10.3.1.12) 56(84) bytes of data.
64 bytes from 10.3.1.12: icmp_seq=1 ttl=64 time=1.98 ms
64 bytes from 10.3.1.12: icmp_seq=2 ttl=64 time=1.65 ms
^C
--- 10.3.1.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.646/1.811/1.977/0.165 ms

[dorian@node1net1 ~]$ ping 10.3.1.254
PING 10.3.1.254 (10.3.1.254) 56(84) bytes of data.
64 bytes from 10.3.1.254: icmp_seq=1 ttl=64 time=1.79 ms
64 bytes from 10.3.1.254: icmp_seq=2 ttl=64 time=1.53 ms
^C
--- 10.3.1.254 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.530/1.660/1.791/0.130 ms
```

```bash
[dorian@node2net1 ~]$ ping 10.3.1.254
PING 10.3.1.254 (10.3.1.254) 56(84) bytes of data.
64 bytes from 10.3.1.254: icmp_seq=1 ttl=64 time=1.69 ms
64 bytes from 10.3.1.254: icmp_seq=2 ttl=64 time=1.57 ms
^C
--- 10.3.1.254 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.567/1.628/1.689/0.061 ms
```

**Réseau 2**
```bash
[dorian@node1tp2 ~]$ ping 10.3.2.11
PING 10.3.2.11 (10.3.2.11) 56(84) bytes of data.
64 bytes from 10.3.2.11: icmp_seq=1 ttl=64 time=0.051 ms
64 bytes from 10.3.2.11: icmp_seq=2 ttl=64 time=0.077 ms
^C
--- 10.3.2.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1047ms
rtt min/avg/max/mdev = 0.051/0.064/0.077/0.013 ms

[dorian@node1tp2 ~]$ ping 10.3.2.254
PING 10.3.2.254 (10.3.2.254) 56(84) bytes of data.
64 bytes from 10.3.2.254: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 10.3.2.254: icmp_seq=2 ttl=64 time=1.74 ms
^C
--- 10.3.2.254 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.738/2.041/2.344/0.303 ms
```

```bash
[dorian@node2tp2 ~]$ ping 10.3.2.254
PING 10.3.2.254 (10.3.2.254) 56(84) bytes of data.
64 bytes from 10.3.2.254: icmp_seq=1 ttl=64 time=1.67 ms
64 bytes from 10.3.2.254: icmp_seq=2 ttl=64 time=1.46 ms
^C
--- 10.3.2.254 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.461/1.563/1.665/0.102 ms
```

**Réseau 3**

```bash
[dorian@router1 ~]$ ping 10.3.100.2
PING 10.3.100.2 (10.3.100.2) 56(84) bytes of data.
64 bytes from 10.3.100.2: icmp_seq=1 ttl=64 time=1.56 ms
64 bytes from 10.3.100.2: icmp_seq=2 ttl=64 time=1.41 ms
^C
--- 10.3.100.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1005ms
rtt min/avg/max/mdev = 1.413/1.484/1.555/0.071 ms
```

**Internet `router1.tp3`**

```bash
[dorian@router1 ~]$ ping google.com
PING google.com (172.217.20.174) 56(84) bytes of data.
64 bytes from waw02s07-in-f14.1e100.net (172.217.20.174): icmp_seq=1 ttl=114 time=15.4 ms
64 bytes from waw02s07-in-f14.1e100.net (172.217.20.174): icmp_seq=2 ttl=114 time=17.0 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 15.359/16.185/17.011/0.826 ms

[dorian@router1 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=114 time=15.6 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=114 time=17.2 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 15.570/16.401/17.233/0.831 ms
```

## II. Routes routes routes

🌞 **Activer le routage sur les deux machines `router`**

**J'active le routage sur `router1` et `router2`**
```bash
sudo sysctl -w net.ipv4.ip_forward=1

sudo firewall-cmd --add-masquerade

sudo firewall-cmd --add-masquerade --permanent
```

🌞 **Mettre en place les routes locales**

```bash
[dorian@router1 ~]$ cat /etc/sysconfig/network-scripts/route-enp0s8 
10.3.2.0/24 via 10.3.100.2

[dorian@router2 ~]$ sudo ip route add 10.3.2.0/24 via 10.3.100.2 dev enp0s8
```

```bash
[dorian@router2 ~]$ sudo ip route add 10.3.1.0/24 via 10.3.100.1 dev enp0s3

[dorian@router2 ~]$ sudo cat /etc/sysconfig/network-scripts/route-enp0s3
10.3.1.0/24 via 10.3.100.1

[dorian@router2 ~]$ ping 10.3.2.11
PING 10.3.2.11 (10.3.2.11) 56(84) bytes of data.
64 bytes from 10.3.2.11: icmp_seq=1 ttl=64 time=1.38 ms
64 bytes from 10.3.2.11: icmp_seq=2 ttl=64 time=1.54 ms
64 bytes from 10.3.2.11: icmp_seq=3 ttl=64 time=1.76 ms
^C
--- 10.3.2.11 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 1.378/1.559/1.762/0.157 ms
```

```bash
[dorian@node1net1 ~]$ sudo cat /etc/sysconfig/network-scripts/route-enp0s3
10.3.2.0/24 via 10.3.1.254

[dorian@node1net1 ~]$ sudo ip route add 10.3.2.0/24 via 10.3.1.254 dev enp0s3

[dorian@node1net1 ~]$ ping 10.3.2.11
PING 10.3.2.11 (10.3.2.11) 56(84) bytes of data.
64 bytes from 10.3.2.11: icmp_seq=1 ttl=62 time=5.80 ms
64 bytes from 10.3.2.11: icmp_seq=2 ttl=62 time=4.14 ms
^C
--- 10.3.2.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 4.139/4.967/5.795/0.828 ms
```

```bash
[dorian@node2net1 ~]$ sudo cat /etc/sysconfig/network-scripts/route-enp0s3
10.3.2.0/24 via 10.3.1.254

[dorian@node2net1 ~]$ sudo ip route add 10.3.2.0/24 via 10.3.1.254 dev enp0s3

[dorian@node2net1 ~]$ ping 10.3.2.11
PING 10.3.2.11 (10.3.2.11) 56(84) bytes of data.
64 bytes from 10.3.2.11: icmp_seq=1 ttl=62 time=4.65 ms
64 bytes from 10.3.2.11: icmp_seq=2 ttl=62 time=3.61 ms
^C
--- 10.3.2.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 3.614/4.131/4.648/0.517 ms
```

```bash
[dorian@node1net2 ~]$ sudo ip route add 10.3.1.0/24 via 10.3.2.254 dev enp0s3

[dorian@node1net2 ~]$ sudo cat /etc/sysconfig/network-scripts/route-enp0s3
10.3.1.0/24 via 10.3.2.254

[dorian@node1net2 ~]$ ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=62 time=3.63 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=62 time=3.44 ms
^C
--- 10.3.1.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 3.436/3.532/3.628/0.096 ms
```

```bash
[dorian@node2net2 ~]$ sudo ip route add 10.3.1.0/24 via 10.3.2.254 dev enp0s3

[dorian@node2net2 ~]$ sudo cat /etc/sysconfig/network-scripts/route-enp0s3
10.3.1.0/24 via 10.3.2.254

[dorian@node2net2 ~]$ ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=62 time=1.90 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=62 time=3.84 ms
^C
--- 10.3.1.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.895/2.865/3.835/0.970 ms
```

🌞 **Mettre en place les routes par défaut**
```bash
[dorian@node1net1 ~]$ echo 'GATEWAY=10.3.1.254' | sudo tee /etc/sysconfig/network

[dorian@node2net1 ~]$ echo 'GATEWAY=10.3.1.254' | sudo tee /etc/sysconfig/network

[dorian@node1net2 ~]$ echo 'GATEWAY=10.3.2.254' | sudo tee /etc/sysconfig/network

[dorian@node2net2 ~]$ echo 'GATEWAY=10.3.2.254' | sudo tee /etc/sysconfig/network

[dorian@router2 ~]$ echo 'GATEWAY=10.3.100.1' | sudo tee /etc/sysconfig/network
```

**Je reboot mes machines**

```bash
[dorian@node1net1 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=4 ttl=113 time=1986 ms
64 bytes from 8.8.8.8: icmp_seq=5 ttl=113 time=962 ms
64 bytes from 8.8.8.8: icmp_seq=6 ttl=113 time=17.2 ms
64 bytes from 8.8.8.8: icmp_seq=7 ttl=113 time=18.7 ms
64 bytes from 8.8.8.8: icmp_seq=8 ttl=113 time=18.8 ms
^C
--- 8.8.8.8 ping statistics ---
8 packets transmitted, 5 received, 37.5% packet loss, time 7141ms
rtt min/avg/max/mdev = 17.239/600.422/1985.645/783.086 ms, pipe 2
```

```bash
[dorian@node2net1 ~]$ traceroute 1.1.1.1
traceroute to 1.1.1.1 (1.1.1.1), 30 hops max, 60 byte packets
 1  * * *
 2  192.168.122.1 (192.168.122.1)  1.232 ms  1.193 ms  1.430 ms
 3  10.100.0.1 (10.100.0.1)  6.530 ms  6.494 ms  6.459 ms
 4  10.100.255.11 (10.100.255.11)  5.474 ms  5.433 ms  5.183 ms
 5  185.176.176.10 (185.176.176.10)  23.785 ms  23.741 ms  23.622 ms
 6  100.126.127.254 (100.126.127.254)  18.039 ms  17.725 ms  17.682 ms
 7  100.126.127.253 (100.126.127.253)  16.172 ms  14.681 ms  14.629 ms
 8  185.181.155.200 (185.181.155.200)  14.796 ms  17.744 ms  17.698 ms
 9  linktsas-ic-381495.ip.twelve99-cust.net (62.115.186.121)  17.659 ms  18.032 ms  16.854 ms
10  prs-b1-link.ip.twelve99.net (62.115.186.86)  16.807 ms prs-b9-link.ip.twelve99.net (62.115.186.120)  16.772 ms  15.291 ms
11  cloudflare-ic-375100.ip.twelve99-cust.net (80.239.194.103)  15.426 ms prs-b1-link.ip.twelve99.net (62.115.115.88)  19.741 ms  18.157 ms
12  cloudflare-ic-363840.ip.twelve99-cust.net (213.248.73.69)  18.101 ms cloudflare-ic-375100.ip.twelve99-cust.net (80.239.194.103)  52.670 ms 172.71.128.2 (172.71.128.2)  20.049 ms
13  172.71.116.2 (172.71.116.2)  37.892 ms one.one.one.one (1.1.1.1)  19.711 ms 172.71.132.2 (172.71.132.2)  19.592 ms
```
