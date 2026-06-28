beneficio = float(input("Beneficion mensual (€): "))
if beneficio >= 2000:
    print("Inversión muy rentable")
elif beneficio >= 1000:
    print("Inversión rentable")
elif beneficio >= 500:
    print("Inversión poco rentable")
elif beneficio >= 0:
    print("Inversión no rentable")
else:
    print("Inversión con pérdidas")
