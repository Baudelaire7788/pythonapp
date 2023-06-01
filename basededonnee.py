import mysql.connector

ma_base_de_donnee = mysql.connector.connect(
    host     = "localhost",
    user     = "root",
    password = ""
)

mon_curseur = ma_base_de_donnee.cursor()
mon_curseur.execute("CREATE DATABASE IF NOT EXISTS projet")
ma_base_de_donnee.commit()