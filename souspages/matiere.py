import tkinter
#import customtkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

def page_matieres():
    def reverse(tuples):
        new_tup = tuples[::-1]
        return new_tup

    def insert(code, nom, coef):
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS
            matieres(Code VARCHAR(50) PRIMARY KEY, Nom_Matiere VARCHAR(100), Coef VARCHAR(50))""")
        mon_curseur.execute(
            "INSERT INTO matieres VALUES('" + str(code) + "','" + str(nom) + "','" + str(coef) + "')")
        ma_base_de_donnee.commit()

    def delete(code):
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS
            matieres(Code VARCHAR(50) PRIMARY KEY, Nom_Matiere VARCHAR(100), Coef VARCHAR(50))""")
        mon_curseur.execute("DELETE FROM matieres WHERE Code='" + str(code) + "'")
        ma_base_de_donnee.commit()

    def update(code, nom, coef):
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS
            matieres(Code VARCHAR(50) PRIMARY KEY, Nom_Matiere VARCHAR(100), Coef VARCHAR(50))""")
        mon_curseur.execute("UPDATE matieres SET Code='" + str(code) + "', Nom_Matiere='" + str(nom) + "', Coef='" + str(
            coef) + "' WHERE Code='" + str(code) + "' ")
        ma_base_de_donnee.commit()

    def read():
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS matieres(Code VARCHAR(50) PRIMARY KEY, Nom_Matiere VARCHAR(100), Coef VARCHAR(50))""")
        mon_curseur.execute("SELECT * FROM matieres")
        resultat = mon_curseur.fetchall()
        ma_base_de_donnee.commit()
        return resultat

    def insert_data():
        code = str(entryCode.get())
        nom = str(entryNom.get())
        coef = str(entryCoef.get())
        if (code == "" or code == " ") or (nom == "" or nom == " ") or (coef == "" or coef == " "):
            message = "Vous devez insérer insérer toutes les informations"
            messagebox.showerror("Erreur d'ajout !", message, parent=matieres)
        else:
            insert(str(code), str(nom), str(coef))

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
        update(entryCode.get(), entryNom.get(), entryCoef.get())

        for data in my_tree.get_children():
            my_tree.delete(data)

        for result in reverse(read()):
            my_tree.insert(parent='', index='end', text="", values=result, tag="orow")

        my_tree.tag_configure('orow', background="#EEEEEE", font=('Century Gothic', 15))
        my_tree.place(x="650", y="100")

    matieres = tkinter.Toplevel()
    matieres.title("Menu des Matieres")
    matieres.geometry('1015x500')
    matieres.resizable(height=False, width=False)
    matieres['bg'] = '#182029'
    icon = PhotoImage(file='icone.png')
    matieres.iconphoto(False, icon)
    pagename = "Enregistrement des Matières"
    titleLabel = Label(matieres, text=pagename, font=('Century Gothic', 30), bd=2, bg="#182029", foreground="#ffffff")
    titleLabel.place(x="250", y="25")

    codeLabel = Label(matieres, text="Code Matière :", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    nomLabel = Label(matieres, text="Libellé de la Matière :", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    coefLabel = Label(matieres, text="Coefficient :", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    codeLabel.place(x="50", y="100")
    nomLabel.place(x="50", y="200")
    coefLabel.place(x="50", y="300")

    entryCode = Entry(matieres, width=25, bd=2, font=('Century Gothic', 15))
    entryNom = Entry(matieres, width=25, bd=2, font=('Century Gothic', 15))
    entryCoef = Entry(matieres, width=25, bd=2, font=('Century Gothic', 15))
    entryCode.place(x="300", y="100")
    entryNom.place(x="300", y="200")
    entryCoef.place(x="300", y="300")

    boutonAjout = Button(
        matieres, text="➕Ajouter", padx=5, pady=5, width=10,
        font=('Century Gothic', 15), bg="#324254", command=insert_data
    )
    boutonAjout.place(x="50", y="400")

    boutonModifi = Button(
        matieres, text="⭕Modifier", padx=5, pady=5, width=10,
        font=('Century Gothic', 15), bg="#bbb441", command=update_data
    )
    boutonModifi.place(x="250", y="400")

    boutonSupp = Button(
        matieres, text="❌Supprimer", padx=5, pady=5, width=10,
        font=('Century Gothic', 15), bg="#af4747", command=delete_data
    )
    boutonSupp.place(x="450", y="400")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Century Gothic', 15))

    my_tree = ttk.Treeview(matieres)
    my_tree['column'] = ("Code", "Nom", "Coef")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Code", anchor=W, width=70)
    my_tree.column("Nom", anchor=W, width=200)
    my_tree.column("Coef", anchor=W, width=70)
    my_tree.heading("Code", text="Code", anchor=W)
    my_tree.heading("Nom", text="Libellé Matière", anchor=W)
    my_tree.heading("Coef", text="Coef", anchor=W)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', text="", values=result, tag="orow")

    my_tree.tag_configure('orow', background="#EEEEEE", font=('Century Gothic', 15))
    my_tree.place(x="650", y="100")

    projet = Label(
        matieres, text="Projet de Python",
        font=('Century Gothic', 15), bg="#182029", foreground="#FFFFFF"
    )
    projet.place(x='825', y='450')