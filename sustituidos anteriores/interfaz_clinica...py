import tkinter as tk
from tkinter import ttk, messagebox
import json
import sqlite3
from openpyxl import Workbook
import pacientes
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkinter import filedialog
from datetime import datetime 

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analisis_ia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT NOT NULL,
            fecha TEXT NOT NULL,
            sintomas TEXT NOT NULL,
            duracion TEXT,
            dolor INTEGER,
            antecedentes TEXT,
            fiebre INTEGER,
            inflamacion INTEGER,
            valoracion TEXT,
            prioridad TEXT,
            pruebas TEXT,
            alarmas TEXT,
            estado TEXT DEFAULT 'Pendiente'
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

def generar_informe():
    seleccionado = tabla.focus()

    if not seleccionado:
        messagebox.showwarning(
            "Aviso",
            "Selecciona un paciente primero"
        )
        return

    datos = tabla.item(seleccionado)["values"]

    nombre = datos[1]
    edad = datos[2]
    tratamiento = datos[3]
    proxima_cita = datos[4]

    informe = f"""
INFORME CLINICO

Paciente: {nombre}
Edad: {edad}

Tratamiento:
{tratamiento}

Próxima cita:
{proxima_cita}

Observaciones:
Paciente en seguimiento clínico.

Recomendación:
Continuar revisiones periódicas.


Generado por DentalAI Manager.
"""
    ventana_informe = tk.Toplevel(ventana)
    ventana_informe.title("Informe clínico")
    ventana_informe.geometry("600x500")

    texto = tk.Text(ventana_informe)
    texto.pack(fill="both", expand=True)

    texto.insert("1.0", informe)

    

    def guardar_pdf():
        ruta = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivo PDF", "*.pdf")],
            initialfile=f"informe_{nombre}.pdf" 
        )

        if not ruta:
            return
        pdf = canvas.Canvas(ruta, pagesize=A4)

        ancho, alto = A4
        margen = 60
        y = alto - 60

        fecha_actual = datetime.now().strftime("%d/%m/%y")

        pdf.setTitle(f"Informe clínico - {nombre}")

        #Título principal
        pdf.setFont("Helvetica-Bold",18)
        pdf.drawString(margen, y, "DENTALAI MANAGER")

        y -=25
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(margen, y, "INFORME CLÍNICO")

        # Línea separadora
        y-=12
        pdf.line(margen, y, ancho - margen, y)
        
        # Fecha 
        y -= 25
        pdf. setFont("Helvetica", 10)
        pdf.drawString(margen, y, f"Fecha: {fecha_actual}")

        # Datos del paciente
        y -=35
        pdf.setFont("Helvetica", 11)
        pdf.drawString(margen, y, "DATOS DEL PACIENTE")

        y -= 22
        pdf. setFont("Helvetica", 11)
        pdf.drawString(margen, y, f"Paciente: {nombre}")

        y-= 20
        pdf.drawString(margen, y, f"Edad: {edad} años")

        y-= 20
        pdf.drawString(margen, y, f"Próxima cita: {proxima_cita}")

        # Tratamiento
        y -= 35
        pdf. setFont("Helvetica-Bold", 11)
        pdf.drawString(margen, y, "TRATAMIENTO")

        y -= 22
        pdf. setFont("Helvetica", 11)
        pdf.drawString(margen, y, tratamiento)

        # Observaciones 
        y -= 35
        pdf. setFont("Helvetica-Bold", 11)
        pdf.drawString(margen, y, "OBSERVACIONES")

        y -= 22
        pdf. setFont("Helvetica", 11)
        pdf.drawString(margen, y, f"Paciente en seguimiento clínico.")

        # Recomendación
        y -= 35
        pdf. setFont("Helvetica-Bold", 11)
        pdf.drawString(margen, y, "RECOMENDACIÓN")

        y -= 22
        pdf. setFont("Helvetica", 11)
        pdf.drawString(margen, y, "Continuar revisiones periódicas.")

        #Pie de página
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.drawCentredString(
            ancho / 2,
            40,
            "Documento generado por DentalAI Manager"
        )
        pdf.save()



        messagebox.showinfo(
            "PDF guardado",
            "El informe se ha guardado correctamente."
        )

    boton_pdf = tk.Button(
        ventana_informe,
        text="Guardar informe en PDF",
        command=guardar_pdf
    )

    boton_pdf.pack(pady=10)

