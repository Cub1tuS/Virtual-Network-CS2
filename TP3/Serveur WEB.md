# II. Serveur Web

- [II. Serveur Web](#ii-serveur-web)
  - [1. Installation](#1-installation)
  - [2. Page HTML et racine web](#2-page-html-et-racine-web)
  - [3. Config de NGINX](#3-config-de-nginx)
  - [4. Firewall](#4-firewall)
  - [5. Test](#5-test)

## 1. Installation

> **L'install et la config sont à réaliser sur la machine `webnet2``.**

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
