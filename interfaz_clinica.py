import tkinter as tk
from tkinter import ttk, messagebox
import json
import sqlite3
from openpyxl import Workbook
import pacientes
from tkinter import messagebox

def crear_base_datos():
    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            tratamiento TEXT NOT NULL,
            proxima_cita TEXT
        )
    """)

    conexion.commit()
    conexion.close()

def mostrar_pacientes_ventana():
    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, nombre, edad, tratamiento, proxima_cita
    FROM pacientes
    ORDER BY id ASC
    """)

    pacientes = cursor.fetchall()

    conexion.close()

    for paciente in pacientes:
        tabla.insert(
            "",
            tk.END,
            values=paciente
            )
        
    actualizar_contador()
        

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
            paciente["tratamiento"],
            paciente.get("proxima_cita", "")
        )
    )
    actualizar_contador()

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

def filtrar_pacientes(event=None):

    texto = entrada_busqueda.get().lower()

    for fila in tabla.get_children():
        tabla.delete(fila)

    with open("pacientes.json", "r", encoding="utf-8") as archivo:
        pacientes = json.load(archivo)
    
    for paciente in pacientes:

        if texto in paciente["nombre"].lower():

            tabla.insert(
                "",
                tk.END,
                values=(
                    paciente["nombre"],
                    paciente["edad"],
                    paciente["tratamiento"]
                )
            )   

    actualizar_contador()


def eliminar_paciente():
    seleccion = tabla.selection()

    if len(seleccion) == 0:
        return
    
    respuesta = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Está seguro de que desea eliminar el paciente seleccionado?"
    )

    if not respuesta:
        return

    for fila in seleccion:
        valores = tabla.item(fila, "values")
        id_paciente = valores[0]

        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM pacientes WHERE id=?",
            (id_paciente,)
        )

        conexion.commit()
        conexion.close()

        tabla.delete(fila)

    
    actualizar_contador()

from modulos.pacientes import modificar_paciente, ver_pacientes, añadir_paciente, buscar_paciente



ventana = tk.Tk()
ventana.title("Gestión Clínica")
ventana.geometry("1200x900")

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

menu_archivo.add_command(label="Salir", command=ventana.destroy)

titulo = tk.Label(
    ventana,
    text="DentalAI Manager",
    font=("Segoe UI", 20, "bold")
)
titulo.pack(pady=10)

subtitulo = tk.Label(
    ventana,
    text="Gestión clínica + IA dental",
    font=("Segoe UI", 11)
)
subtitulo.pack()


contador_pacientes = tk.Label(
    ventana,
    text="Pacientes registrados: 0",
    font=("Segoe UI", 10, "bold")
)

contador_pacientes.pack(pady=5)

tk.Label(
    ventana,
    text="Gestión clínica inteligente",
    font=("Segoe UI", 10)
).pack()

#caja_resultados = tk.Text(ventana, width=55, height=10)
#caja_resultados.pack(pady=10)

tk.Label(
    ventana,
    text="Buscar paciente",
).pack()

entrada_busqueda = tk.Entry(ventana, width=40)
entrada_busqueda.pack(pady=5)
entrada_busqueda.bind("<KeyRelease>", filtrar_pacientes)

tabla = ttk.Treeview(
    ventana,
    columns=("ID", "Nombre", "Edad", "Tratamiento", "Próxima cita"),
    show="headings"
)

orden_ascendente = True

def ordenar_por_nombre():
    global orden_ascendente

    filas = []

    for fila in tabla.get_children():
        datos = tabla.item(fila, "values")
        filas.append(datos)

    filas.sort(
        key=lambda paciente: paciente[1]. lower(),
        reverse=not orden_ascendente
    )
    for fila in tabla.get_children():
        tabla.delete(fila)

    for paciente in filas:
        tabla.insert(
            "",
            tk.END,
            values=paciente
        )

    orden_ascendente = not orden_ascendente


tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre", command=ordenar_por_nombre)
tabla.heading("Edad", text="Edad")
tabla.heading("Tratamiento", text="Tratamiento")

tabla.heading("Próxima cita", text="Próxima cita")
              
tabla.column("ID", width=40, anchor="center")
tabla.column("Nombre", width=250, anchor="center")
tabla.column("Edad" , width=80, anchor="center")
tabla.column("Tratamiento", width=250, anchor="center")

tabla.column("Próxima cita", width=120, anchor="center")

tabla.pack(pady=20)

def actualizar_contador():
    total = len(tabla.get_children())
    contador_pacientes.config(
        text=f"Pacientes registrados: {total}"
    )



