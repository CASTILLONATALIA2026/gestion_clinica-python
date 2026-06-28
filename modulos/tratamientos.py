import sqlite3
from modulos.pacientes import ver_pacientes

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

