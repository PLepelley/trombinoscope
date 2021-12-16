from tkinter import *
import sql
import mysql.connector as msq


# Ouverture de la connexion
config = {
    "user": "root",
    "password": "root",
    "host": "127.0.0.1",
    "port": "8081",
    "database": "trombinoscope",
}
db = msq.connect(**config)


# Création Interface
# --------------------------------------------------------
fenetre = Tk()
fenetre.title("Trombinoscope")

# Création des fonctions
# --------------------------------------------------------


def click_button():
    prenom, nom = find_person()
    path = get_path_image(prenom, nom)
    path = path.replace("jpg", "png")
    path = "./photo_resize/" + path
    change_photo(path)
    identite = get_identite(prenom, nom)
    change_label(identite)


def find_person() -> tuple:
    indice = user_list.curselection()
    full_name = user_list.get(indice)
    full_name = full_name.split(" ")
    prenom, nom = full_name
    return (prenom, nom)


def get_path_image(prenom: str, nom: str) -> str:
    """
    Retourne le chemin de l'image depuis la BDD
    """
    # Cursor sert à récuperer les données que l'on demande
    cursor = db.cursor()

    # Requêtes : SELECT nom, prenom FROM utilisateurs WHERE id_utilisateur = 1
    query = (
        "SELECT photo FROM personnes WHERE nom = '"
        + nom
        + "' AND prenom = '"
        + prenom
        + "'"
    )
    cursor.execute(query)
    path = cursor.fetchone()

    # Fermeture
    cursor.close()
    return path[0]


def change_photo(path: str):
    photo.config(file=path)


def get_identite(prenom: str, nom: str) -> tuple:
    """
    Retourne l'identité de la personne
    """
    # Cursor sert à récuperer les données que l'on demande
    cursor = db.cursor()

    # Requêtes : SELECT nom, prenom FROM utilisateurs WHERE id_utilisateur = 1
    query = (
        "SELECT prenom, nom, qualification, libelle_genre FROM personnes NATURAL JOIN genres NATURAL JOIN statuts WHERE nom = '"
        + nom
        + "' AND prenom = '"
        + prenom
        + "'"
    )

    cursor.execute(query)
    libelle = cursor.fetchone()

    # Fermeture
    cursor.close()
    return libelle


def change_label(libelle: tuple):
    name_label.config(text=libelle)


# --------------------------------------------------------
# PanedWindow
# Element principal
main_layout = Frame(fenetre)
header = Label(
    main_layout,
    text="Ecole ISEN x SIMPLON \n Formation IA",
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

user_list.insert(END, *sql.get_users_list(db))
# user_list.bind("<<ListboxSelect>>", lambda x: click_button())

# Elément Content : photo & user
content = Frame(central_widget)
canvas = Canvas(content, width=350, height=350, bg="#FAEDF0")
photo = PhotoImage(file="avatar_h.png")
canvas.create_image(0, 0, anchor=NW, image=photo)
name_label = Label(
    content,
    text="Nom Prénom",
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
