import tkinter
import souspages.etudiant
import souspages.matiere
import souspages.note
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import ttk

w = Tk()

width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

w.overrideredirect(1)

s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
progress = Progressbar(w, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=500, mode='determinate', )


# progressbar
def new_win():
    fenetre = Tk()
    fenetre.title("Gestion des notes")
    fenetre.geometry('1150x500')
    fenetre.resizable(height=False, width=False)
    icon = PhotoImage(file='icon.png')
    fenetre.iconphoto(False, icon)
    photo = PhotoImage(file='background.png')
    label = Label(fenetre, image=photo)
    label.pack()

    mon_menu = Menu(fenetre)
    etudiant = Menu(mon_menu, tearoff=0)
    etudiant.add_command(label="Ajouter des étudiants", command=souspages.etudiant.page_etudiant)
    matieres = Menu(mon_menu, tearoff=0)
    matieres.add_command(label="Ajouter des Matieres", command=souspages.matiere.page_matieres)
    notes = Menu(mon_menu, tearoff=0)
    notes.add_command(label="Ajouter des notes", command=souspages.note.page_notes)
    mon_menu.add_cascade(label="Page des étudiants", menu=etudiant)
    mon_menu.add_cascade(label="Page des matières", menu=matieres)
    mon_menu.add_cascade(label="Page des notes", menu=notes)
    mon_menu.add_command(label="Quitter", command=exit)
    fenetre.config(menu=mon_menu)

    fenetre.mainloop()


def bar():
    l4 = Label(w, text='Chargement...', fg='white', bg=a)
    lst4 = ('Calibri (Body)', 10)
    l4.config(font=lst4)
    l4.place(x=18, y=210)

    import time
    r = 0
    for i in range(100):
        progress['value'] = r
        w.update_idletasks()
        time.sleep(0.03)
        r = r + 1

    w.destroy()
    new_win()


progress.place(x=-10, y=235)

# frame

a = '#182029'
Frame(w, width=427, height=241, bg=a).place(x=0, y=0)  # 249794
b1 = Button(w, width=25, height=1,font=('Century Gothic', 10), text='Cliquez pour lancer le logiciel', command=bar, border=0, fg=a, bg='white')
b1.place(x=215, y=210)

# Label

l1 = Label(w, text='GESTION', fg='white', bg=a)
lst1 = ('Calibri (Body)', 18, 'bold')
l1.config(font=lst1)
l1.place(x=50, y=80)

l2 = Label(w, text='des NOTES', fg='white', bg=a)
lst2 = ('Calibri (Body)', 18)
l2.config(font=lst2)
l2.place(x=170, y=82)

l3 = Label(w, text='Projet de Python', fg='white', bg=a)
lst3 = ('Calibri (Body)', 13)
l3.config(font=lst3)
l3.place(x=50, y=110)

w.mainloop()


