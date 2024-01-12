import sqlite3 as sq3
from tkinter import *
from tkinter import messagebox
import datetime
from resources.listados import listar_alumnos,listar_cuotas,listar_precios, listar_pagos, alumnos_x_curso
from invoice import convert_to_pdf

con = sq3.connect("resources/Alas_test.db")
cur = con.cursor()

# --- paleta de colores --- #
color_fondo = "cornflower blue"
alternative_color = "dodger blue"
color_letra = "black"
color_letra_alternativo = "seashell"
fuente = ("Myanmar text",14,"bold")  # (font_family, font_size_in_pixel, font_weight) ->> .configure (font = fuente )
fuente_botones = ("Myanmar text", 12, "bold")
fondo_framebotones = "RosyBrown2"
color_fondo_boton = "black"
color_texto_boton = "snow"
# --- paleta de colores --- #


##################################################################
######################## FUNCIONES VARIAS ########################
##################################################################

def mostrar_mes_actual():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    return month

def buscar_curso(actualiza):
    if actualiza:
        cur.execute("SELECT curso_id FROM cursos WHERE nombre = ?", (curso.get(),))
    else:
        cur.execute("SELECT nombre FROM cursos")

    resultado = cur.fetchall()
    course = []
    for i in resultado:
        if actualiza:
            co = i[0]  # id del curso esta en la posicion 0
            course.append(co)
        else:
            course.append(i[0])
    return course

def mostrar_total():
    precio_mes = int(importe.get())
    precio_deudas = int(deudas.get())
    precio_fotocs = int(fotocs.get())
    cuenta_total = precio_mes + precio_deudas + precio_fotocs
    total.set(cuenta_total)
    return cuenta_total

def imprimir_recibo():
    imprimir_legajo = legajo.get()
    imprimir_apellido = apellido.get()
    imprimir_nombre = nombre.get()
    imprimir_mes = mes.get()
    imprimir_importe = importe.get()
    imprimir_deudas = deudas.get()
    imprimir_fotocs =  fotocs.get()

    convert_to_pdf(imprimir_legajo,imprimir_apellido,imprimir_nombre,imprimir_mes,imprimir_importe,imprimir_deudas,imprimir_fotocs)


##################################################################
#################### FUNCIONES DE MENU ARRIBA ####################
##################################################################

# funciones de info de licencia y desarrollador
def licencia():
    messagebox.showinfo(
        "LICENCIA",
        """Sistema CRUD en Python
Copyright (C) 2023 - LeaLuna215
Email: lea21luna@gmail.com\n=======================================
This program is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any 
later version.
This program is distributed in the hope that it will be 
useful, but WITHOUT ANY WARRANTY; without even the 
implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE.  See the GNU General Public License 
for more details.
You should have received a copy of the GNU General Public 
License along with this program.  
If not, see <https://www.gnu.org/licenses/>.""",
    )

def acerca():
    messagebox.showinfo(
        "ACERCA DE...",
        "Creado por Leandro Gastón Luna [2023] - All rights reserved TM\n\nContacto: \nEmail: lea21luna@gmail.com\nTel: 1166781404",
    )

##################################################################
################### FUNCIONES DE BOTONES ABAJO ###################
##################################################################

# fx para buscar a un alumno (por legajo)  
def buscar_registro():
    if legajo.get() == "":
        messagebox.showerror("ERROR", "Por favor introduzca un número de legajo!")
    else:
        # armamos la query con los datos a traer apellido, nombre, dni, telefono, y curso
        query = "SELECT alumnos.apellido, alumnos.nombre, alumnos.dni, alumnos.telefono, cursos.nombre FROM alumnos INNER JOIN cursos ON alumnos.curso_id = cursos.curso_id WHERE alumnos.legajo ="
        # usamos .capitalize() para que el usuario no necesite preocuparse por las mayusculas
        cur.execute(query + legajo.get())

        # fetcheamos lo consultado a la BBDD
        resultado = cur.fetchall()
        # si esta vacio mostramos que el registro es inexistente
        if resultado == []:
            messagebox.showerror("ERROR", "Registro Inexistente.")
        # si recupero datos seteamos los campos del crud con dichos datos
        else:
            for campo in resultado:
                apellido.set(campo[0])
                nombre.set(campo[1])
                dni.set(campo[2])
                telefono.set(campo[3])
                curso.set(campo[4])
                legajo_input.config(state="disabled")

