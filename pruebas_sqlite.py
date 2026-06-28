import sqlite3

conexion = sqlite3.connect("clinica.db")
print("Base de datod conectada")

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

print("Tabla creada")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tratamientos (
               
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER,
    fecha TEXT,
    tratamiento TEXT,
               
    FOREIGN KEY  (paciente_id) REFERENCES pacientes(id)

)
""")

conexion.commit()

print("Tabla tratamientos creada")

conexion.close()

