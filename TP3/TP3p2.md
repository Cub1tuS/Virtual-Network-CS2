# Services Réseau

- [Services Réseau](#services-réseau)
  - [Présentation](#présentation)
    - [Topologie](#topologie)
    - [Tableau d'adressage](#tableau-dadressage)

## Présentation

On va aller un peu plus loin dans cette partie et différencier nos deux réseaux :

- le réseau 1 représentera un réseau pour des clients classiques du réseau : les employés d'une entreprise par exemple
- le réseau 2 représentera la salle serveur de l'établissement : on y trouve donc les serveurs d'infrastructure

Ainsi, dans cette partie, on va monter plusieurs services, orientés réseau, que l'on retrouve dans la plupart des réseaux classiques.

**Au menu :**

➜ **Serveur DHCP, again !**

- sur une machine `dhcp.net1.tp3`
- comme d'hab, il filera des IP à nos clients, et leur indiquera aussi comment joindre internet
- il a besoin d'être dans le même réseau que les clients à qui il file des IPs, il sera donc dans le réseau 1
- à l'inverse, on attribue aux serveurs des IPs statiques, pas de DHCP pour les serveurs !

➜ **Serveur Web**

- sur une machine `web.net2.tp3`
- il hébergera un bête site web d'accueil, qui symbolisera un site web d'entreprise par exemple
- il sera dans le réseau 2

➜ **Serveur DNS**

- sur une machine `dns.net2.tp3`
- il permettra à toutes les machines de notre parc de se joindre avec leurs noms respectifs
- ainsi on pourra accéder au site web en utilisant l'adresse `http://web.net2.tp3` dans le navigateur d'un des clients

> *Ainsi, on aura touché à trois protocoles extrêmement communs dans toute infrastructure : DHCP, DNS et HTTP.*

### Topologie

![Topologie 2](./../img/topo2.png)

### Tableau d'adressage

| Machine          | Réseau 1        | Réseau 2        | Réseau 3        |
| ---------------- | --------------- | --------------- | --------------- |
| `node1.net1.tp3` | `10.3.1.11/24`  | nop             | nop             |
| `dhcp.net1.tp3`  | `10.3.1.253/24` | nop             | nop             |
| `router1.tp3`    | `10.3.1.254/24` | nop             | `10.3.100.1/30` |
| `router2.tp3`    | nop             | `10.3.2.254/24` | `10.3.100.2/30` |
| `web.net2.tp3`   | nop             | `10.3.2.101/24` | nop             |
| `dns.net2.tp3`   | nop             | `10.3.2.102/24` | nop             |

Remarquez dans le tableau d'adressage que :

- il n'y a plus de clients dans le réseau 2
  - ouais bah c'est la salle serveur, pas de PC client dans la salle serveur, que des serveurs !
- il reste un client dans le réseau 1
  - normal : c'est le réseau des clients, c'est avec eux qu'on testera que tout fonctionne

> Ne vous gênez pas pour recycler `node1.net2.tp3` et `node2.net2.tp3` en `web.net2.tp3` et `dns.net2.tp3`. Veillez à bien reconfigurer les IPs et les noms d'hôte. Aussi, n'hésitez pas à descendre la RAM allouée aux VMs si ça commence à faire beaucoup de machines.

Une fois la topologie légèrement modifiée, les machines ré-adressées et renommées, passez à la suite, dans l'ordre :

1. [**Serveur DHCP**](./dhcp.md)
2. [**Serveur Web**](./web.md)
3. [**Serveur DNS**](./dns.md)
