import tkinter
#import customtkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

def page_etudiant():

    def reverse(tuples):
        new_tup = tuples[::-1]
        return new_tup

    def insert(matricule, nom_prenom, tel):
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS
            etudiants(Mat VARCHAR(50) PRIMARY KEY, Nom_Prenom VARCHAR(100), Tel VARCHAR(150))""")
        mon_curseur.execute(
            "INSERT INTO etudiants VALUES('" + str(matricule) + "','" + str(nom_prenom) + "','" + str(tel) + "')")
        ma_base_de_donnee.commit()

    def delete(matricule):
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS
            etudiants(Mat VARCHAR(50) PRIMARY KEY, Nom_Prenom VARCHAR(100), Tel VARCHAR(150))""")
        mon_curseur.execute("DELETE FROM etudiants WHERE Mat='" + str(matricule) + "'")
        ma_base_de_donnee.commit()

    def update(matricule, nom_prenom, tel):
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS
            etudiants(Mat VARCHAR(50) PRIMARY KEY, Nom_Prenom VARCHAR(100), Tel VARCHAR(150))""")
        mon_curseur.execute("UPDATE etudiants SET Mat='" + str(matricule) + "', Nom_Prenom='" + str(nom_prenom) + "', Tel='" + str(
            tel) + "' WHERE Mat='" + str(matricule) + "' ")
        ma_base_de_donnee.commit()

    def read():
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS
            etudiants(Mat VARCHAR(50) PRIMARY KEY, Nom_Prenom VARCHAR(100), Tel VARCHAR(150))""")
        mon_curseur.execute("SELECT * FROM etudiants ORDER BY Mat")
        resultat = mon_curseur.fetchall()
        ma_base_de_donnee.commit()
        return resultat

    def insert_data():
        matricule = str(entryMatricule.get())
        nom_prenom = str(entryNom.get())
        tel = str(entryTel.get())
        if matricule == "" or matricule == " ":
            message = "Vous devez insérer insérer toutes les informations"
            messagebox.showerror("Erreur d'ajout !", message, parent=etudiant)
        elif nom_prenom == "" or nom_prenom == " ":
            message = "Vous devez insérer insérer toutes les informations"
            messagebox.showerror("Erreur d'ajout !", message, parent=etudiant)
        elif tel == "" or tel == " ":
            message = "Vous devez insérer insérer toutes les informations"
            messagebox.showerror("Erreur d'ajout !", message, parent=etudiant)
        else:
            insert(str(matricule), str(nom_prenom), str(tel))

        for data in my_tree.get_children():
            my_tree.delete(data)

        for result in reverse(read()):
            my_tree.insert(parent='', index='end', text="", values=result, tag="orow")

        my_tree.tag_configure('orow', background="#EEEEEE", font=('Century Gothic', 15))
        my_tree.place(x="650", y="100")

    def delete_data():
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['values'][0])
        delete(deleteData)

        for data in my_tree.get_children():
            my_tree.delete(data)

        for result in reverse(read()):
            my_tree.insert(parent='', index='end', text="", values=result, tag="orow")

        my_tree.tag_configure('orow', background="#EEEEEE", font=('Century Gothic', 15))
        my_tree.place(x="650", y="100")

    def update_data():
        selected_item = my_tree.selection()[0]
        update_nom = str(my_tree.item(selected_item)['values'][0])
        update(entryMatricule.get(), entryNom.get(), entryTel.get())

        for data in my_tree.get_children():
            my_tree.delete(data)

        for result in reverse(read()):
            my_tree.insert(parent='', index='end', text="", values=result, tag="orow")

        my_tree.tag_configure('orow', background="#EEEEEE", font=('Century Gothic', 15))
        my_tree.place(x="650", y="100")

    etudiant = tkinter.Toplevel()
    etudiant.title("Menu des Etudiants")
    etudiant.geometry('1080x500')
    etudiant.resizable(height=False, width=False)
    etudiant['bg'] = '#182029'
    icon = PhotoImage(file='icon.png')
    etudiant.iconphoto(False, icon)
    pagename = "Enregistrement des Etudiants"
    titleLabel = Label(etudiant, text=pagename, font=('Century Gothic', 30), bd=2, bg="#182029", foreground="#ffffff")
    titleLabel.place(x="250", y="25")

    matriculeLabel = Label(etudiant, text="Matricule de l'étudiant :", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    nomLabel = Label(etudiant, text="Nom et Prénom(s) :", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    telLabel = Label(etudiant, text="Numéro de l'étudiant :", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    matriculeLabel.place(x="50", y="100")
    nomLabel.place(x="50", y="200")
    telLabel.place(x="50", y="300")

    entryMatricule = Entry(etudiant, width=25, bd=2, font=('Century Gothic', 15), foreground="#182029")
    entryNom = Entry(etudiant, width=25, bd=2, font=('Century Gothic', 15), foreground="#182029")
    entryTel = Entry(etudiant, width=25, bd=2, font=('Century Gothic', 15), foreground="#182029")
    entryMatricule.place(x="300", y="100")
    entryNom.place(x="300", y="200")
    entryTel.place(x="300", y="300")

    boutonAjout = Button(
        etudiant, text="➕Ajouter", padx=5, pady=5, width=10,
        font=('Century Gothic', 15), bg="#324254", command=insert_data, foreground="#182029"
    )
    boutonAjout.place(x="50", y="400")

    boutonModifi = Button(
        etudiant, text="⭕Modifier", padx=5, pady=5, width=10,
        font=('Century Gothic', 15), bg="#bbb441", command=update_data, foreground="#182029"
    )
    boutonModifi.place(x="250", y="400")

    boutonSupp = Button(
        etudiant, text="❌Supprimer", padx=5, pady=5, width=10,
        font=('Century Gothic', 15), bg="#af4747", command=delete_data, foreground="#182029"
    )
    boutonSupp.place(x="450", y="400")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Century Gothic', 15), bg="#182029", foreground="#182029")

    my_tree = ttk.Treeview(etudiant)

    my_tree['column'] = ("Matricule", "Nom_Prenom", "Tel")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Matricule", anchor=W, width=70)
    my_tree.column("Nom_Prenom", anchor=W, width=230)
    my_tree.column("Tel", anchor=W, width=150)
    my_tree.heading("Matricule", text="Mat", anchor=W)
    my_tree.heading("Nom_Prenom", text="Nom et prénom(s)", anchor=W)
    my_tree.heading("Tel", text="Téléphone", anchor=W)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', text="", values=result, tag="orow")

    my_tree.tag_configure('orow', background="#182029", font=('Arial bold', 15))
    my_tree.place(x="620", y="100")

    projet = Label(
        etudiant, text="Projet de Python",
        font=('Century Gothic', 15), bg="#182029", foreground="#ffffff"
    )
    projet.place(x='880', y='450')