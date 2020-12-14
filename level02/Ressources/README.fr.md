# Level02

## Récupération du fichier:
Pour ce level, on nous fournit un fichier `.pcap` au niveau du home directory: `level02.pcap`
Après quelques recherches (voir [ici](https://www.reviversoft.com/fr/file-extensions/pcap)),
On voit quze ce genre de fichier correspond à un fichier d'enregistrement réseau,
on peut donc l'ouvrir avec un logiciel comme Wireshark.

Je décide donc de copier le fichier sur mon ordinateur:
```sh
scp -P 4242 level02@192.168.1.14:~/level02.pcap /tmp
```

N'ayant pas les droits de l'ouvrir directement (`ls -l`), je décide de l'ouvrir
avec `sudo`:
```sh
sudo wireshark /tmp/level02.pcap
```

## Observations

On s'aperçoit de plusieurs choses:
- Le fichier fait état d'une communication entre deux acteurs: ports 12121 et 39247.
- Tous les échanges se font par des segments [TCP](https://fr.wikipedia.org/wiki/Transmission_Control_Protocol)
    - _TCP_ est un protocole réseau de la couche 4 (transport du modèle OSI).
    - Il embarque ainsi avec lui les headers des couches précédentes:
        - couche 3, ou _réseau_, ici le protocole IP.
        - couche 2, ou _liaison_, ici le protocole Ethernet.
    - Vient ensuite le header TCP (cf: wiki)
    - Puis la data

On s'aperçoit qu'au segment n°43, un segment est envoyé du port 12121 (_serveur_),
vers le port 39247 (_client_). Ce segment contient les données suivantes:

**Hexa**: 00 0d 0a 50 61 73 73 77 64 3a 20
**ASCII**: "\0\r\nPassword:"

Plusieurs remarque:
- La connexion n'est pas chiffrée
- Nous nous interesseront à la réponse du client.
    - Pour se faire on peut filtrer les segments sur wireshark avec: `tcp.dstport==12121`
    - De plus nous ignoreront les segments de type `ACK` (Acknowledge) seulement, qui ne sont que des accusé de reception.

Ainsi, nous nous intèresseront à tous les segments (où de la donnée est transmise du client au serveur)
jusqu'à un apui sur la touche \[Entrée\](retour chariot, '\r' ou '\n'):

On à donc des segments n°45 à 85, les données suivantes:

**Héxa**: 66 74 5f 77 61 6e 64 72 7f 7f 7f 4e 44 52 65 6c 7f 4c 30 4c 0d
**ASCII**: `"ft_wandr[DEL][DEL][DEL]NDRel[DEL]L0L\r"`

Si on corrige les backspaces:
"ft_waNDReL0L"

On tente de se connecter à l'utilisateur `flag02`, et ça marche,
On peut obtenir le flag (`getflag`), et passer à l'utilisateur suivant.