# fx para agregar alumno a la BBDD
def agregar_registro(): 
    alumno = legajo.get()
    if alumno == '':
        messagebox.showerror('Error','Introduzca un número de legajo.')
    else:
        # checkeamos primero si el legajo ya existe - traemos los legajos de la BBDD
        query = "SELECT legajo FROM alumnos"
        cur.execute(query)
        result = (cur.fetchall())  # esto devuelve una tupla de tuplas >>> ((1000,), (1001,), (1002,))
        # es necesesario desempaquetarlas -> podemos usar un list comprehension para eso >>> x[0]=(1000) , x[1]=(,)
        if int(legajo.get()) in [x[0] for x in result]:
            messagebox.showwarning("ATENCION!", "N° de legajo YA existente!")
        else:
            id_curso = int(buscar_curso(True)[0])
            datos = (
                legajo.get(),
                apellido.get(),
                nombre.get(),
                dni.get(),
                telefono.get(),
                id_curso,
            )
            cur.execute("INSERT INTO alumnos (legajo,apellido,nombre,dni,telefono,curso_id) VALUES (?,?,?,?,?,?)",(datos),)
            
            # debemos agregar a la tabla "pagos" el nuevo registro con los valores correspondientes
            cur.execute("INSERT INTO pagos (legajo,curso_id,fotocs, January, February, March, April, May, June, July, August, September, October, November, December) VALUES (?,?,0,0,0,0,0,0,0,0,0,0,0,0,0)",((legajo.get()),(id_curso)),)
            
            # guardamos el nro de legajo
            nro_legajo = datos[0]
            
            # traemos el precio de las fotocopias
            cur.execute("SELECT fotocs FROM pagos LIMIT 1")
            resultado = cur.fetchall()
            precio_fotocs = resultado[0][0]
            # updateamos el precio en el nuevo registro agregado
            cur.execute("UPDATE pagos SET fotocs = "+str(precio_fotocs)+" WHERE legajo = "+nro_legajo)
            
            # traemos el precio del mes de la tabla de cursos
            cur.execute("SELECT precio FROM cursos WHERE curso_id = "+str(id_curso))
            resultado = cur.fetchall()
            precio_curso = resultado[0][0]

            # creamos la iteracion para cambiar los valores de las columnas de la tabla pagos
            columnas_meses = ["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            indice = 0
            while indice < len(columnas_meses):    
                # seteamos los valores de las columnas (con cada iteracion)
                query = "UPDATE pagos SET "+columnas_meses[indice]+" = "+str(precio_curso)+" WHERE legajo = "+nro_legajo 
                cur.execute(query)
                indice += 1
                
            con.commit()
            messagebox.showinfo("STATUS", "Registro añadido con éxito!")
            limpiar_pantalla()

# fx para actualizar datos de un registro
def actualizar_registro():
    alumno = legajo.get()
    if alumno == '':
        messagebox.showerror('Error','Introduzca un número de legajo.')
    else:
        resp = messagebox.askquestion(
            "CONFIRMACION", "¿Esta seguro que desea modificar este registro?"
        )
        if resp == "yes":
            id_curso = int(buscar_curso(True)[0])
            datos = apellido.get(), nombre.get(), dni.get(), telefono.get(), id_curso
            cur.execute(
                "UPDATE alumnos SET apellido = ?, nombre = ?, dni = ?, telefono = ?, curso_id = ? WHERE legajo ="
                + legajo.get(),
                datos,
            )

            # traemos el precio del mes de la tabla de cursos
            cur.execute("SELECT precio FROM cursos WHERE curso_id = "+str(id_curso))
            resultado = cur.fetchall()
            precio_curso = resultado[0][0]

            # creamos la iteracion para cambiar los valores de las columnas de la tabla pagos
            columnas_meses = ["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            indice = 0
            while indice < len(columnas_meses):    
                # seteamos los valores de las columnas (con cada iteracion)
                cur.execute("UPDATE pagos SET "+columnas_meses[indice]+" = "+str(precio_curso)+" WHERE legajo = "+ legajo.get(),)
                indice += 1

            con.commit()
            messagebox.showinfo("STATUS", "Registro actualizado con exito!")
    limpiar_pantalla()

# fx para eliminar un registro de la BBDD
def eliminar_registro():
    alumno = legajo.get()
    if alumno == '':
        messagebox.showerror('Error','Introduzca un número de legajo.')
    else:
        resp = messagebox.askquestion(
            "CONFIRMACION", "¿Esta seguro que desea eliminar el registro?"
        )
        if resp == "yes":
            query = "DELETE FROM alumnos WHERE legajo ="
            query2 = "DELETE FROM pagos WHERE legajo ="
            cur.execute(query + legajo.get())
            cur.execute(query2 + legajo.get())
            
            con.commit()
            messagebox.showinfo("STATUS", "Registro eliminado!")
    limpiar_pantalla()

# fx que limpia los campos input de la app
def limpiar_pantalla(pagos=False):
    if pagos:
        importe.set(0)
        deudas.set(0)
        fotocs.set(0)
        total.set(0)
    else:
        legajo_input.config(state="normal")
        legajo.set("")
        apellido.set("")
        nombre.set("")
        dni.set("")
        telefono.set("")
        curso.set("  Seleccione... ")
        mes.set(mostrar_mes_actual())
        # mes_input.config(state="disabled")
        importe.set(0)
        deudas.set(0)
        fotocs.set(0)
        total.set(0)

# con la fx cobrar traemos el pago de fotocopias, el monto del mes corriente y el monto adeudado
def cobrar():
    nro_legajo = legajo.get()
    nombre_mes = mes.get()
    # seleccionamos el monto de fotocopias y el monto del mes actual
    query = 'SELECT pagos.fotocs, pagos.'+nombre_mes+' FROM pagos INNER JOIN alumnos ON pagos.curso_id = alumnos.curso_id WHERE alumnos.legajo='+nro_legajo+' GROUP BY alumnos.legajo'
    cur.execute(query)
    data = cur.fetchall() # esto siempre trae una lista de tuplas
    # asignamos cada valor de la tupla (fotocs,monto_mes) a los campos en el GUI
    fotocs.set(data[0][0])
    importe.set(data[0][1])

    # para las deudas creamos un diccionario que representa cada mes del año y le asignamos un valor
    # ese valor lo usaremos luego para hacer un slicing de los valores de la tupla que nos devuelve el query
    meses = {'January': 0, 'February': 1,'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6, 'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11}

    # traemos todos los montos del año
    query2 = 'SELECT "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" FROM pagos WHERE legajo ='+nro_legajo
    cur.execute(query2)
    data = cur.fetchall()

    # usando slicing reducimos la tupla solo hasta el mes corriente(almacenado en nombre_mes)
    # esa variable, a su vez es la clave del valor numerico que representa el fin del slicing
    cuenta_deudas = data[0][:meses[nombre_mes]]
    # sumamos los valores de la tupla ya partida
    cuenta_deudas = sum(cuenta_deudas)
    # se lo asignamos al campo deudas del GUI
    deudas.set(cuenta_deudas)    

    total.set(mostrar_total())

def pagar():
    pagar_mes()
    pagar_fotocs()
    pagar_deudas()
    limpiar_pantalla(True) #pasamos True para que la fx borre solo los campos de los pagos

def pagar_mes():
    nro_legajo = legajo.get() 
    importe_mes = importe.get()
    nombre_mes = mes.get()

    query = "SELECT "+nombre_mes+" FROM pagos WHERE legajo ="+nro_legajo
    cur.execute(query)
    result = cur.fetchall()
    monto = result[0][0]

    if monto >= importe_mes:
        # actualizamos el monto en la BBDD
        new_query = "UPDATE pagos SET "+nombre_mes+" = "+nombre_mes+" - "+str(importe_mes)+" WHERE legajo ="+nro_legajo+" AND "+nombre_mes+" > 0" 
        cur.execute(new_query)
        con.commit()
    else:
        # sino mostramos mje de error, ya que el monto es mayor.
        messagebox.showerror("ERROR",f"El monto introducido en el campo 'Fotocs' (${importe_mes}) supera el monto a deducir: ${monto}.")

def pagar_fotocs():
    nro_legajo = legajo.get() 
    importe_fotocs = fotocs.get()

    # recuperamos el monto que deberia pagar el alumno
    query = "SELECT fotocs FROM pagos WHERE legajo ="+nro_legajo
    cur.execute(query)
    result = cur.fetchall()
    monto = result[0][0]

    # si el monto es mayor a lo que yo quiero cobrarle o igual
    if monto >= importe_fotocs:
        # actualizamos el monto en la BBDD
        new_query = "UPDATE pagos SET fotocs = fotocs - "+str(importe_fotocs)+" WHERE legajo ="+nro_legajo+" AND fotocs > 0" 
        cur.execute(new_query)
        con.commit()
    else:
        # sino mostramos mje de error, ya que el monto es mayor.
        messagebox.showerror("ERROR",f"El monto introducido en el campo 'Fotocs' (${importe_fotocs}) supera el monto a deducir: ${monto}.")

def pagar_deudas():
    nro_legajo = legajo.get() 
    nombre_mes = mes.get()
    importe_deudas = deudas.get()

    meses = {'March': 0, 'April': 1,'May': 2, 'June': 3, 'July': 4, 'August': 5, 'September': 6, 'October': 7, 'November': 8, 'December': 9 }

    query = 'SELECT "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" FROM pagos WHERE legajo ='+nro_legajo
    cur.execute(query)
    data = cur.fetchall()

    # traemos el total adeudado
    cuenta_deudas = data[0][:meses[nombre_mes]]
    cuenta_deudas = sum(cuenta_deudas)
    
    # contamos la cantidad de meses adeudados para luego dividirlo
    cantidad_meses_adeudados = len(data[0][:meses[nombre_mes]])

    # dividimos el total por los meses para actualizar la bbdd
    cantidad_a_descontar = cuenta_deudas/cantidad_meses_adeudados

    columnas_meses = ["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    indice = 0

    # si el importe indicado es mayor al saldo adeudado, mostrar error
    if importe_deudas >  cuenta_deudas:
        messagebox.showerror("ERROR",f"El monto introducido en el campo 'deudas' (${importe_deudas}) supera el monto a deducir: ${cuenta_deudas}.")
    else:
        # sino, mientras que el importe adeudado sea mayor a la cantidad a descontar
        while importe_deudas >= cantidad_a_descontar:
            # modificamos los campos de los meses en la bbdd
            query = "UPDATE pagos SET "+columnas_meses[indice]+" = 0 WHERE legajo = "+nro_legajo 
            cur.execute(query)
            con.commit()
            # restamos la cantidad de cada iteracion del importe total para que no sea infinito
            importe_deudas -= cantidad_a_descontar
            # y sumamos la variable indice para ir corriendonos de columna en la bbdd
            indice += 1

        # cuando el importe adeudado sea menor a la cantidad en la iteracion
        if importe_deudas < cantidad_a_descontar:
            # restamos esa cantidad restante del ultimo mes en el que nos hallamos quedado al iterar
            query = "UPDATE pagos SET "+columnas_meses[indice]+" = "+columnas_meses[indice]+" - "+ str(importe_deudas)+" WHERE legajo = "+nro_legajo 
            cur.execute(query)
            con.commit()
    

##################################################################
######################## INTERFAZ GRAFICA ########################
##################################################################

window = Tk()
window.title("Cultural Inglesa Alas")
window.geometry("1050x700")
window.resizable(False, False)  # hace imposible cambiar el tamaño de la ventana

# creamos la barra de menu
main_menu = Menu(window)
window.config(menu=main_menu, border=2, bg="snow")
# window.overrideredirect(1) -> para eliminar los bordes

# creamos los menu desplegables:
# menu alumnos contiene el listado completo de alumnos y de cuotas abonadas de los alumnos
menu_alumnos = Menu(main_menu, tearoff=0, relief="raised")
menu_alumnos.add_command(label="Listado de alumnos", command=listar_alumnos)
menu_alumnos.add_command(label="Cuotas",command=listar_cuotas)
menu_alumnos.add_command(label="Pagos",command=listar_pagos)

# menu cursos contiene los precios y los alumnos por curso
menu_cursos = Menu(main_menu, tearoff=0)
menu_cursos.add_command(label="Precios y Horarios", command=listar_precios)
# creamos un sub-menu para acceder a cada curso
menu_cursos2 = Menu(menu_cursos, tearoff=0)
menu_cursos2.add_command(label="Preparatory",command=lambda: alumnos_x_curso(0))
menu_cursos2.add_command(label="Kids",command=lambda: alumnos_x_curso(1))
menu_cursos2.add_command(label="Junior",command=lambda: alumnos_x_curso(2))
menu_cursos2.add_command(label="Starter",command=lambda: alumnos_x_curso(3))
menu_cursos2.add_command(label="Beginner",command=lambda: alumnos_x_curso(4))
menu_cursos2.add_command(label="Elementary",command=lambda: alumnos_x_curso(5))
menu_cursos2.add_command(label="Pre-Intermediate",command=lambda: alumnos_x_curso(6))
menu_cursos2.add_command(label="Teens",command=lambda: alumnos_x_curso(7))
menu_cursos2.add_command(label="Intermediate",command=lambda: alumnos_x_curso(8))
menu_cursos2.add_command(label="Upper-Intermediate",command=lambda: alumnos_x_curso(9))

# menu que contiene info sobre el desarrollador
menu_acerca = Menu(main_menu, tearoff=0)
menu_acerca.add_command(label="Licencia", command=licencia)
menu_acerca.add_command(label="Acerca del Creador", command=acerca)

# agregamos todos los menu creados en forma de cascada a estos labels
main_menu.add_cascade(label="Alumnos", menu=menu_alumnos)
main_menu.add_cascade(label="Cursos", menu=menu_cursos)
menu_cursos.add_cascade(label="Alumnos x Curso", menu=menu_cursos2)
main_menu.add_cascade(label="+Info", menu=menu_acerca)

#### creamos el frame de arriba
# QUIZA SAQUEMOS ESTO
frametop = Frame(window)
frametop.config(bg=alternative_color, width=500, height=40)
frametop.pack(fill="both")

#### frame para los campos con data
framecampos = Frame(window)
framecampos.config(
    bg=color_fondo, width=500, height=50
)  # relief='sunken',bd=5 -> hundido hacia adentro y borde
framecampos.pack(
    fill="both", expand=1
)  # expand= expande el frame para rellenar el espacio


### creamos una fx para configurar los labels
def labels_config(mi_label, ncol, nfila):
    labels_location = {"ipady": 20, "pady": 5, "padx": 20, "sticky": "e"}
    labels_color = {"borderwidth": 2, "bg": color_fondo, "fg": "black", "font": ("Myanmar text", 16, "bold")}  # o'fg':color_letra_alternativo, 'font': fuente
    mi_label.grid(row=nfila, column=ncol, **labels_location)
    mi_label.config(**labels_color)

    
### creamos los labels que se veran en pantalla
legajo_label = Label(framecampos, text="Legajo n°")
labels_config(legajo_label, 0, 0)
apellido_label = Label(framecampos, text="Apellido")
labels_config(apellido_label, 0, 1)
nombre_label = Label(framecampos, text="Nombre")
labels_config(nombre_label, 0, 2)
dni_label = Label(framecampos, text="DNI")
labels_config(dni_label, 0, 3)
telefono_label = Label(framecampos, text="Telefono")
labels_config(telefono_label, 0, 4)
curso_label = Label(framecampos, text="Curso")
labels_config(curso_label, 0, 5)
### estos son los labels para las columnas del costado
mes_label = Label(framecampos, text="Mes corriente:")
labels_config(mes_label, 2, 0)
importe_label = Label(framecampos, text="Importe:")
labels_config(importe_label, 2, 1)
debe_label = Label(framecampos, text="Debe:")
labels_config(debe_label, 2, 2)
fotoc_label = Label(framecampos, text="Fotocs:")
labels_config(fotoc_label, 2, 3)
total_label = Label(framecampos, text="Total:")
labels_config(total_label, 2, 4)

boton_cobrar = Button(framecampos, text='COBRAR',command=cobrar)

boton_cobrar.grid(row=5, column=3, **{"ipady": 0, "pady":0,'padx':15,"ipadx": 40, 'sticky':'w'})
boton_cobrar.config(width=4, anchor='center',**{"font": ("Myanmar text", 12, "bold")})

boton_pagar = Button(framecampos, text='PAGAR', command=pagar)

boton_pagar.grid(row=5, column=3, **{"ipady": 0, "pady": 0,'padx':15,"ipadx": 40, 'sticky':'e'})
boton_pagar.config(width=4,anchor='center',**{"font": ("Myanmar text", 12, "bold")})

#Import the image using PhotoImage function
total_btn= PhotoImage(file='resources/facturas/calc.png')
resized_total = total_btn.subsample(5,5)
boton_imprimir = Button(framecampos, image=resized_total, command=mostrar_total)
boton_imprimir.grid(row=4,column=4,sticky="w")
boton_pagar.config(width=2)

#Import the image using PhotoImage function
click_btn= PhotoImage(file='resources/facturas/printer.png')
resized_img = click_btn.subsample(5,5)
boton_imprimir = Button(framecampos, image=resized_img, command=imprimir_recibo)
boton_imprimir.grid(row=5,column=4,sticky="w")
boton_pagar.config(width=2)


### creamos una fx para configurar los inputs
def inputs_config(mi_input, ncol, nfila):
    inputs_location = {"padx": 35, "pady": 8, "ipadx": 20}
    mi_input.grid(column=ncol, row=nfila, **inputs_location)
    mi_input.config(font=("Myanmar text", 13))


### creamos los inputs donde el usuario va a interactuar
## primero necesitamos los datos que va a manejar
legajo = StringVar()
apellido = StringVar()
nombre = StringVar()
dni = IntVar()
telefono = StringVar()
curso = StringVar()
mes = StringVar()
importe = IntVar()
deudas = IntVar()
fotocs = IntVar()
total = IntVar()

legajo_input = Entry(framecampos, textvariable=legajo)
inputs_config(legajo_input, 1, 0)
apellido_input = Entry(framecampos, textvariable=apellido)
inputs_config(apellido_input, 1, 1)
nombre_input = Entry(framecampos, textvariable=nombre)
inputs_config(nombre_input, 1, 2)
dni_input = Entry(framecampos, textvariable=dni)
inputs_config(dni_input, 1, 3)
telefono_input = Entry(framecampos, textvariable=telefono)
inputs_config(telefono_input, 1, 4)
# creamos el desplegable con los cursos
cursos = buscar_curso(False)
curso_opciones = OptionMenu(framecampos, curso, *cursos)
curso_opciones.grid(column=1, row=5, padx=10, pady=15, ipadx=20)
# inputs de la 4ta col
mes_input = Entry(framecampos, textvariable=mes)
inputs_config(mes_input, 3, 0)
importe_input = Entry(framecampos, textvariable=importe)
inputs_config(importe_input,3,1)
deudas_input = Entry(framecampos, textvariable=deudas)
inputs_config(deudas_input, 3, 2)
fotocs_input = Entry(framecampos, textvariable=fotocs)
inputs_config(fotocs_input, 3, 3)
total_input = Entry(framecampos, textvariable=total)
inputs_config(total_input, 3, 4)

#### frame para los botones de abajo
framebotones = Frame(window)
framebotones.config(bg=alternative_color, width=200, height=90)
framebotones.pack(fill="both")


def config_botones(mi_boton, columna):
    espaciado_botones = {"row": 0, "padx": 27, "pady": 10, "ipadx": 35, "ipady": 10}
    mi_boton.config(bg="snow", fg="black", font=25)
    mi_boton.grid(column=columna, **espaciado_botones)


# RECORDAR AGREGAR COMMAND= AL BOTON CON LA FX QUE CUMPLEN
boton_buscar = Button(framebotones, text="Buscar", command=buscar_registro)
config_botones(boton_buscar, 0)

boton_crear = Button(framebotones, text="Agregar", command=agregar_registro)
config_botones(boton_crear, 1)

boton_actualizar = Button(framebotones, text="Actualizar", command=actualizar_registro)
config_botones(boton_actualizar, 2)

boton_eliminar = Button(framebotones, text="Eliminar", command=eliminar_registro)
config_botones(boton_eliminar, 3)

boton_limpiar = Button(framebotones, text="Limpiar", command=limpiar_pantalla)
config_botones(boton_limpiar, 4)


limpiar_pantalla()

window.mainloop()
# fin programa

