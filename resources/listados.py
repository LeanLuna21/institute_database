import sqlite3 as sq3
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd

# -------------- paleta --------------
color_fondo = 'SteelBlue1'
color_letra = 'black'
fondo_framebotones = 'RosyBrown2'
color_fondo_boton = 'black'
color_texto_boton = 'snow'
# --------------        ---------------
 
## estas funciones muestran los listados del menu superior ##

def listar_alumnos():
    con = sq3.connect("resources/Alas_test.db")
    cur = con.cursor()
    query = '''SELECT alumnos.legajo, alumnos.apellido, alumnos.nombre, alumnos.dni, alumnos.telefono, cursos.nombre, cursos.precio FROM alumnos INNER JOIN cursos ON alumnos.curso_id = cursos.curso_id ORDER BY alumnos.legajo'''

    result = cur.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = [ x[0] for x in result.description]

    # Create the window
    raiz2 = tk.Tk()
    raiz2.geometry('1250x500')
    raiz2.title("Alumnos x Curso")
    frame = tk.Frame(raiz2)
    frame.pack(fill='both', expand=True)

    # Create a Treeview with dual Scrollbars
    tree = ttk.Treeview(frame, show="headings", columns=df.columns[0:-1]) # -> este slicing saca la columna extra que me trae la tabla 
    hsb = tk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    vsb = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
    tree.grid(column=0, row=0, sticky=tk.NSEW)
    vsb.grid(column=1, row=0, sticky=tk.NS)
    hsb.grid(column=0, row=1, sticky=tk.EW)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    for i, header in enumerate(df.columns):
        tree.column(i, width=150, anchor='center')
        tree.heading(i, text=header.upper())
    for row in range(df.shape[0]):
        tree.insert('', 'end', values=list(df.iloc[row]))
    raiz2.mainloop()

def listar_cuotas():
    con = sq3.connect('resources/Alas_test.db')
    cur = con.cursor()  
    query = '''SELECT alumnos. apellido || ' ' || alumnos.nombre AS Alumno, cursos.nombre as 'curso', pagos.fotocs, pagos.March, pagos.April, pagos.May, pagos.June, pagos.July, pagos.August, pagos.September, pagos.October, pagos.November, pagos.December FROM pagos INNER JOIN alumnos INNER JOIN cursos ON pagos.legajo = alumnos.legajo AND pagos.curso_id = cursos.curso_id ORDER BY alumnos.apellido'''

    result = cur.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = [ x[0] for x in result.description]

    # Create the window
    win = tk.Tk()
    win.geometry('1250x500')
    win.title("Cuotas (alumnos)")
    frame = tk.Frame(win)
    frame.pack(fill='both', expand=True)

    # Create a Treeview with dual Scrollbars
    tree = ttk.Treeview(frame, show="headings", columns=df.columns[0:-1]) # -> este slicing saca la columna extra que me trae la tabla 

    hsb = tk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    vsb = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
    tree.grid(column=0, row=0, sticky=tk.NSEW)
    vsb.grid(column=1, row=0, sticky=tk.NS)
    hsb.grid(column=0, row=1, sticky=tk.EW)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    for i, header in enumerate(df.columns):
        tree.column(i, width=150, anchor='center')
        tree.heading(i, text=header.upper())
    for row in range(df.shape[0]):
        tree.insert('', 'end', values=list(df.iloc[row]))
        
    win.mainloop()

def listar_precios(): # habra que agregar horarios cuando los haya
    class Table:
        def __init__(self):
            nombre_columnas = ['CURSO', 'PRECIO']

            for i in range(cant_columnas):
                self.e = Entry(secondframe)
                self.e.config(bg="black", fg="snow")
                self.e.grid(row=0, column=i)
                self.e.insert(END, nombre_columnas[i])
                self.e.config(state="disabled")

            for fila in range(cant_filas):
                for col in range(cant_columnas):
                    self.e = Entry(secondframe)
                    self.e.grid(row=fila + 1, column=col)
                    self.e.insert(END, resultado[fila][col])
                    self.e.config(state="readonly")


    ###### segunda ventana iterfaz ######
    raiz2 = Tk()
    raiz2.title("Cursos y Precios")
    raiz2.resizable(False,False)
    # cuadros donde ira la info #
    secondframe = Frame(raiz2)
    secondframe.pack(fill="both")
    framecerrar = Frame(raiz2)
    framecerrar.config(bg=color_texto_boton)
    framecerrar.pack(fill="both")
    boton_cerrar = Button(framecerrar, text="Cerrar", command=raiz2.destroy)
    boton_cerrar.pack(fill="both")

    ##### segunda ventana funcional #####
    con = sq3.connect("resources/Alas_test.db")
    cur = con.cursor()
    query = 'SELECT nombre, precio FROM cursos ORDER BY curso_id '
    cur.execute(query)
    resultado = cur.fetchall()
    cant_filas = len(resultado)
    cant_columnas = len(resultado[0])

    tabla = Table()
    con.close()
    raiz2.mainloop()

