import tkinter
#import customtkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.pdfgen.canvas import *
from reportlab.lib.colors import *
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import SimpleDocTemplate, Table

import os
import sys
import subprocess

def page_notes() :

    def choix() :
        etu = listeCombo.get()
        PDFPrint(etu)

    def PDFPrint(nom):
        canvas = Canvas("bulletin.pdf")
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(230, 770, 'BULLETIN DE NOTES')
        canvas.line(150, 760, 450, 760)

        canvas.drawString(30, 730, 'MATRICULE :')
        canvas.drawString(30, 695, "NOM ET PRENOM DE L'ETUDIANT :")
        canvas.drawString(30, 660, 'TELEPHONE :')

        #reccuperation des identifiant de l'étudiant
        ma_base_de_donnee = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password ="",
            database = "projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("SELECT * FROM etudiants WHERE Mat = {}".format(nom))
        for row in mon_curseur :
            canvas.drawString(300, 730, row[0])
            canvas.drawString(300, 695, row[1])
            canvas.drawString(300, 660, row[2])

        #tableau de notes
        canvas.line(0,  600, 650, 600)#position x, position y,taille et position z
        canvas.line(0, 550, 650, 554)
        canvas.drawString(20, 570, 'MATIERE')
        canvas.drawString(110, 570, 'COEFFICIENT')
        canvas.drawString(230, 570, 'PROJET')
        canvas.drawString(320, 570, 'DEVOIR')
        canvas.drawString(415, 570, 'EXAMEN')
        canvas.drawString(515, 570, 'MOYENNE')
        #reccuperation des identifiant des notes
        mes_notes = ma_base_de_donnee.cursor()
        mes_notes.execute("SELECT * FROM notes WHERE Matricule_Etudiant = {}".format(nom))
        row = mes_notes.fetchall()
        canvas.drawString(20, 480, str(row[0]))
        canvas.drawString(20, 430, str(row[1]))
        canvas.drawString(20, 390, str(row[2]))
        canvas.drawString(20, 330, str(row[3]))
        canvas.line(0, 150, 650, 155)
        #Le bas
        #Calcul de la moyenne générale
        moy   = 0
        scoef = 0
        moyenne_generale = 0
        calcul1 = ma_base_de_donnee.cursor()
        calcul1.execute("SELECT Moyenne FROM notes WHERE Matricule_Etudiant = {}".format(nom))
        for row in calcul1 :
            moy += float(row[0])
        calcul2 = ma_base_de_donnee.cursor()
        calcul2.execute("SELECT Coef FROM notes WHERE Matricule_Etudiant = {}".format(nom))
        for row in calcul2 :
            scoef += float(row[0])

        moyenne_generale = float(moy/scoef)

        canvas.drawString(30, 100, 'MOYENNE GENERALE :')
        canvas.drawString(200, 100, str(moyenne_generale))

        if moyenne_generale <= 9 :
            canvas.drawString(200, 50, 'MEDIOCRE')
        elif moyenne_generale <= 12 :
            canvas.drawString(200, 50, 'PASSABLE')
        elif moyenne_generale <= 14 :
            canvas.drawString(200, 50, 'ASSEZ BIEN')
        elif moyenne_generale <= 16 :
            canvas.drawString(200, 50, 'BIEN')
        elif moyenne_generale <= 18 :
            canvas.drawString(200, 50, 'TRES BIEN')
        else :
            canvas.drawString(200, 50, 'EXCELLENT')

        canvas.drawString(30, 50, 'MENTION :')
        canvas.drawString(250, 15, 'Copyright &copy; 2021 tout droit réservé')

        canvas.save()
        subprocess.Popen(['bulletin.pdf'], shell=True)



    def insert_data_base(): 
        ma_base_de_donnee = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projet"
        )
        mon_curseur = ma_base_de_donnee.cursor()
        mon_curseur.execute("""CREATE TABLE IF NOT EXISTS notes (
            Matricule_Etudiant VARCHAR(50),
            Nom_Matiere VARCHAR(100) , 
            Coef VARCHAR(50) , 
            Projet FLOAT ,
            Devoir FLOAT ,
            Examen FLOAT ,
            Moyenne FLOAT,
            FOREIGN KEY(Matricule_Etudiant) REFERENCES etudiants,
            FOREIGN KEY(Nom_Matiere) REFERENCES matieres)""")
        
        for i in LISTETABLEAU:
            mon_curseur.execute(
                "INSERT INTO notes VALUES('" + str(i[0]) + "','" + str(i[1]) + "','" + str(i[2]) + "','" + str(i[3]) + "','" + str(i[4]) + "','" + str(i[5]) + "','" + str(i[6]) + "')")
        ma_base_de_donnee.commit()


    def insert_data_tableau():

        rec_nomprenom=listeCombo.get()
        rec_matiere= listeCombo2.get()
        rec_coefficient = listeCombo3.get()
        rec_projet= entryProjet.get()
        rec_devoir= entryDevoir.get()
        rec_examen= entryExamen.get()
        rec_moyenne = moyenne_matiere()

        LISTETABLEAU.append([rec_nomprenom,rec_matiere,rec_coefficient,rec_projet,rec_devoir,rec_examen,rec_moyenne])
    
        tableau.insert('',END,values=LISTETABLEAU[-1])
        tableau.tag_configure('orow', background="#EEEEEE", font=('Century Gothic', 15))
        tableau.place(x="330",y="154")


    def delete_data():
        selected_item = tableau.selection()[0]
        tableau.delete(selected_item)
 

    projet  = DoubleVar()
    devoir  = DoubleVar()
    examen  = DoubleVar()
    moyenne = 0.0

    def moyenne_matiere() :
        Projet= float(entryProjet.get())
        Devoir = float(entryDevoir.get())
        Examen = float(entryExamen.get())
        Coefficient= float(listeCombo3.get())
        moyenne= ((Projet+Devoir+(Examen*2))*Coefficient)/4

        if (Projet<0 or  Projet>20) or (Devoir<0 or  Devoir>20) or (Examen<0 or  Examen>20) :
            message = "Les notes ne doivent pas dépasser 20 ou être en dessous de 0"
            messagebox.showerror("Erreur d'entrée !", message, parent = notes)
        else :
            moyenneLabel.config(text=moyenne)
       
        return moyenne

    notes = tkinter.Toplevel()
    notes.title("Menu des Notes")
    notes.geometry('1015x500')
    notes.resizable(height=False, width=False)
    notes['bg'] = '#182029'
    icon = PhotoImage(file='icone.png')
    notes.iconphoto(False, icon)
    pagename = "Enregistrement des Notes"
    titleLabel = Label(notes, text=pagename, font=('Century Gothic', 30), bd=2, bg="#182029", foreground="#ffffff")
    titleLabel.place(x="318", y="25")


    etuLabel = Label(notes, text="ETUDIANT ", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    etuLabel.place(x="30", y="30")

    matiereLabel = Label(notes, text="MATIERE ", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    matiereLabel.place(x="30", y="90")

    matiereLabel = Label(notes, text="COEF ", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    matiereLabel.place(x="30", y="150")

    projetLabel = Label(notes, text="PROJET ", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    projetLabel.place(x="30", y="210")

    devoirLabel = Label(notes, text="DEVOIR ", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    devoirLabel.place(x="30", y="270")

    examLabel = Label(notes, text="EXAMEN ", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    examLabel.place(x="30", y="330")

    moyLabel = Label(notes, text="MOYENNE ", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    moyLabel.place(x="30", y="390")

    LISTETABLEAU=[]


    def listefunc():
        ma_base_de_donnee = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="projet"
        )
        etudiant = ma_base_de_donnee.cursor()
        etudiant.execute("""CREATE TABLE IF NOT EXISTS etudiants(Mat VARCHAR(50) PRIMARY KEY, Nom_Prenom VARCHAR(100), Tel VARCHAR(150))""")
        etudiant.execute("SELECT Nom_Prenom FROM etudiants")
        data = []
        for row in etudiant.fetchall():
            data.append(row[0])
        return data
    listeCombo = ttk.Combobox(notes, font=("Century Gothic", 10), width=20)
    listeCombo['values'] = listefunc()
    listeCombo.place(x="138", y="34")

    def listefuncMat():
        ma_base_de_donnee = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="projet"
        )
        matiere = ma_base_de_donnee.cursor()
        matiere.execute("""CREATE TABLE IF NOT EXISTS matieres(Code VARCHAR(50) PRIMARY KEY, Nom_Matiere VARCHAR(100), Coef VARCHAR(50))""")
        matiere.execute("SELECT Nom_Matiere FROM matieres")
        data = []
        for row in matiere.fetchall():
            data.append(row[0])
        return data

    listeCombo2 = ttk.Combobox(notes, font=("Century Gothic", 10), width=20)

    listeCombo2['values'] = listefuncMat()
    
    listeCombo2.place(x="138", y="94")
    #listeCombo2.bind("<<ComboboxSelected>>", action)


    #combobox du coefficient
    def listefuncCoef():
        ma_base_de_donnee = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="projet"
        )
        coefficient = ma_base_de_donnee.cursor()
        coefficient.execute("""CREATE TABLE IF NOT EXISTS matieres(Code VARCHAR(50) PRIMARY KEY, Nom_Matiere VARCHAR(100), Coef VARCHAR(50))""")
        coefficient.execute("SELECT Coef FROM matieres")
        data = []
        for row in coefficient.fetchall():
            data.append(row[0])
        return data

    listeCombo3 = ttk.Combobox(notes, font=("Century Gothic", 10), width=20)
    liste3=[]
    for i in listefuncCoef():
        if i not in liste3:
            liste3.append(i)
    listeCombo3['values'] = liste3
    listeCombo3.place(x="138", y="154")


    #Création du tableau d'enregistrement des notes 
    enreLabel = Label(notes, text="Tableau des notes ", font=("Century Gothic", 15), bg="#182029", foreground="#ffffff")
    enreLabel.place(x="570", y="120")

    entryProjet  = Entry(notes, width=22, bd=2, font=('Century Gothic', 10), textvariable = projet)
    entryDevoir  = Entry(notes, width=22, bd=2, font=('Century Gothic', 10), textvariable = devoir)
    entryExamen  = Entry(notes, width=22, bd=2, font=('Century Gothic', 10), textvariable = examen)
    entryProjet.place(x="140", y="214")
    entryDevoir.place(x="140", y="274")
    entryExamen.place(x="140", y="334") 

    moyenneLabel = Label(notes, font=("Century Gothic", 15), bg="#fff", foreground="#000", width=13,text=entryProjet.get())
    moyenneLabel.place(x="140", y="390")

    boutonMoyenne = Button(
        notes, text="✍Calculer moyenne", padx=2, pady=2, width=17,
        font=('Century Gothic', 10), bg="olive", command=moyenne_matiere)
    boutonMoyenne.place(x="80", y="434")

    #tableau
    tableau = ttk.Treeview(notes, columns=('etudiant','matieres', 'coef', 'projet', 'devoir', 'exam', 'moyenne'))
    tableau.column("#0", width=0, stretch=NO)
    tableau.column("etudiant", anchor=W, width=130)
    tableau.column("matieres", anchor=W, width=90)
    tableau.column("coef", anchor=W, width=55)
    tableau.column("projet", anchor=W, width=60)
    tableau.column("devoir", anchor=W, width=75)
    tableau.column("exam", anchor=W, width=100)
    tableau.column("moyenne", anchor=W, width=150)

    tableau.heading('etudiant', text='Etudiant')
    
    tableau.heading('matieres', text='Matières')

    tableau.heading('coef', text='Coef')

    tableau.heading('projet', text='Projet')

    tableau.heading('devoir', text='Devoir')

    tableau.heading('exam', text='Examen')

    tableau.heading('moyenne', text='Moyenne')

    tableau.place(x="330",y="154")


    #boutons
    boutonAffiche = Button(
        notes, text="👁Afficher", padx=2, pady=2, width=10,
        font=('Century Gothic', 10), bg="gold", command=insert_data_tableau)
    boutonAffiche.place(x="400", y="400")

    boutonAjout = Button(
        notes, text="➕Ajouter", padx=2, pady=2, width=10,
        font=('Century Gothic', 10), bg="#324254",command=insert_data_base)
    boutonAjout.place(x="510", y="400")

    boutonSupprimer = Button(
        notes, text="❌Supprimer", padx=2, pady=2, width=10,
        font=('Century Gothic', 10), bg="#af4747",command=delete_data)
    boutonSupprimer.place(x="620", y="400")

    boutonBulletin = Button(
        notes, text="📚Générer bulletin", padx=2, pady=2, width=15,
        font=('Century Gothic', 10), bg="orange", command= choix)
    boutonBulletin.place(x="733", y="400")

    projet = Label(notes, text="Projet de Python",
        font=('Century Gothic', 15), bg="#182029", foreground="#FFFFFF"
    )
    projet.place(x='825', y='450')