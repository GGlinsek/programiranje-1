import math

stevilo = int(input("vpiši število: "))

if math.sqrt(stevilo) % 1 == 0:
    print("število je kvadrat")
else:
    print("število ni kvadrat")