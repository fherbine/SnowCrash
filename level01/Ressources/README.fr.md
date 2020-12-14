Pour cette exercice plus simple.

(Aparté)
Premièrement, il y'a d'une part un ensemble de
commande que je lance usuellement en arrivant sur un système inconnu, comme:

- `w`, `id`: Pour avoir un statut sur les utilisateurs connecté dont "moi".
- `last`: Qui me donne des infos sur les derniers utilisateurs connectés. Inutilisable ici.
- Ou encore des commandes pour avoir des statuts sur les processus en cours d'exectution (`ps`, `top`).

Il s'avère donc, qu'avec tout ce genre d'opérations, j'avais trouvé un gros indice dès le level00 (/etc/passwd).
Toutefois, par acquis de conscience, je préfère expliquer mon travail comme si je n'avais rien vu.
(Fin de l'aparté)

Ma commande id me donne mon nom d'utilisateur et mon groupe, comme pour le level précédent,
je peux tenter une commande find à la racine, cette fois pour mon utilisateur / groupe (level01):

```sh
find / -user level01 -group level01 2>/dev/null
```

Cette commande ne renvoie que des fichiers situés sous `/proc`, qui selon le [FHS](https://fr.wikipedia.org/wiki/Filesystem_Hierarchy_Standard)
contient des fichiers utilisés par les différent processus, à priori, rien d'interessant pour nous.

On peut aussi essayer de repérer les fichiers lisible par tous (donc moi) avec: 
```sh
find / -perm -a+r
```

> C'est grâce à cette commande que l'on peut retrouver le fichier `/etc/passwd`

> **Note**: Le fichier `/etc/passwd` est assez connu comme fichier de configuration,
> c'est la raison pour laquelle, j'ai pû m'y interesser directement.
> Ce fichier contient notamment l'username, les uid/gid, home directory, shell,
> mais surtout les password (si il n'utilise pas `shadow`, dans ce cas 'x' pour le password)

Si on affiche ce fichier (commande `cat`), l'utilisateur `flag01`, n'a pas pour
mot de passe 'x' (`shadow`) mais, `42hDRfypTqqnw`.

Si on essaye, de se connecter à l'utilisateur level01, on échoue.
Le mot de passe est donc chiffré.
On essaye d'utiliser un autre outil de la vidéo ici `john` (pour John the ripper).
Il s'agit d'un logiciel de cassage de mots de passe qui embarque avec lui, différentes fonctions de hachage.

Pour se  faire j'ai copié le cryptogramme dans un fichier sur mon ordinateur, installé `john`,
et j'ai lancé les deux ensembles:

```sh
fherbine@fherbine-HUAWEI:/tmp$ cat pass
42hDRfypTqqnw
fherbine@fherbine-HUAWEI:/tmp$ john pass
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 128/128 SSE2-16])
Press 'q' or Ctrl-C to abort, almost any other key for status
abcdefg          (?)
1g 0:00:00:00 100% 2/3 50.00g/s 38400p/s 38400c/s 38400C/s raquel..bigman
Use the "--show" option to display all of the cracked passwords reliably
Session completed
fherbine@fherbine-HUAWEI:/tmp$
```

`john` nous renvoie un résultat, `abcdefg`.
On essaye de se connecter à l'utilisateur flag01 avec, et ça marche, on peut donc obtenir le flag et se connecter à l'utilisateur suivant.
