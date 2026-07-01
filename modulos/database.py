import sqlite3


conexion = sqlite3.connect("clinica.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    edad INTEGER,
    tratamiento TEXT
)
""")

conexion.commit()
conexion.close()

def obtener_pacientes():
    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT nombre, edad, tratamiento FROM pacientes"
    )

    pacientes = cursor.fetchall()

    conexion.close()

    return pacientes


   
def insertar_paciente(nombre, edad, tratamiento):
    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO pacientes 
        (nombre, edad, tratamiento)
        VALUES (?, ?, ?)
        """,
        (nombre, edad, tratamiento)
    )

    conexion.commit()
    conexion.close()