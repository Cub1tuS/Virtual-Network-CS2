# I. DHCP

🌞 **Setup de la machine `dhcp.net1.tp3`**

```bash
[dorian@dhcpnet1 ~]$ sudo ip route add default via 10.3.1.254 dev enp0s3

[dorian@dhcpnet1 ~]$ sudo dnf install -y dhcp-server
```

```bash
[dorian@dhcpnet1 ~]$ sudo !!
sudo cat /etc/dhcp/dhcpd.conf

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
IP4.DNS[1]: 1.1.1.1
```
