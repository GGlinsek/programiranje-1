vsota = 0
i = 0
while True:
    a = int(input("Cena izdelka: "))
    vsota += a
    if a != 0:
        i+=1
    else:
        break

print("vsota:", vsota)
print("Povprečna cena: ", vsota/i)