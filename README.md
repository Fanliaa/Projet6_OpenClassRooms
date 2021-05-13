# Script Sauvegarde de bases de données et Upload sur cloud AWS en Python

*Exemple d'un script permettant d'automatiser la sauvegarde de bases de données sur plusieurs serveurs et d'envoyer nos sauvegardes vers le cloud AWS. Ce projet a été créé dans le but de se former à la programmation de scripts d'automatisation de tâches sous Python, ce projet fait partit du Projet 6 de la formation d'__Administrateur système et Cloud__ d'__OpenClassRooms__.*

## __Installation des librairies__
Sur votre machine qui exécutera votre script vous allez devoir installer les librairies suivantes afin que votre script puisse s'exécuter correctement. *(Ici j'utilise un environement sous __Ubuntu 20.04.2 TLS__)*
```
apt install python3-pip
apt install mysql
apt install postgresql-client
apt install paramiko
pip3 install -r requirements.txt
```
*Vous trouverez dans le fichier __requirements.txt__ toutes les librairies à installer via la commande __pip3__.*
___
## __Informations à renseigner pour le fichier JSON__
Dans le fichier __info_srv_template.json__ vous allez pouvoir renseigner toutes les informations nécessaire à la connexion de vos serveurs de bases de données comme l'IP de votre serveur, le type de base de données que vous utilisez, l'identifiant de connexion et son mot de passe,... *etc*.
___
## __Modifications à apporter à vos serveurs__
* __Si vous utilisez un serveur MYSQL / MariaDB__ :
    <br/> *Ici, nous utilisons la version 10.3.27 de MariaDB.*
    <br/> Dans le fichier "__/etc/mysql/mariadb.conf.d/50-server.cnf__" vous pouvez y vérifier votre port d'écoute pour être sûr de pouvoir y accéder.

* __Si vous utilisez un serveur PostgreSQL__ :
    <br/> *Ici, nous utilisons la version 11.10 de PostgreSQL.* 
    <br/> Dans le fichier "__/etc/postgresql/11/main/pg_hba.conf__" à la ligne "__IPV4 local connections__" rajoutez le réseau sur lequel se trouve votre serveur. *Par exemple :*
    ```
    host    all     all     192.168.1.0/24      md5
    ```
* __Si vous utilisez un serveur SQLite__ :
    <br/> *Ici, nous utilisons la version 3.27.2 de SQLite3.*
    <br/> Installez ssh sur votre serveur pour pouvoir se connecter sur le serveur et effectuer la sauvegarde de la base de donnée:
    ```
    apt install ssh
    ```
    Puis dans "__/etc/ssh/sshd_config__" vous pouvez vérifier le port d'écoute (*par défaut le port d'écoute est le 22*) ou modifier votre port.
    ___
    ## __Préparatif pour effectuer la sauvegarde Cloud vers AWS__
    