def abrir_analisis_ia():
    """Abre el copiloto clínico y permite guardar el análisis en SQLite."""
    ventana_analisis = tk.Toplevel(ventana)
    ventana_analisis.title("DentalAI Copilot")
    ventana_analisis.geometry("760x760")
    ventana_analisis.resizable(False, True)

    paciente_seleccionado = "Paciente no seleccionado"
    seleccion = tabla.selection()
    if seleccion:
        valores = tabla.item(seleccion[0], "values")
        if len(valores) > 1:
            paciente_seleccionado = str(valores[1])

    tk.Label(
        ventana_analisis,
        text="DentalAI Copilot",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=(15, 2))

    tk.Label(
        ventana_analisis,
        text=f"Paciente: {paciente_seleccionado}",
        font=("Segoe UI", 10, "bold")
    ).pack(pady=(0, 10))

    formulario = tk.Frame(ventana_analisis)
    formulario.pack(fill="x", padx=35)

    tk.Label(formulario, text="Síntomas principales").pack(anchor="w")
    entrada_sintomas = tk.Text(formulario, height=4, width=75, wrap="word")
    entrada_sintomas.pack(fill="x", pady=(2, 8))

    tk.Label(formulario, text="Duración de los síntomas").pack(anchor="w")
    entrada_duracion = tk.Entry(formulario, width=45)
    entrada_duracion.pack(anchor="w", pady=(2, 8))

    tk.Label(formulario, text="Dolor de 0 a 10").pack(anchor="w")
    entrada_dolor = tk.Entry(formulario, width=15)
    entrada_dolor.pack(anchor="w", pady=(2, 8))

    tk.Label(formulario, text="Antecedentes relevantes").pack(anchor="w")
    entrada_antecedentes = tk.Text(formulario, height=3, width=75, wrap="word")
    entrada_antecedentes.pack(fill="x", pady=(2, 8))

    opciones = tk.Frame(formulario)
    opciones.pack(anchor="w", pady=(0, 8))

    tiene_fiebre = tk.BooleanVar(value=False)
    tiene_inflamacion = tk.BooleanVar(value=False)

    tk.Checkbutton(opciones, text="Fiebre", variable=tiene_fiebre).pack(side="left", padx=(0, 15))
    tk.Checkbutton(opciones, text="Inflamación", variable=tiene_inflamacion).pack(side="left")

    resultado_ia = tk.Text(
        ventana_analisis,
        height=12,
        width=82,
        wrap="word",
        state="disabled"
    )
    resultado_ia.pack(fill="both", expand=True, padx=35, pady=(5, 10))

    ultimo_analisis = {
        "valoracion": "",
        "prioridad": "",
        "pruebas": "",
        "alarmas": ""
    }

    def mostrar_resultado(texto):
        resultado_ia.config(state="normal")
        resultado_ia.delete("1.0", "end")
        resultado_ia.insert("1.0", texto)
        resultado_ia.config(state="disabled")

    def analizar_caso():
        sintomas_originales = entrada_sintomas.get("1.0", "end").strip()
        sintomas = sintomas_originales.lower()
        duracion = entrada_duracion.get().strip()
        dolor = entrada_dolor.get().strip()
        antecedentes = entrada_antecedentes.get("1.0", "end").strip()

        if not sintomas_originales:
            messagebox.showwarning("Aviso", "Escribe primero los síntomas.")
            return

        if dolor and (not dolor.isdigit() or not 0 <= int(dolor) <= 10):
            messagebox.showwarning("Aviso", "El dolor debe ser un número entre 0 y 10.")
            return

        prioridad = "Baja"
        valoracion = "No se ha identificado una situación concreta con los datos aportados."
        pruebas = "Exploración clínica general."
        alarmas = "No se han detectado señales de alarma."
        informacion_faltante = []

        dolor_num = int(dolor) if dolor.isdigit() else None

        if tiene_fiebre.get() and tiene_inflamacion.get():
            prioridad = "Urgente"
            valoracion = "Posible proceso infeccioso odontógeno."
            pruebas = "Exploración clínica prioritaria y radiografía diagnóstica."
            alarmas = "Fiebre e inflamación. Valorar atención urgente si existe inflamación facial o dificultad para tragar."
        elif tiene_inflamacion.get() and dolor_num is not None and dolor_num >= 7:
            prioridad = "Alta"
            valoracion = "Dolor intenso acompañado de inflamación. Requiere valoración prioritaria."
            pruebas = "Exploración clínica y radiografía diagnóstica."
            alarmas = "Dolor intenso e inflamación."
        elif "dolor" in sintomas and dolor_num is not None and dolor_num >= 7:
            prioridad = "Alta"
            valoracion = "Dolor dental intenso que requiere valoración prioritaria."
            pruebas = "Exploración clínica y radiografía diagnóstica."
            alarmas = "Dolor intenso."
        elif "sangrado" in sintomas:
            prioridad = "Media"
            valoracion = "Posibles signos de inflamación gingival o periodontal."
            pruebas = "Valoración periodontal y revisión de higiene oral."
        elif "sensibilidad" in sintomas:
            prioridad = "Media"
            valoracion = "Posible hipersensibilidad dental."
            pruebas = "Exploración clínica y valoración de desgaste, retracción o caries."
        elif "caries" in sintomas:
            prioridad = "Media"
            valoracion = "Posible lesión de caries."
            pruebas = "Exploración clínica y radiografía si procede."
        elif "sarro" in sintomas or "placa" in sintomas:
            prioridad = "Baja"
            valoracion = "Posible acumulación de placa o cálculo dental."
            pruebas = "Valoración periodontal e higiene profesional."

        if not duracion:
            informacion_faltante.append("duración de los síntomas")
        if dolor_num is None:
            informacion_faltante.append("intensidad del dolor")
        if not antecedentes:
            informacion_faltante.append("antecedentes relevantes")

        faltante = ", ".join(informacion_faltante).capitalize() if informacion_faltante else "Ninguna."

        ultimo_analisis.update({
            "valoracion": valoracion,
            "prioridad": prioridad,
            "pruebas": pruebas,
            "alarmas": alarmas
        })

        resultado = f"""ANÁLISIS CLÍNICO ORIENTATIVO

Paciente:
{paciente_seleccionado}

Valoración:
{valoracion}

Prioridad:
{prioridad}

Pruebas sugeridas:
{pruebas}

Señales de alarma:
{alarmas}

Información pendiente:
{faltante}

Antecedentes:
{antecedentes if antecedentes else 'No indicados'}

Aviso:
Resultado orientativo. Requiere validación profesional.
"""
        mostrar_resultado(resultado)

    def guardar_analisis():
        sintomas = entrada_sintomas.get("1.0", "end").strip()
        duracion = entrada_duracion.get().strip()
        dolor = entrada_dolor.get().strip()
        antecedentes = entrada_antecedentes.get("1.0", "end").strip()

        if not sintomas:
            messagebox.showwarning("Aviso", "Escribe primero los síntomas.")
            return

        if not ultimo_analisis["prioridad"]:
            messagebox.showwarning("Aviso", "Analiza primero el caso.")
            return

        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO analisis_ia (
                paciente, fecha, sintomas, duracion, dolor,
                antecedentes, fiebre, inflamacion, valoracion,
                prioridad, pruebas, alarmas, estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            paciente_seleccionado,
            datetime.now().strftime("%d/%m/%Y %H:%M"),
            sintomas,
            duracion,
            int(dolor) if dolor.isdigit() else None,
            antecedentes,
            int(tiene_fiebre.get()),
            int(tiene_inflamacion.get()),
            ultimo_analisis["valoracion"],
            ultimo_analisis["prioridad"],
            ultimo_analisis["pruebas"],
            ultimo_analisis["alarmas"],
            "Pendiente"
        ))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Análisis guardado", "El análisis se ha guardado correctamente.")

    frame_acciones = tk.Frame(ventana_analisis)
    frame_acciones.pack(pady=(0, 15))

    tk.Button(
        frame_acciones,
        text="Analizar caso",
        width=22,
        command=analizar_caso
    ).pack(side="left", padx=6)

    tk.Button(
        frame_acciones,
        text="Guardar análisis",
        width=22,
        command=guardar_analisis
    ).pack(side="left", padx=6)


