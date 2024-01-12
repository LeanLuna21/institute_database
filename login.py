import sqlite3 as sq3
from tkinter import *
from tkinter import messagebox

# --- paleta de colores --- #
color_fondo = 'cornflower blue'
alternative_color = 'dodger blue'
color_letra = 'black'
color_letra_alternativo = 'seashell'
fuente = ('Myanmar text', 15,'bold')  # (font_family, font_size_in_pixel, font_weight) ->> .configure (font = fuente )
fuente_alt = ('Bahnschrift Light',14)
# --- paleta de colores --- #

# fx de login - solo accede si username y password coinciden con lo almacenado
def login():
    username = "florencia"
    password = "2106"
    if username_entry.get()==username and password_entry.get()==password:
        messagebox.showinfo(title="Login Successful!", message="You successfully logged in.")
        # si coincide lo ingresado por teclado, cerramos esta ventana de login
        window.destroy()
        
        # y LA SEGUNDA VENTANA de interfaz se abre
        import main
    else:
        messagebox.showerror(title="Error", message="Invalid login.")  

    # window.destroy()
                
def main_screen():
    global username_entry
    global password_entry
    global window
    # creamos un objeto de tipo ventana
    window = Tk()
    window.title("Cultural Inglesa Alas - Log in Page")
    window.geometry('650x450')
    window.config(bg='RoyalBlue2', border=3)
    window.resizable(False,False)
    
    # creamos el frame para el contenido
    frame = Frame(bg='RoyalBlue2')
    
    # creamos las etiquetas para la interfaz y recuperacion de datos
    login_label = Label(frame, text="Welcome!", bg=alternative_color, fg='black', font=('Myanmar text',20,'bold'),height=2, width=5,  highlightthickness=2)
    username_label = Label(frame, text="Username:", bg= 'RoyalBlue2', fg='snow', font=fuente, padx=30)
    password_label = Label(frame, text="Password:", bg= 'RoyalBlue2', fg='snow', font=fuente, padx=30)
    username_entry = Entry(frame, font=fuente_alt)
    password_entry = Entry(frame, show="*", font=fuente_alt)
    login_button = Button(frame, text="Login", bg=alternative_color, fg='black', font=("Arial", 16,'bold'), command=login)

    # para mostrar en pantalla las etiquetas necesito darles una ubicacion
    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=45)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    frame.pack(expand=1)
    window.mainloop()

if __name__ == '__main__':  
    main_screen()

