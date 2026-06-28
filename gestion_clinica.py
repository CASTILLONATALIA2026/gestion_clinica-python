"""
GESTIÓN CLÍNICA - VERSIÓN 1.0

Aplicación de gestión clínica desarrollada en Python y SQLite.

Funciones:
-Gestión de pacientes
-Gestión de tratamientos
-Historial clínico
-Búsquedas avanzadas
-Estadísticas
"""

import json
import os
import sqlite3

from modulos.pacientes import (
    ver_pacientes,
    buscar_paciente,
    añadir_paciente,
    eliminar_paciente,
    modificar_paciente,
    ver_pacientes_ordenados,
    contar_pacientes
)

from modulos.tratamientos import (
    buscar_tratamiento,
    añadir_tratamiento,
    historial_tratamientos,
    eliminar_tratamiento,
    modificar_tratamiento,
    ver_tratamientos_pacientes
)

from modulos.busquedas import (
    buscar_nombre_parcial,
    buscar_por_edad,
    buscar_rango_edades
)

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

#==========================
# FUNCIONES DE PACIENTES
#==========================


#============================
# FUNCIONES DE TRATAMIENTOS
#============================


#==========================
# FUNCIONES DE BÚSQUEDA
#==========================



#==========================
# MENÚ PRINCIPAL
#==========================


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
        buscar_por_edad()

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
        
    

    