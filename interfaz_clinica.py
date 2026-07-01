import tkinter as tk
from tkinter import ttk
import json

def mostrar_pacientes_ventana():
    for fila in tabla.get_children():
        tabla.delete(fila)

    pacientes = [
        {"nombre": "Luis", "edad": 8, "tratamiento": "Revision"},
        {"nombre": "Valentina", "edad": 6, "tratamiento": "Revision"},
        {"nombre": "Rafael", "edad": 4, "tratamiento": "Primera cita"},
        {"nombre": "Natalia", "edad": 37, "tratamiento": "Limpieza"},
    ]

    for paciente in pacientes:
        tabla.insert(
            "",
            tk.END,
            values=(
                paciente["nombre"],
                paciente["edad"],
                paciente["tratamiento"]
            )
        )
        
        

def cargar_pacientes_json():
    for fila in tabla.get_children():
        tabla.delete(fila)

    with open("pacientes.json", "r", encoding="utf-8") as archivo:
        pacientes = json.load(archivo)
    
    for paciente in pacientes:
        tabla.insert(
            "",
            tk.END,
            values=(
            paciente["nombre"],
            paciente["edad"],
            paciente["tratamiento"]
        )
    )

def guardar_pacientes_json():
    pacientes = []
    
    for fila in tabla.get_children():
        datos = tabla.item(fila, "values")

        paciente = {
            "nombre": datos[0],
            "edad": datos [1],
            "tratamiento": datos[2]
        }

        pacientes.append(paciente)

    with open("pacientes.json", "w", encoding="utf-8") as archivo:
        json.dump(pacientes, archivo, indent=4, ensure_ascii=False)

def eliminar_paciente():
    seleccion = tabla.selection()

    if len(seleccion) == 0:
        return

    for fila in seleccion:
        tabla.delete(fila)

    guardar_pacientes_json()

from modulos.pacientes import ver_pacientes, añadir_paciente, buscar_paciente



ventana = tk.Tk()
ventana.title("Gestión Clínica")
ventana.geometry("900x600")

titulo = tk.Label(
    ventana,
    text="Gestión Clínica",
    font=("Arial", 22)
)
titulo.pack(pady=20)
#caja_resultados = tk.Text(ventana, width=55, height=10)
#caja_resultados.pack(pady=10)

tabla = ttk.Treeview(
    ventana,
    columns=("Nombre", "Edad", "Tratamiento"),
    show="headings",
    height=8
)

tabla.heading("Nombre", text="Nombre")
tabla.heading("Edad", text="Edad")
tabla.heading("Tratamiento", text="Tratamiento")

tabla.column("Nombre", width=250, anchor="center")
tabla.column("Edad" , width=80, anchor="center")
tabla.column("Tratamiento", width=250, anchor="center")

tabla.pack(pady=20)

def abrir_ventana_añadir():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Añadir paciente")
    ventana_nueva.geometry("350x250")

    tk.Label(ventana_nueva, text="Nombre").pack()
    entrada_nombre = tk.Entry(ventana_nueva)
    entrada_nombre.pack(pady=5)

    tk.Label(ventana_nueva, text="Edad").pack()
    entrada_edad = tk.Entry(ventana_nueva)
    entrada_edad.pack(pady=5)

    tk.Label(ventana_nueva, text="Tratamiento").pack()
    entrada_tratamiento = tk.Entry(ventana_nueva)
    entrada_tratamiento.pack(pady=5)

    def guardar():
        nombre = entrada_nombre.get()
        edad = entrada_edad.get()
        tratamiento = entrada_tratamiento.get()

        tabla.insert(
            "",
            tk.END,
            values=(nombre, edad, tratamiento)
        )

        guardar_pacientes_json()
        ventana_nueva.destroy()
    
    tk.Button(
        ventana_nueva,
        text="Guardar paciente",
        command=guardar
    ).pack(pady=10)
    
boton_ver = tk.Button(
    ventana,
    text="Ver pacientes",
    width=25,
    command=mostrar_pacientes_ventana
)
boton_ver.pack(pady=10)

boton_añadir = tk.Button(
    ventana,
    text="Añadir paciente",
    width=25,
    command=abrir_ventana_añadir
)
boton_añadir.pack(pady=10)

boton_eliminar = tk.Button(
    ventana,
    text="Eliminar paciente",
    width=25,
    command=eliminar_paciente
)
boton_eliminar.pack(pady=10)


boton_buscar = tk.Button(
    ventana,
    text="Buscar paciente",
    width=25,
    command=buscar_paciente
)
boton_buscar.pack(pady=10)
boton_json = tk.Button(
    ventana,
    text="Cargar JSON",
    width=25,
command=cargar_pacientes_json
)

boton_json.pack(pady=10)


boton_salir = tk.Button(
    ventana,
    text="Salir",
    width=25,
    command=ventana.destroy
)
boton_salir.pack(pady=10)

def abrir_ficha_paciente(event=None):
    seleccion = tabla.selection()

    if len(seleccion) == 0:
        return
    
    datos = tabla.item(seleccion[0], "values")


    ventana_ficha = tk.Toplevel(ventana)
    ventana_ficha.title("Ficha del paciente")
    ventana_ficha.geometry("450x350")
        
    tk.Label(ventana_ficha, text="Nombre").pack()
    

    entry_nombre = tk.Entry(ventana_ficha, width=30)
    entry_nombre.insert(0, datos[0])
    entry_nombre.pack(pady=5)

    tk.Label(ventana_ficha, text="Edad"). pack()

    entry_edad = tk.Entry(ventana_ficha, width=30)
    entry_edad.insert(0, datos[1])
    entry_edad.pack(pady=5)

    tk.Label(ventana_ficha, text="Tratamiento").pack()

    entry_tratamiento = tk.Entry(ventana_ficha, width=30)
    entry_tratamiento.insert(0, datos[2])
    entry_tratamiento.pack(pady=5)

    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nueva_edad = entry_edad.get()
        nuevo_tratamiento = entry_tratamiento.get()

        tabla.item(
            seleccion[0],
            values=(nuevo_nombre, nueva_edad, nuevo_tratamiento)
            )
        guardar_pacientes_json()

        ventana_ficha.destroy()

    tk.Button(
        ventana_ficha,
        text="Guardar cambios",
        command=guardar_cambios
    ).pack(pady=15)

tabla.bind("<Double-1>", abrir_ficha_paciente)
ventana.mainloop()