import json
import os
import sqlite3

if os.path.exists("pacientes.json"):
    with open("pacientes.json", "r") as archivo:
        pacientes = json.load(archivo)
else:
    pacientes = [
    {"nombre": "Natalia", "edad": 37, "tratamiento": "Limpieza"},
    {"nombre": "Luis", "edad": 6, "tratamiento": "Revisión"},
    {"nombre": "Valentina", "edad": 9, "tratamiento": "Ortodoncia"},
    {"nombre": "Rafael", "edad": 4, "tratamiento": "Obturación"}
]
    
def ver_pacientes():

    conexion = sqlite3. connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM pacientes
    """)

    resultado = cursor.fetchall()

    for paciente in resultado:
            print("ID:", paciente[0])
            print("Nombre:", paciente[1])
            print("Edad:", paciente[2])
            print("Tratamiento:", paciente[3])
            print("---")   

    conexion.close()

def buscar_paciente():
    
    nombre_buscado = input("Nombre del paciente: ")

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM pacientes
    WHERE nombre = ?
    """, (nombre_buscado,))

    resultado = cursor.fetchall()

    for paciente in resultado:
        print( "Nombre:", paciente[1])
        print("Edad:", paciente[2])
        print("Tratamiento:", paciente[3])
        print("-----")
    
    conexion.close()

def añadir_paciente():

    nombre = input("Nombre: ") 
    edad = int(input("Edad: "))
    tratamiento = input("Tratamiento: ")

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO pacientes (nombre, edad, tratamiento)
    VALUES (?, ?, ?)
    """, (nombre, edad, tratamiento))

    conexion.commit()
    conexion.close()

    print("Paciente añadido correctamente")

def eliminar_paciente():
  
    ver_pacientes()

    id_paciente = int(input("ID del paciente a eliminar: "))

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    print("ID introducido:", id_paciente)

    cursor.execute("""
    DELETE FROM pacientes
    WHERE id = ? 
    """, (id_paciente,))

    conexion.commit()
    
    print("Pacientes eliminador", cursor.rowcount)

    conexion.close()

def modificar_paciente():
    
    ver_pacientes()

    id_paciente = int(input("ID del paciente a modificar: ")) 

    nuevo_nombre = input("Nuevo nombre: ")
    nueva_edad = int(input("Nueva edad: "))
    nuevo_tratamiento = input("Nuevo tratamiento: ")

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    UPDATE pacientes
    SET nombre = ?, edad = ?, tratamiento = ?
    WHERE id = ?
    """, (nuevo_nombre, nueva_edad, nuevo_tratamiento, id_paciente))

    conexion.commit()

    print("Pacientes modificados:", cursor.rowcount)

    conexion.close()

def ver_pacientes_ordenados():

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM pacientes
    ORDER BY edad
    """)

    pacientes = cursor.fetchall()

    for paciente in pacientes:
        print("ID:", paciente[0])
        print("Nombre:", paciente[1])
        print("Edad:", paciente[2])
        print("Tratamiento:", paciente[3])
        print("-----")

    conexion.close()

def contar_pacientes():

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM pacientes")

    total = cursor.fetchone()[0]

    print("Número de pacientes:", total)

    conexion.close()

def buscar_tratamiento():

    tratamiento = input("Tratamiento a buscar: ")

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM pacientes
    WHERE tratamiento = ?
    """, (tratamiento,))

    resultado = cursor.fetchall()

    if len(resultado)== 0:
        print("No hay pacientes con ese tratamiento.")
    else:
        for paciente in resultado:
            print("ID:", paciente[0])
            print("Nombre:", paciente[1])
            print("Edad:", paciente[2])
            print("Tratamiento:", paciente[3])
            print("-----")

    conexion.close()

