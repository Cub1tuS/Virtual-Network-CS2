# I. DHCP

Bon, vous devez être rodés nan maintenant ?!

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
  - [Intro](#intro)
  - [1. Installation](#1-installation)
  - [2. Page HTML et racine web](#2-page-html-et-racine-web)
  - [3. Config de NGINX](#3-config-de-nginx)
  - [4. Firewall](#4-firewall)
  - [5. Test](#5-test)

## Intro

Dans cette section on va monter un bête serveur web. On va pas développer un site web maintenant, c'est pas DU TOUT l'objet du cours, une bête page HTML bidon fera très bien l'affaire.

**Ce qui nous intéresse c'est la partie réseau** : faire tourner le serveur web, et permettre aux PC clients du réseau d'y accéder.

Un **serveur Web** c'est un serveur qui permet de télécharger des fichiers à l'aide du protocole HTTP. Si on télécharge un fichier standard, écrit en HTML par exemple, avec un logiciel client adapté, un navigateur web par exemple, alors le navigateur met en forme visuellement le HTML et on accède à un "site web". Woaw.

On va donc, dans l'ordre :

1. setup une nouvelle machine `web.net2.tp3` (ou recycler un `node` de la première partie du TP)
2. installer un serveur web : on va utiliser NGINX ici
3. créer une bête page HTML (une phrase toute nulle dans un fichier texte, tout simplement)
4. configurer le serveur web
5. configurer le firewall de Rocky pour autoriser les clients à joindre le serveur Web
6. lancer le serveur web
7. tester qu'on accède bien au site (visualisation de notre page HTML toute nulle)

> On commence doucement à amener la notion de **firewall**. Rocky est bien évidemment muni d'un firewall actif par défaut. Il s'appelle *Firewalld* sous Rocky.

## 1. Installation

> **L'install et la config sont à réaliser sur la machine `web.net2.tp3`.**

🌞 **Installation du serveur web NGINX**

- installez le paquet `nginx`

## 2. Page HTML et racine web

🌞 **Création d'une bête page HTML**

- on va créer un nouveau dossier qui hébergera tous les fichiers de notre site (bon là y'en aura qu'un, et il sera moche, c'est un détail)
- créez le dossier `/var/www/efrei_site_nul/`

> Ce dossier va contenir tous les fichiers de notre site web. On l'appelle la ***racine*** de notre site web. Ou ***racine web***. Ou ***webroot*** pour les anglophones.

- faites le appartenir à l'utilisateur `nginx` (sinon le contenu du dossier ne sera pas accessible par le serveur Web NGINX, et il ne pourra pas servir le site !)
  - ça se fait avec une commande `chown`, n'hésitez pas à me poser des questions si c'pas clair ça
- créez un fichier texte `/var/www/efrei_site_nul/index.html` avec la phrase de votre choix à l'intérieur
  - ce fichier aussi doit appartenir à l'utilisateur `nginx`

> Un simple `coucou EFREI` ça fait l'affaire par exemple pour le contenu du fichier, vous faites pas chier avec des balises HTML on est pas là pour ça, ça fonctione très bien sans, pour un ptit test comme celui-ci en tout cas.

## 3. Config de NGINX

🌞 **Création d'un fichier de configuration NGINX**

- on va indiquer à NGINX qu'il faut servir un nouveau site web
  - il faut lui indiquer la racine de notre site web
  - et indiquer sur quelle IP et quel port ce site doit être accessible
- créez le fichier `/etc/nginx/conf.d/web.net2.tp3.conf` et ajoutez le contenu suivant :

```nginx
  server {
      # on indique le nom d'hôte du serveur
      server_name   web.net2.tp3;

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

- le trafic HTTP c'est encapsulé dans du TCP
- comme indiqué dans la conf, on va servir le site sur le port standard : 80
- ouvrez donc à l'aide d'une commande le port 80 dans le firewall de `web.net2.tp3` (voir le [**mémo**](../../../memo/rocky_network.md))
- vérifiez avec une deuxième commande que le port est bien actuellement ouvert dans le firewall

## 5. Test

🌞 **Démarrez le service NGINX !**

- s'il y a des soucis, lisez bien les lignes d'erreur, et n'hésitez pas à m'appeler

```bash
# Démarrez le service tout de suite
$ sudo systemctl start nginx

# Faire en sorte que le service démarre tout seul quand la VM s'allume
$ sudo systemctl enable nginx

# Obtenir des infos sur le service
$ sudo systemctl status nginx

# Obtenir des logs en cas de probème
$ sudo journalctl -xe -u nginx
```

🌞 **Test local**

- vous pouvez visiter le site web en local, depuis la ligne de commande de la machine `web.net2.tp3`, avec la commande `curl` : par exemple `curl http://10.3.2.101`

> *La commande `curl` permet de faire des requêtes HTTP depuis la ligne de commande. Inutile de dire que l'HTML, CSS etc. ne seront pas rendus visuellement, et qu'ils s'afficheront en brut dans le terminal.*

🌞 **Accéder au site web depuis un client**

- direction n'importe quelle machine du réseau 1, et accédez au site web
- vous pouvez ajouter une machine avec interface graphique si vous voulez, sinon un `curl` fera très bien l'affaire !

🌞 **Avec un nom ?**

- utilisez le fichier `hosts` de votre machine client pour accéder au site web en saissant `http://web.net2.tp3` (ce qu'on avait écrit dans la conf quoi !)
- référez-vous au [**mémo**](../../../memo/rocky_network.md) pour la modification du fichier `hosts`
