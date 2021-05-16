#!/bin/bash/python
# 
# Importation des librairies utiles
import json
import os
import pipes
import time
import datetime
import sys
import zipfile
from os.path import basename
import paramiko
import logging
import boto3
from botocore.exceptions import ClientError

# Declaration des variables
DATETIME = time.strftime('%Y-%m-%d_%H-%M-%S')
BACKUP_PATH = '/home/fanny/Documents/Sauvegardes/BACKUP_' + DATETIME
FILE_MYSQL = '/home/fanny/Documents/Sauvegardes/MySQL/'
FILE_POSTGRE = '/home/fanny/Documents/Sauvegardes/PostgreSQL/'
FILE_SQLITE = '/home/fanny/Documents/Sauvegardes/SQLite/'
BUCKET_S3 = 'backup-srv-bdd'

# Declaration des fonctions
def upload_file(file_name, bucket, object_name=None):
    # Si S3 object_name n'est pas spécifié, alors on utilisera le nom original de celui-ci
    if object_name is None:
        object_name = file_name

    with open(infoJS, "r") as filejson:
	    donnees = json.load(filejson)

    # Informations client S3
    s3_client = boto3.client('s3',
                aws_access_key_id=donnees["aws_access_key_id"],
                aws_secret_access_key=donnees["aws_secret_access_key"])
    # Permet de télécharger les fichiers que l'on souhaite et lesdéposer sur AWS
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print (response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# On verifie que le dossier de Backup n'existe pas, s'il n'existe pas on le creer
try:
    os.mkdir(BACKUP_PATH)
    print("Dossier créé.")
    os.mkdir(FILE_MYSQL)
    print("Dossier MYSQL créé.")
    os.mkdir(FILE_POSTGRE)
    print("Dossier POSTGRE créé.")
    os.mkdir(FILE_SQLITE)
    print("Dossier SQLITE créé.")
except:
    print("Certains dossiers existent déjà")
    pass

# Importer les valeurs de JSON et les stocker dans des variables
infoJS = "/home/fanny/Documents/Projet6/info_srv.json" 

with open(infoJS, "r") as filejson:
	donnees = json.load(filejson)

# Debut de la boucle
for server in donnees["databases"]:

    # Condition, boucler sur cette condition de connexion tant que c'est une BDD Mysql
    if server["type"] == 'MariaDB':
        # Sauvegarde des bases de données passées en paramètre
        os.system("mysqldump --column-statistics=0 -h " + server["ip"] + " -u " + server["user"] + " -p" + server["password"] + " " + server["BDD"] + " > " + pipes.quote(BACKUP_PATH) + "/" + server["BDD"] + ".sql")
        print("Sauvegarde de la base de donnée " + server["BDD"] + " a bien été effectuée.")
        # ZIP du fichier sql de notre base de donnée
        zf = zipfile.ZipFile (FILE_MYSQL + server["BDD"] + ".zip", mode='w')
        try:
            print("Zipping " + server["BDD"])
            zf.write(BACKUP_PATH + "/" + server["BDD"] + ".sql", basename(BACKUP_PATH + "/" + server["BDD"] + ".sql",))
        finally:
            zf.close()
            print("Le fichier ZIP a bien été créé.")
        # Envoi des zip de sauvegarde sur AWS3
        upload_file(FILE_MYSQL + "/" + server["BDD"] + ".zip", BUCKET_S3, "MYSQL/" + server["BDD"] + ".zip")
        print("Fichier zip envoyé sur AWS.")

    # Condition, boucler sur cette condition de connexion tant que c'est une BDD Postgre
    elif server["type"] == 'PostgreSQL':
        # Sauvegarde des bases de données passées en paramètre
        os.system("export PGPASSWORD=" + server["password"] + " && pg_dump --user=" + server["user"] + " --host=" + server["ip"] + " --port=" + server["port"] + " > " + pipes.quote(BACKUP_PATH) + "/" + server["BDD"] + ".sql")
        print("La sauvegarde de la base de donnée " + server["BDD"] + " a bien été effectuée.")
        zf = zipfile.ZipFile (FILE_POSTGRE + server["BDD"] + ".zip", mode='w')
        try:
            print("Zipping " + server["BDD"])
            zf.write(BACKUP_PATH + "/" + server["BDD"] + ".sql", basename(BACKUP_PATH + "/" + server["BDD"] + ".sql",))
        finally:
            zf.close()
            print("Le fichier ZIP a bien été créé.")
        upload_file(FILE_POSTGRE + "/" + server["BDD"] + ".zip", BUCKET_S3, "POSTGRE/" + server["BDD"] + ".zip")

    # Condition, boucler sur cette condition de connexion tant que c'est une BDD SQLite
    elif server["type"] == 'SQLite':
        # Connexion au server pour sauvegarder la/les BDD
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server["ip"], 22, server["user"], server["password"])
        print("Connexion au serveur réussie, lancement de la sauvegarde des bases de données du serveur.")
        ssh_client.exec_command('sqlite3 bambou.db')
        ssh_client.exec_command('.output /tmp/dump.sql')
        ssh_client.exec_command('.dump')
        ftp_client=ssh_client.open_sftp()
        ftp_client.get("/tmp/dump.sql", "" + BACKUP_PATH + "/" + server["BDD"] + ".sql")
        ftp_client.close()
        ssh_client.close()
        print("La sauvegarde de la base de donnée " + server["BDD"] + " a bien été effectuée.")
        zf = zipfile.ZipFile (FILE_SQLITE + server["BDD"] + ".zip", mode='w')
        try:
            print("Zipping " + server["BDD"])
            zf.write(BACKUP_PATH + "/" + server["BDD"] + ".sql", basename(BACKUP_PATH + "/" + server["BDD"] + ".sql",))
        finally:
            zf.close()
            print("Le fichier ZIP a bien été créé.")
        upload_file(FILE_SQLITE+ "/" + server["BDD"] + ".zip", BUCKET_S3 + "", "SQLITE/" + server["BDD"] + ".zip")

    # Fin de la boucle
    else:
        print("Pus aucune base de donnée à sauvegarder.")
        break