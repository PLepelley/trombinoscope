from tkinter import *

fenetre= Tk()
fenetre.title('Trombinoscope')


def get_users():
    liste=['Perrine', 'Mina', 'Sacha']
    return liste


#PanedWindow
main_layout = PanedWindow(fenetre, orient=VERTICAL)
header = Label(main_layout, text='Ecole Formation IA')
central_widget = PanedWindow(main_layout, orient=HORIZONTAL)
main_layout.add(header)
main_layout.add(central_widget)

#Premier Element 
sidebar = PanedWindow(central_widget, orient=VERTICAL)
teacher_list = Listbox(sidebar)
student_list = Listbox(sidebar)
sidebar.add(teacher_list)
sidebar.add(student_list)
#sidebar.pack()
teacher_list.insert(END, *get_users())

#Deuxième élément
content = PanedWindow(central_widget, orient=VERTICAL)
canvas = Canvas(content, width=350, height=350, background="#F5EEDC")
photo = PhotoImage(file="avatar_h.png")
canvas.create_image(0,0, anchor=NW, image=photo)
name_label = Label(content, text='Nom Prénom')
content.add(canvas)
content.add(name_label)
#content.pack()

#Troisème élément
central_widget.add(sidebar)
central_widget.add(content)
#central_widget.pack()
main_layout.pack()





fenetre.mainloop()