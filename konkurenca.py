vsota = 0
st_izdelkov = int(input("število izdelkov: "))
for x in range (0,st_izdelkov):
    vsota += int(input("Cena artikla: "))

print("vsota:", vsota)