def abrir_historial_ia():
    """Muestra los análisis guardados y permite validarlos o rechazarlos."""
    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial de análisis IA")
    ventana_historial.geometry("1050x600")

    tk.Label(
        ventana_historial,
        text="Historial de análisis IA",
        font=("Segoe UI", 17, "bold")
    ).pack(pady=12)

    columnas = ("ID", "Paciente", "Fecha", "Prioridad", "Estado")
    historial = ttk.Treeview(ventana_historial, columns=columnas, show="headings", height=15)

    anchos = {"ID": 55, "Paciente": 220, "Fecha": 160, "Prioridad": 100, "Estado": 120}
    for columna in columnas:
        historial.heading(columna, text=columna)
        historial.column(columna, width=anchos[columna], anchor="center")

    historial.pack(fill="both", expand=True, padx=20, pady=8)

    def cargar_historial():
        historial.delete(*historial.get_children())
        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, paciente, fecha, prioridad, estado
            FROM analisis_ia
            ORDER BY id DESC
        """)
        registros = cursor.fetchall()
        conexion.close()
        for registro in registros:
            historial.insert("", "end", values=registro)

    def obtener_id_seleccionado():
        seleccion = historial.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un análisis.")
            return None
        return historial.item(seleccion[0], "values")[0]

    def cambiar_estado(nuevo_estado):
        id_analisis = obtener_id_seleccionado()
        if id_analisis is None:
            return
        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE analisis_ia SET estado=? WHERE id=?",
            (nuevo_estado, id_analisis)
        )
        conexion.commit()
        conexion.close()
        cargar_historial()

    def ver_detalle():
        id_analisis = obtener_id_seleccionado()
        if id_analisis is None:
            return

        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT paciente, fecha, sintomas, duracion, dolor, antecedentes,
                   fiebre, inflamacion, valoracion, prioridad, pruebas, alarmas, estado
            FROM analisis_ia
            WHERE id=?
        """, (id_analisis,))
        registro = cursor.fetchone()
        conexion.close()

        if not registro:
            messagebox.showerror("Error", "No se ha encontrado el análisis.")
            return

        detalle = tk.Toplevel(ventana_historial)
        detalle.title(f"Detalle análisis #{id_analisis}")
        detalle.geometry("720x620")

        campos = [
            ("Paciente", registro[0]),
            ("Fecha", registro[1]),
            ("Síntomas", registro[2]),
            ("Duración", registro[3] or "No indicada"),
            ("Dolor", registro[4] if registro[4] is not None else "No indicado"),
            ("Antecedentes", registro[5] or "No indicados"),
            ("Fiebre", "Sí" if registro[6] else "No"),
            ("Inflamación", "Sí" if registro[7] else "No"),
            ("Valoración", registro[8]),
            ("Prioridad", registro[9]),
            ("Pruebas sugeridas", registro[10]),
            ("Señales de alarma", registro[11]),
            ("Estado", registro[12])
        ]

        texto = tk.Text(detalle, wrap="word", padx=15, pady=15)
        texto.pack(fill="both", expand=True)
        for etiqueta, valor in campos:
            texto.insert("end", f"{etiqueta}:\n{valor}\n\n")
        texto.config(state="disabled")

    acciones = tk.Frame(ventana_historial)
    acciones.pack(pady=10)

    tk.Button(acciones, text="Ver detalle", width=18, command=ver_detalle).pack(side="left", padx=5)
    tk.Button(acciones, text="Validar", width=18, command=lambda: cambiar_estado("Validado")).pack(side="left", padx=5)
    tk.Button(acciones, text="Rechazar", width=18, command=lambda: cambiar_estado("Rechazado")).pack(side="left", padx=5)
    tk.Button(acciones, text="Actualizar", width=18, command=cargar_historial).pack(side="left", padx=5)

    historial.bind("<Double-1>", lambda event: ver_detalle())
    cargar_historial()

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
    messagebox.showinfo(
        "Excel",
        "Archivo pacientes.xlsx creado correctamente."
    )
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
    text="DentalAI Copilot",
    width=35,
    command=abrir_analisis_ia
)
boton_ia.pack(pady=3)

boton_historial_ia = tk.Button(
    ventana,
    text="Historial IA",
    width=35,
    command=abrir_historial_ia
)
boton_historial_ia.pack(pady=3)









def mostrar_estadisticas():
    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM pacientes")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(edad) FROM pacientes")
    edad_media = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE edad < 18")
    menores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE edad >= 18")
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

boton_informe = tk.Button(
        ventana,
        text="Generar informe clinico",
        width=35,
        command=generar_informe
    )
boton_informe.pack(pady=3)

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