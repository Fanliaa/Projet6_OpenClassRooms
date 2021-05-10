# Script Sauvegarde de bases de données et Upload sur cloud AWS en Python

*Exemple d'un script permettant d'automatiser la sauvegarde de bases de données sur plusieurs serveurs et d'envoyer nos sauvegardes vers le cloud AWS. Ce projet a été créé dans le but de se former à la programmation de scripts d'automatisation de tâches sous Python, ce projet fait partit du Projet 6 de la formation d'__Administrateur système et Cloud__ d'__OpenClassRooms__.*

## __Installation des librairies__
Sur votre machine qui exécutera votre script vous allez devoir installer les librairies suivantes afin que votre script puisse s'exécuter correctement. *(Ici j'utilise un environement sous __Ubuntu 20.04.2 TLS__)*
```
apt install python3-pip
apt install mysql
apt install postgresql-client
pip3 install sqlite-dump
apt install paramiko
pip3 install boto3
```
___
## __Informations à renseigner pour le fichier JSON__
Dans le fichier __info_srv_template.json__ vous allez pouvoir renseigner toutes les informations nécessaire à la connexion de vos serveurs de bases de données comme l'IP de votre serveur, le type de base de données que vous utilisez, l'identifiant de connexion et son mot de passe,... *etc*.
___
## __Modifications à apporter à vos serveurs__
