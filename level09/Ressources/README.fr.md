# level09
## Observations

Dans ce level on se retrouve avec deux fichiers au niveau du home directory:
- `level09`, un binaire accessible en lecture/execution disposant d'un setuid bit,
nous permettant ainsi de l'executer en tant qu'utilisateur `flag09`.
- `token`, un fichier accessible en lecture, qui en l'affichant nous donne une
string contenant des caractères non-ascii.

## Analyse du binaire

En lançant le binaire sans argument:
```sh
level09@SnowCrash:~$ ./level09
You need to provied only one arg.
```

On devra donc lancer la commande avec un argument:
```sh
level09@SnowCrash:~$ ./level09 test
tfuw
level09@SnowCrash:~$ ./level09 hello
hfnos
level09@SnowCrash:~$ ./level09 fherbine
figufntl
level09@SnowCrash:~$ ./level09 toto
tpvr
```

Le script semble chiffrer la chaîne qu'on lui donne en argument, de plus,
sur ces tests, la première lettre du cryptogramme est toujours la même que la
première lettre du message d'entrée.

Je fais plus de tests:
```sh
level09@SnowCrash:~$ ./level09 aa
ab
level09@SnowCrash:~$ ./level09 aaaaaaa
abcdefg
level09@SnowCrash:~$ ./level09 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
abcdefghijklmnopqrstuvwxyz{|}~����������������������
level09@SnowCrash:~$ ./level09 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
bcdefghijklmnopqrstuvwxyz{|}~����������
```

La méthode de chiffrement semble être assez simple, chaque caractère vaut sa valeure
en ascii + son index:
- 'a' à la position 0, vaudra 97 + 0 = 97 soit 'a'
- 'a' à la position 1, 97 + 1 = 98 => 'b'
- 'z' à la position 1, 122 + 1 = 123 => '{'

Ainsi, on pourra se retrouver avec des caractères non-ASCII, valeure >= 127, qui seront
représenté par: '�'

## Résolution

Pour résoudre ce level je vais utiliser un script en python3 (sur ma machine disponible en annexe).
Ce script va inversé le comportement du binaire de chiffrement sur le fichier token,
en soustrayant la valeur de l'index à chaque caractère de la string.

Pour éviter les erreurs, et manipuler plus simplement les caractères de la string
sous forme d'entiers, j'utilise une lecture binaire `rb`.

De plus il faut penser à retirer le retour à la ligne, avec la méthode `rstrip()`.

Dans un premier temps je copie le fichier token sur ma machine:
```sh
scp -P 4242 level09@192.168.1.14:~/token /tmp
```

Je change les droits et le propriétaire par précaution:
```sh
fherbine@fherbine-HUAWEI:~/42/SnowCrash/level09/Resources$ sudo chown fherbine: /tmp/token
[sudo] Mot de passe de fherbine :
fherbine@fherbine-HUAWEI:~/42/SnowCrash/level09/Resources$ sudo chmod 666 /tmp/token
```

Je lance mon script:
```sh
fherbine@fherbine-HUAWEI:~/42/SnowCrash/level09/Resources$ ls
README.fr.md  reverse_hash.py
fherbine@fherbine-HUAWEI:~/42/SnowCrash/level09/Resources$ python3 ./reverse_hash.py /tmp/token
f3iji1ju5yuevaus41q1afiuq
```

`f3iji1ju5yuevaus41q1afiuq` me servira de mot de passe pour accéder à l'utilisateur  `flag09`,
et effectuer la commande `getflag` pour obtenir mon flag et continuer vers le level 10.
