from tkinter import *
from PIL import Image, ImageTk
import sql
import mysql.connector as msq


# Ouverture de la connexion
# --------------------------------------------------------
config = {
    "user": "root",
    "password": "root",
    "host": "127.0.0.1",
    "port": "8081",
    "database": "trombinoscope",
}
db = msq.connect(**config)


# Création de l'interface
# --------------------------------------------------------
fenetre = Tk()
fenetre.title("Trombinoscope")

# Création des fonctions
# --------------------------------------------------------


def click_button():
    prenom, nom = find_person()
    path = get_path_image(prenom, nom)
    path = "./photos/" + path
    identite = get_identite(prenom, nom)
    change_content(path, identite)


def find_person():
    indice = user_list.curselection()  # retourne un indice
    print(indice)
    full_name = user_list.get(
        indice
    )  # retourne un string avec le prenom, nom de l'indice
    print(full_name)
    full_name = full_name.split(" ")
    prenom, nom = full_name
    return (prenom, nom)


def get_path_image(prenom, nom):
    """
    Retourne le chemin de l'image depuis la BDD
    """
    # Cursor sert à récupérer les données que l'on demande
    cursor = db.cursor()

    # Requêtes :
    query = (
        "SELECT photo FROM personnes WHERE nom = '"
        + nom
        + "' AND prenom = '"
        + prenom
        + "'"
    )
    cursor.execute(query)
    path = cursor.fetchone()  # retourne une ligne de la requête sous forme de tuple

    # Fermeture
    cursor.close()
    return path[0]


def get_identite(prenom, nom):
    """
    Retourne le nom, le prénom, le genre et le statut de la personne
    """
    # Cursor sert à récupérer les données que l'on demande
    cursor = db.cursor()

    # Requêtes :
    query = (
        "SELECT prenom, nom, qualification, libelle_genre FROM personnes NATURAL JOIN genres NATURAL JOIN statuts WHERE nom = '"
        + nom
        + "' AND prenom = '"
        + prenom
        + "'"
    )

    cursor.execute(query)
    libelle = cursor.fetchone()  # retourne une ligne de la requête sous forme de tuple

    # Fermeture
    cursor.close()
    return libelle


def change_content(path, libelle):
    # Changement de l'image dans le canvas
    img = Image.open(path)
    photo_resize = ImageTk.PhotoImage(img.resize((263, 350)))
    # photo.config(file=photo_resize)
    canvas.itemconfig(image_canvas, image=photo_resize)
    # Changement du texte dans le label
    name_label.config(text=libelle)
    canvas.mainloop()


def get_users_list(db):
    """
    Retourne tous les utilisateurs pour la ListBox
    """
    # Cursor sert à récuperer les données que l'on demande
    cursor = db.cursor()

    # Requêtes :
    query = "SELECT prenom, nom FROM personnes ORDER BY id_personne"

    cursor.execute(query)
    users = []
    for user in cursor:
        print(user)
        name = " ".join(user)
        users.append(name)

    # Fermeture
    cursor.close()
    return users


# Interface
# --------------------------------------------------------
# Element principal
main_layout = Frame(fenetre)
header = Label(
    main_layout,
    text="Ecole ISEN x SIMPLON \n Formation IA 2021/2022",
    fg="#161853",
    font="Noto 15",
    background="#FAEDF0",
    padx=15,
    pady=15,
)
central_widget = PanedWindow(main_layout, orient=HORIZONTAL)
# Placement du label header et central widget
header.pack(fill="x")
central_widget.pack(fill=BOTH)

# Element listes_users
sidebar = Frame(central_widget)
user_list = Listbox(sidebar, relief=FLAT)
button = Button(
    sidebar, text="Valider", fg="white", bg="#292C6D", relief=FLAT, command=click_button
)
user_list.pack(side=TOP, expand=10, fill=BOTH)
button.pack(fill="x")
# Insertion des personnes dans la ListBox en appelant la fonction get_users_list
user_list.insert(END, *get_users_list(db))


# Elément Content : photo & user
content = Frame(central_widget)
canvas = Canvas(content, width=350, height=350, bg="#FAEDF0")
photo = PhotoImage(file="avatar_h.png")
image_canvas = canvas.create_image(50, 0, anchor=NW, image=photo)
name_label = Label(
    content,
    text="Prénom Nom \n Statut Genre",
    fg="#161853",
    font="Noto 12",
    padx=10,
    pady=10,
    bg="#FAEDF0",
)
# Assemblage de la photo et du label
canvas.pack()
name_label.pack(fill="x")
content.pack(fill=BOTH)

# Assemblage
central_widget.add(sidebar)
central_widget.add(content)
# central_widget.pack()
main_layout.pack(fill=BOTH)


fenetre.mainloop()


# ----------------------------------------------------------
# Fermeture de la DB
db.close()
