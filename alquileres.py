alquiler1 = float(input("Alquiler piso 1:"))
alquiler2 = float(input("Alquiler piso 2:"))
hipoteca= float(input("Hipoteca mensual:"))

ingresos = alquiler1 + alquiler2
beneficio = ingresos - hipoteca

print("Ingresos:", ingresos, "€")
print("Beneficio mensual:", beneficio, "€")
print("Beneficio anual:", beneficio * 12, "€")
