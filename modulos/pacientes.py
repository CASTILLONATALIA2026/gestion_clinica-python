import sqlite3
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

