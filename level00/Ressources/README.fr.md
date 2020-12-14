Level00
======

Pour le level00, je n'ai pas de `README` dans le home directory de l'utilisateur
`level00`.

Après avoir regardé la [vidéo de l'intra](https://elearning.intra.42.fr/notions/snow-crash/subnotions/snow-crash/videos/snow-crash),
je m'aperçois que le présentateur de ce sujet dispose lui d'un README, ayant pour contenu:

```txt
FIND this first file who can run only as flag00...
```

Il y a plusieurs indices dans cette phrase:

- Premièrement, le mot "FIND" est écrit en majuscule, j'irai donc voir le man de `find`.
- Deuxièmement, la phrase nous indique que ce fichier est possédé par flag00 (user / groupe ?).

En consultant, le man de find, je tombe sur deux options:
- `-user [uname]`: Nous permettant de faire une recherche par utilisateur.
- `-group [gname]`: Nous permettant de faire une recherche par groupe.

Commençons avec `-user flag00` depuis la racine (on cherche sur tout le disque).
Avec:

```sh
find / -user flag00
```

Nous avons beaucoup de résultats d'erreurs (permission refusé), du type:
```
find: `/path/to/a/file': Permission denied
```

Redirigeons STDERR, sur `/dev/null`, pour ignorer ces lignes:
```sh
find / -user flag00 2>/dev/null
```

On a plus que deux sorties:
```
/usr/sbin/john
/rofs/usr/sbin/john
```

Ces deux fichiers sont semblables (commande `ls -l`):

- Même permissions
- Même propriétaire
- Et surtout même contenu: `cdiiddwpgswtgt` (lisible par TOUS cf.: `ls -l`)

Si on essaye de ce connecter directement à l'utilisateur `flag00` avec le contenu
trouvé, on échoue.

A ce stade on peut supposer que le password est hashé:
- Sa longueur fait 14 caractères.
- Ce n'est pas de l'hexadécimal: 'i' > 'f'

Nous ne sommes donc pas face à une méthode de chiffrement standard comme MD5, ou SHA-1.

La vidéo nous donne d'autres outils pour ce sujet, comme le site dcode.fr
> **Note:** J'ai également utilisé `john` à ce niveau mais sans succès.
Le site nous propose plusieurs outils pour la cryptographie sur [cette page](https://www.dcode.fr/liste-outils).

Ces outils concerne plusieurs choses:
- Des techniques de cryptanylse. Ce qui nous interesse pas vraiment pour le moment.
- Des outils de chiffrement par transposition. Qui selon [Wikipedia](https://fr.wikipedia.org/wiki/Chiffrement_par_transposition),
permet de crée un cryptogramme (message chiffré), avec les lettre présent dans le message d'entrée.
    - A première vue, rien de flagrant dans notre cryptogramme pour avoir un anagramme.
- Chiffrement par sustitution, il s'agit ici d'effectuer un "décalage" alphabetique sur notre
message d'origine pour créer un cryptogramme.
    - [Wikipedia](https://fr.wikipedia.org/wiki/Chiffrement_par_substitution) nous
    donne plus d'infos sur le sujet:
        - Il existe deux type: monoalphabétique (Rot13, César, ...) et polyalphabetique (Vigenère, Hill, Enigma).
- Il existe aussi le chiffrement polygraphique auquel je ne me suis pas vraiment interessé.

Après plusieurs test sur ce site on arrive à un résultat cohérent avec le _Code César_:
En testant toutes les décalages possibles, on s'aperçoit qu'un décalage de 15 nous donne:
`nottoohardhere`

On essaye de se connecter à l'utilisateur flag00 avec ce mot de passe:

```sh
level00@SnowCrash:~$ su flag00
Password:
Don't forget to launch getflag !
flag00@SnowCrash:~$
```

On lance la commande `getflag` pour obtenir le flag.
> **Note:** Le flag nous servira pour nous connecter à l'utilisateur.