def añadir_tratamiento():

    ver_pacientes()

    id_paciente = int(input("ID del paciente: "))
    fecha = input("Fecha: ")
    tratamiento = input("Tratamiento: ")

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO tratamientos (paciente_id, fecha, tratamiento)
    VALUES (?, ?, ?)
    """, (id_paciente, fecha, tratamiento))

    conexion.commit()

    print("Tratamiento añadido correctamente")

    conexion.close()


def buscar_mayores():

    edad = int(input("Edad minima: "))
    
    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM pacientes
    WHERE edad >= ?
    ORDER BY edad
    """, (edad,))

    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("No hay pacientes con esa edad o mayores.")
    else:
        for paciente in resultado:
            print("ID:", paciente[0])
            print("Nombre:", paciente[1])
            print("Edad:", paciente[2])
            print("Tratamiento:", paciente[3])
            print("-----")
    
    conexion.close()

def historial_tratamientos():

    ver_pacientes()

    id_paciente = int(input("ID del paciente: "))

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    
    cursor.execute("""
    SELECT fecha, tratamiento
    FROM tratamientos
    WHERE paciente_id = ?
    ORDER BY fecha
    """, (id_paciente,))


    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("Este paciente no tiene tratamientos.")
    else:
        for tratamiento in resultado:
            print("Fecha:", tratamiento[0])
            print("Tratamiento:", tratamiento[1])
            print("-----")
    
    conexion.close()

def eliminar_tratamiento():

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM tratamientos")

    tratamientos = cursor.fetchall()

    for tratamiento in tratamientos:
            print("ID:", tratamiento[0])
            print("ID paciente:", tratamiento[1])
            print("Fecha:", tratamiento[2])
            print("Tratamiento:", tratamiento[3])
            print("-----")
    
    id_tratamiento = int(input("ID del tratamiento a eliminar: "))

    cursor.execute ("""
    DELETE FROM tratamientos
    WHERE id = ?
    """, (id_tratamiento,))

    conexion.commit()

    print("Tratamientos eliminados:", cursor.rowcount)

    conexion.close()

def modificar_tratamiento():

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM tratamientos")

    tratamientos = cursor.fetchall()
    
    for tratamiento in tratamientos:
            print("ID:", tratamiento[0])
            print("ID paciente:", tratamiento[1])
            print("Fecha:", tratamiento[2])
            print("Tratamiento:", tratamiento[3])
            print("-----")
    

    id_tratamiento = int(input("ID del tratamiento a modificar:"))

    nueva_fecha = input("Nueva fecha: ")
    nuevo_tratamiento = input("Nuevo tratamiento: ")

    cursor.execute("""
    UPDATE tratamientos
    SET fecha = ?, tratamiento = ?
    WHERE id = ?
    """, (nueva_fecha, nuevo_tratamiento, id_tratamiento))

    conexion.commit()

    print("Tratamientos modificados:", cursor.rowcount)

    conexion.close()

def ver_tratamientos_pacientes():

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT pacientes.nombre,
           tratamientos.fecha,
           tratamientos.tratamiento
    FROM tratamientos
    JOIN pacientes
    ON tratamientos.paciente_id = pacientes.id
    """)

    resultado = cursor.fetchall()

    for fila in resultado:
        print("Paciente:", fila[0])
        print("Fecha:", fila[1])
        print("Tratamiento:", fila[2])
        print("-----")

    conexion.close()    

def buscar_nombre_parcial():

    texto = input("Introduce parte del nombre: ")

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * 
    FROM pacientes
    WHERE nombre LIKE ?
    """, ("%" + texto + "%",))

    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("No se han encontrado pacientes.")
    else:
        for paciente in resultado:
            print("ID:", paciente[0])
            print("Nombre:", paciente[1])
            print("Edad:", paciente[2])
            print("Tratamiento:", paciente[3])
            print("-----")
    
    conexion.close()

