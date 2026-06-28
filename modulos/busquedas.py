import sqlite3
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