def abrir_ventana_añadir():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Añadir paciente")
    ventana_nueva.geometry("350x350")

    tk.Label(ventana_nueva, text="Nombre").pack()
    entrada_nombre = tk.Entry(ventana_nueva)
    entrada_nombre.pack(pady=5)

    tk.Label(ventana_nueva, text="Edad").pack()
    entrada_edad = tk.Entry(ventana_nueva)
    entrada_edad.pack(pady=5)

    tk.Label(ventana_nueva, text="Tratamiento").pack()
    entrada_tratamiento = tk.Entry(ventana_nueva)
    entrada_tratamiento.pack(pady=5)

    tk.Label(ventana_nueva, text="Proxima cita").pack()
    entrada_proxima_cita = tk.Entry(ventana_nueva)
    entrada_proxima_cita.pack(pady=5)


    def guardar():
        nombre = entrada_nombre.get()
        edad = entrada_edad.get()
        tratamiento = entrada_tratamiento.get()
        proxima_cita = entrada_proxima_cita.get()

        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO pacientes (nombre, edad, tratamiento, proxima_cita)
            VALUES (?, ?, ?, ?)
        """, (nombre, edad, tratamiento, proxima_cita))

        conexion.commit()
        conexion.close()

        mostrar_pacientes_ventana()
        actualizar_contador()
        ventana_nueva.destroy()

    boton_guardar = tk.Button(
            ventana_nueva,
            text="Guardar",
            width=20,
            command=guardar
    )
    boton_guardar.pack(pady=10)   

        #tabla.insert(
            #"",
            #tk.END,
            #values=(nombre, edad, tratamiento, proxima_cita)
        #)
        #actualizar_contador()

        #guardar_pacientes_json()
        #ventana_nueva.destroy()
    
def exportar_a_excel():
    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT nombre, edad, tratamiento, proxima_cita
        FROM pacientes
        ORDER BY nombre
    """)

    pacientes = cursor.fetchall()
    conexion.close()

    libro_excel = Workbook()
    hoja = libro_excel.active
    hoja.title = "Pacientes"

    hoja.append(["Nombre", "Edad", "Tratamiento", "Próxima cita"])

    for paciente in pacientes:
        hoja.append(paciente)

        libro_excel.save("pacientes.xlsx")
        #messagebox.showinfo(
            #"Excel",
            #"Archivo pacientes.xlsx creado correctamente"
        #mostrar_pacientes_ventana()
        #actualizar_contador()

        
        #)
        #messagebox.showinfo(
            #"Exportación a completada",
            #"Archivo pacientes.xlsx creado correctamente"
        #)
def modificar_paciente():
    seleccionado = tabla.focus()

    if not seleccionado:
        messagebox.showwarning(
            "Aviso",
            "Seleccione un paciente para modificar"
        )
        return
    abrir_ficha_paciente(None)

def abrir_asistente_ia():
    ventana_ia = tk.Toplevel(ventana)
    ventana_ia.title("Asistente IA Dental")
    ventana_ia.geometry("600x400")

    tk.Label(
        ventana_ia,
        text="Describe los sintomas:"
    ).pack(pady=10)

    texto_sintomas = tk.Text(
        ventana_ia,
        width=60,
        height=8
    )
    texto_sintomas.pack(pady=10)

    resultado = tk.Label(
        ventana_ia,
        text="",
        wraplength=500,
        justify="left"
    )
    resultado.pack(pady=20)

    def analizar():
        sintomas = texto_sintomas.get("1.0", tk.END).lower()
        color ="black"

        if "caries" in sintomas and "profunda" in sintomas:
            recomendado = (
                "Valoración orientativa:\n"
                "Posible caries profunda.\n\n"
                "Tratamiento sugerido:\n"
                "-Radiografía periapical\n"
                "-Valoración de endodoncia\n\n"
                "Prioridad: Alta"
            )
            color = "red"

        elif "dolor" in sintomas and (
            "inflamación" in sintomas or "inflamación" in sintomas
            ):
                recomendado = (
                    "Valoración orientatica:\n"
                    "Posible proceso inflamatorio.\n\n"
                    "Prioridad: Urgente"
                )
                color = "darkred"

        elif "caries" in sintomas and "dolor" in sintomas:
           recomendado = (
               "Valoración orientatica:\n"
               "Posible lesión de caries con afectación pulpar.\n\n"
               "Tratamiento sugerido:\n"
               "-Radiografía diagnóstica\n"
               "-Obturación o valoración de endodoncia\n\n"
               "Prioridad: Alta\n\n"
               "Recomendación:\n"
               "Solicitar valoración odontológica lo antes posible."
           )
           color = "orange"

        elif "caries" in sintomas:
            recomendado = (
                "Valoración orientativa:\n"
                "Posible lesión de caries.\n\n"
                "Tratamiento sugerido:\n"
                "-Exploración clínica\n"
                "-Obturación si procede\n\n"
                "Prioridad: Media"
            )

        elif "sarro" in sintomas or "placa" in sintomas:
            recomendado = (
                "Valoración orientativa:\n"
                "Acumulación de placa o cálculo dental.\n\n"
                "Tratamiento sugerido:\n"
                "-Limpieza dental profesional\n"
                "- Revisión periodontal\n\n"
                "Prioridad: Baja"
            )
            color = "green"

        elif "sangrado" in sintomas:
            recomendado = (
                "Valoración orientativa:\n"
                "Posibles signos de inflamación gingival.\n\n"
                "Traramiento sugerido:\n"
                "-Valoración periodontal\n"
                "-Higiene profesional\n\n"
                "Prioridad: Media"
            )
        elif "dolor" in sintomas:
            recomendado = (
                "Valoración orientativa:\n"
                "El dolor dental puede tener distintas causas.\n\n"
                "Tratamiento sugerido:\n"
                "-Exploración clínica\n"
                "-Radiografía diagnóstica \n\n"
                "Prioridad: Alta"
            )
        elif "sensibilidad" in sintomas:
            recomendado =(
            "Valoración orientativa:\n"
            "Posible hipersensibilidad dental.\n\n"
            "Tratamiento sugerido:\n"
            "-Revisión clínica\n"
            "-Valoración de desgaste, retracción o caries \n\n"
            "Prioridad: Media"
        )
        
        else:
            recomendado = (
            "No se ha podido determinar un tratamiento específico.\n\n"
            "Se recomienda revision clinica."
        )

        resultado.config(
            text=recomendado,
            fg=color
        )

    tk.Button(
        ventana_ia,
        text="Analizar",
        width=20,
        command=analizar
    ).pack(pady=10)


    