def buscar_por_edad():

    edad = int(input("Edad a buscar: "))

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * 
    FROM pacientes
    WHERE edad = ?
    """, (edad,))

    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("No hay pacientes con esa edad.")
    else:
        for paciente in resultado:
            print("ID:", paciente[0])
            print("Nombre:", paciente[1])
            print("Edad:", paciente[2])
            print("Tratamiento:", paciente[3])
            print("-----")
    
    conexion.close()

def buscar_rango_edades():

    edad_min = int(input("Edad minima:"))
    edad_max = int(input("Edad maxima:"))

    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * 
    FROM pacientes
    WHERE edad BETWEEN ? AND ?
    ORDER BY edad
    """, (edad_min, edad_max))

    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("No hay pacientes en ese rango.")
    else:
        for paciente in resultado:
            print("ID:", paciente[0])
            print("Nombre:", paciente[1])
            print("Edad:", paciente[2])
            print("Tratamiento:", paciente[3])
            print("-----")
    
    conexion.close()



while True:
    print("----- MENÚ CLÍNICA -----")
    print("1. Ver pacientes")
    print("2. Buscar paciente")
    print("3. Buscar tratamiento")
    print("4. Estadisticas")
    print("5. Salir")
    print("6. Añadir paciente")
    print("7. Eliminar paciente")
    print("8. Modificar paciente")
    print("9. Ver pacientes ordenados por edad")
    print("10. Numero de pacientes")
    print("11. Buscar por tratamiento")
    print("12. Buscar mayores de una edad")
    print("13. Añadir tratamiento a paciente")
    print("14. Historial tratamientos")
    print("15. Eliminar tratamiento")
    print("16. Modificar tratamiento")
    print("17. Ver tratamientos con pacientes")
    print("18. Buscar paciente por nombre parcial")
    print("19. Buscar paciente por edad")
    print("20. Buscar paciente por rango de edad")


    opcion = input("Elige una opción: ")
    if opcion == "1":
        ver_pacientes()
        
    elif opcion == "2":
        buscar_paciente()

    elif opcion == "3":
        tratamiento_buscado = input("Tratamiento a buscar: ")

        for paciente in pacientes:
            if paciente["tratamiento"].lower() == tratamiento_buscado.lower():
                print("Nombre:", paciente["nombre"])
                print("Edad:", paciente["edad"])
                print("---")

    elif opcion == "4":
        total_pacientes = len(pacientes)
        mayores = 0 
        menores = 0
        edad_maxima = 0
        edad_minima = 100

        for paciente in pacientes:
            if paciente["edad"] >= 18:
                mayores += 1
            else:
                menores += 1

            if paciente["edad"] > edad_maxima:
                edad_maxima = paciente["edad"]
            if paciente["edad"] < edad_minima:
                edad_minima = paciente["edad"]

        print("Total de pacientes:", total_pacientes)
        print("Pacientes mayores de edad:", mayores)
        print("Pacientes menores de edad:", menores)
        print("Edad_máxima:", edad_maxima)
        print("Edad_mínima:", edad_minima)

        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT COUNT (*) FROM tratamientos")
        total_tratamientos = cursor.fetchone()[0]

        print("Total de tratamientos:", total_tratamientos)

        conexion.close()

    elif opcion == "5":
        print("Saliendo del programa...")
        break

    elif opcion == "6":
        añadir_paciente()

        
    elif opcion == "7":
        eliminar_paciente()
        
                
    elif opcion == "8":

        modificar_paciente()

    elif opcion == "9":
        ver_pacientes_ordenados()

    elif opcion == "10":
        contar_pacientes()
    
    elif opcion == "11":
        buscar_tratamiento()
    
    elif opcion == "12":
        buscar_mayores()

    elif opcion == "13":
        añadir_tratamiento()

    elif opcion == "14":
        historial_tratamientos()
    
    elif opcion == "15":
        eliminar_tratamiento()

    elif opcion == "16":
        modificar_tratamiento()

    elif opcion == "17":
        ver_tratamientos_pacientes()
    
    elif opcion == "18":
        buscar_nombre_parcial()
    
    elif opcion == "19":
        buscar_por_edad()

    elif opcion == "20":
        buscar_rango_edades()


    else:
        print("Opción no válida")

with open("pacientes.json", "w") as archivo:
    json.dump(pacientes, archivo, indent=4)
        
    

    