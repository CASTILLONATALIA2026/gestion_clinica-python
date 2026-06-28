pacientes = [

    {
        "nombre": "Natalia",
        "edad": 37,
        "tratamiento": "Limpieza"
    },
    {
        "nombre": "Luis",
        "edad": 6,
        "tratamiento": "Revisión"
    },
    {
        "nombre": "Valentina",
        "edad": 9,
        "tratamiento": "Ortodoncia"
    },
    {
        "nombre": "Rafael",
        "edad": 4,
        "tratamiento": "Obturación"
    }
    
]

for paciente in pacientes:

    print("Nombre:", paciente["nombre"])
    print("Edad:", paciente["edad"])
    print("Tratamiento:", paciente["tratamiento"])
    print("---")

mayor = 0
nombre_mayor = ""


for paciente in pacientes:
        if paciente["edad"] > mayor:
            mayor = paciente["edad"]
            nombre_mayor = paciente["nombre"]

print("Edad máxima:", mayor)
print("nombre mayor:", nombre_mayor)


menor = 100
nombre_menor = ""

for paciente in pacientes:
    if paciente["edad"] < menor:
            menor = paciente["edad"]
            nombre_menor = paciente["nombre"]

print("Edad mínima:", menor)
print("nombre menor:", nombre_menor)

ortodoncia = 0
for paciente in pacientes:
    if paciente["tratamiento"] == "Ortodoncia":
        ortodoncia += 1
        nombre = paciente["nombre"]

print("Número de pacientes con ortodoncia:", ortodoncia)        
print("Nombre del paciente con ortodoncia:", nombre)

def es_mayor_edad(edad):
    if edad >= 18:
        return True
    else:
        return False
    
print(es_mayor_edad(37))

def mostrar_paciente(nombre, edad, tratamiento):
    print("Nombre:", nombre)
    print("Edad:", edad)
    print("Tratamiento:", tratamiento)

mostrar_paciente("Natalia", 37, "Limpieza")
mostrar_paciente("Valentina", 9, "Ortodoncia")

def calcular_media(lista):
    suma = 0
    for numero in lista:
        suma = suma + numero

    media = suma / len(lista)
    return media

numeros = [10, 20, 30, 40]
resultado = calcular_media(numeros)
print("Media:", resultado)

def es_par(numero):
    if numero % 2 == 0:
        return True
    else:
        return False
print(es_par(8))
print(es_par(5))

def es_mayor_diez(numero):
    if numero >10:
         return True
    else:
        return False
print(es_mayor_diez(15))
print(es_mayor_diez(7))

def contar_mayores(lista):
    contador = 0
    for numero in lista:
        if numero > 18:
            contador = contador + 1
    return contador

edades = [37, 6, 9, 4]
resultado = contar_mayores(edades)
print("Mayores de edad:", resultado)

def mostrar_mayoria_edad(pacientes):
    for paciente in pacientes:
        if paciente["edad"] >= 18:
            print(paciente["nombre"], "es mayor de edad")
        else:
            print(paciente["nombre"], "es menor de edad")
mostrar_mayoria_edad(pacientes)

def contar_tratamientos(pacientes):
    limpieza = 0
    revision = 0
    ortodoncia = 0
    obturacion = 0

    for paciente in pacientes:
        if paciente["tratamiento"] == "Limpieza":
            limpieza += 1
        if paciente["tratamiento"] == "Revisión":
            revision += 1
        if paciente["tratamiento"] == "Ortodoncia":
            ortodoncia += 1
        if paciente["tratamiento"] == "Obturación":
            obturacion += 1

    print("Limpieza:", limpieza)
    print("Revisión:", revision)
    print("Ortodoncia:", ortodoncia)
    print("Obturación:", obturacion)
contar_tratamientos(pacientes)

def buscar_tratamiento(tratamiento_buscado):
    for paciente in pacientes:
        if paciente["tratamiento"] ==tratamiento_buscado:
            print(paciente["nombre"])

buscar_tratamiento("Ortodoncia")
buscar_tratamiento("Limpieza")