boton_ver = tk.Button(
    ventana,
    text="Ver pacientes",
    width=35,
    command=mostrar_pacientes_ventana
)
boton_ver.pack(pady=3)

boton_añadir = tk.Button(
    ventana,
    text="Añadir paciente",
    width=35,
    command=abrir_ventana_añadir
)
boton_añadir.pack(pady=3)

boton_modificar = tk.Button(
    ventana,
    text="Modificar paciente",
    width=35,
    command=modificar_paciente
)
boton_modificar.pack(pady=3)



boton_eliminar = tk.Button(
    ventana,
    text="Eliminar paciente",
    width=35,
    command=eliminar_paciente
)
boton_eliminar.pack(pady=3)

boton_excel = tk.Button(
    ventana,
    text="Exportar a Excel",
    width=35,
    command=exportar_a_excel
)
boton_excel.pack(pady=3)

boton_json = tk.Button(
    ventana,
    text="Cargar JSON",
    width=35,
command=cargar_pacientes_json
)

boton_json.pack(pady=3)

boton_ia = tk.Button(
    ventana,
    text="Asistente IA Dental",
    width=35,
    command=abrir_asistente_ia
)
boton_ia.pack(pady=3)







def mostrar_estadisticas():
    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM pacientes")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(edad) FROM pacientes")
    edad_media = cursor.fetchone()[0]

    cursor.execute("SELECT tratamiento, COUNT(*) FROM pacientes WHERE edad < 18")
    menores = cursor.fetchone()[0]

    cursor.execute("SELECT tratamiento, COUNT(*) FROM pacientes WHERE edad >= 18")
    mayores = cursor.fetchone()[0]
                   
    cursor.execute("SELECT tratamiento, COUNT(*) AS cantidad FROM pacientes GROUP BY tratamiento ORDER BY cantidad DESC LIMIT 1")


    tratamiento_frecuente = cursor.fetchone()
    conexion.close()

    texto = f"Pacientes registrados {total}\n"
    texto += f"Edad promedio: {edad_media:.1f}\n"

    texto += f"\nMenores de edad: {menores}\n"
    texto += f"Mayores de edad: {mayores}\n\n"

    if tratamiento_frecuente:
        texto += f"Tratamiento más frecuente: {tratamiento_frecuente[0]}"
    else: 
        texto +="No hay tratamientos registrados"

    messagebox.showinfo("Estadísticas", texto)

boton_estadisticas = tk.Button(
    ventana,
    text="Mostrar estadísticas",
    width=35,
    command=mostrar_estadisticas
)
boton_estadisticas.pack(pady=3)

boton_salir = tk.Button(
    ventana,
    text="Salir",
    width=35,
    command=ventana.destroy
)
boton_salir.pack(pady=3)




       
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
    entry_nombre.insert(0, datos[1])
    entry_nombre.pack(pady=5)

    tk.Label(ventana_ficha, text="Edad"). pack()

    entry_edad = tk.Entry(ventana_ficha, width=30)
    entry_edad.insert(0, datos[2])
    entry_edad.pack(pady=5)

    tk.Label(ventana_ficha, text="Tratamiento").pack()

    entry_tratamiento = tk.Entry(ventana_ficha, width=30)
    entry_tratamiento.insert(0, datos[3])
    entry_tratamiento.pack(pady=5)

    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nueva_edad = entry_edad.get()
        nuevo_tratamiento = entry_tratamiento.get()
        id_paciente = datos[0]

        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()

        cursor.execute(
            "UPDATE pacientes SET nombre=?, edad=?, tratamiento=? WHERE id=?",
            (
                nuevo_nombre,
                nueva_edad,
                nuevo_tratamiento,
                id_paciente
            )
        )

        conexion.commit()
        conexion.close()
        mostrar_pacientes_ventana()
        actualizar_contador()

        ventana_ficha.destroy()

    tk.Button(
        ventana_ficha,
        text="Guardar cambios",
        command=guardar_cambios
    ).pack(pady=15)

tabla.bind("<Double-1>", abrir_ficha_paciente)

crear_base_datos()

mostrar_pacientes_ventana()

ventana.mainloop()