def alumnos_x_curso(num):
    class Table:
        def __init__(self):
            nombre_columnas = ['CURSO','APELLIDO', 'NOMBRE','LEGAJO', 'DNI', 'TELEFONO', 'PRECIO']

            for i in range(cant_columnas):
                self.e = Entry(secondframe)
                self.e.config(bg="black", fg="snow")
                self.e.grid(row=0, column=i)
                self.e.insert(END, nombre_columnas[i])
                self.e.config(state="disabled")

            for fila in range(cant_filas):
                for col in range(cant_columnas):
                    self.e = Entry(secondframe)
                    self.e.grid(row=fila + 1, column=col)
                    self.e.insert(END, resultado[fila][col])
                    self.e.config(state="readonly")


    ###### segunda ventana iterfaz ######
    raiz2 = Tk()
    raiz2.title("Alumnos x curso")
    raiz2.resizable(False,False)
    
    # cuadros donde ira la info #
    secondframe = Frame(raiz2)
    secondframe.pack(fill="both")
    framecerrar = Frame(raiz2)
    framecerrar.config(bg=color_texto_boton)
    framecerrar.pack(fill="both")
    boton_cerrar = Button(framecerrar, text="Cerrar", command=raiz2.destroy)
    boton_cerrar.pack(fill="both")

    ##### segunda ventana funcional #####
    con = sq3.connect("resources/Alas_test.db")
    cur = con.cursor()
    
    cursos_disponibles = "SELECT nombre FROM cursos"
    cur.execute(cursos_disponibles)
    result = cur.fetchall()
    cursos = []
    for i in result:
        cursos.append(i[0])
    
    query = 'SELECT cursos.nombre, alumnos.apellido, alumnos.nombre, alumnos.legajo, alumnos.dni, alumnos.telefono, cursos.precio FROM alumnos INNER JOIN cursos ON alumnos.curso_id = cursos.curso_id  WHERE cursos.nombre LIKE '
    curso = cursos[num]
    query2 = ' ORDER BY alumnos.apellido'
    
    cur.execute(query+'"'+curso+'"'+query2)
    resultado = cur.fetchall()
    cant_filas = len(resultado)
    cant_columnas = len(resultado[0])

    tabla = Table()
    con.close()
    raiz2.mainloop()

def listar_pagos():
    con = sq3.connect('resources/Alas_test.db')
    cur = con.cursor()  
    # creamos la query para traer los datos a mostrar
    query = '''SELECT alumnos.apellido || ' ' || alumnos.nombre AS Alumno, cursos.nombre as 'curso', pagos.fotocs, pagos.March, pagos.April, pagos.May, pagos.June, pagos.July, pagos.August, pagos.September, pagos.October, pagos.November, pagos.December FROM pagos INNER JOIN alumnos INNER JOIN cursos ON pagos.legajo = alumnos.legajo AND pagos.curso_id = cursos.curso_id ORDER BY alumnos.apellido'''

    result = cur.execute(query)
    # creamos un dataframe para almacenar los resultados de la busqueda
    df = pd.DataFrame(result.fetchall())
    
    # asignamos la 1er fila del df como los nombres de las columnas 
    df.columns = [ x[0] for x in result.description]

    # Creamos la window
    win = tk.Tk()
    win.geometry('1250x500')

    my_label = Label(win, text="Filtrar por apelllido: ")
    my_label.pack()

    # creamos la variable para luego usarla para filtrar
    nombre = StringVar()
    my_entry = Entry(win, font=('fangsong ti',12),width=50, textvariable=nombre)
    my_entry.pack(padx=20)

    ##### Funcion que filtra el df y muestra el resultado que coincida; o muestra el df completo si no hay dato de entrada
    def filtrar():
        # traemos el apellido de la variable Entry()
        apellido = my_entry.get()
        # print ("apellido a buscar:", apellido)     
                
        # Verificar si la variable apellido está vacía
        if not apellido:
            # Si está vacía, mostrar el dataframe completo
            mostrar_df = df
        else:
            # Si contiene un valor, filtrar el dataframe 
            mostrar_df = df[df.Alumno.str.contains(apellido)]

        # print(mostrar_df)

        # Limpiar el treeview antes de agregar nuevas filas
        for item in tree.get_children():
            tree.delete(item)

        # Configurar columnas y encabezados
        for i, header in enumerate(mostrar_df.columns):
            tree.column(i, width=120, anchor='center')
            tree.heading(i, text=header.upper())

        # Insertar filas en el treeview
        for row in range(mostrar_df.shape[0]):
            tree.insert('', 'end', values=list(mostrar_df.iloc[row]))

        
    # este boton ejecutará el filtrado
    my_button = Button(win, text="Buscar",command=filtrar)
    my_button.pack()

    win.title("Cuotas (alumnos)")
    frame = tk.Frame(win)
    frame.pack(fill='both', expand=True)  

    # Creamos el Treeview con los Scrollbars
    tree = ttk.Treeview(frame, show="headings", columns=df.columns[0:-1]) # -> este slicing saca la columna extra que me trae la tabla 
    hsb = tk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    vsb = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
    tree.grid(column=0, row=0, sticky=tk.NSEW)
    vsb.grid(column=1, row=0, sticky=tk.NS)
    hsb.grid(column=0, row=1, sticky=tk.EW)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    #### INICIALMENTE se verá el df completo 

    # Insertar los nombres de las columnas
    for i, header in enumerate(df.columns):
        tree.column(i, width=120, anchor='center')
        tree.heading(i, text=header.upper())

    # Insertar filas en el treeview
    for row in range(df.shape[0]):
        tree.insert('', 'end', values=list(df.iloc[row]))
    
    win.mainloop()

