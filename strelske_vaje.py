import math

hitrost_izstrelka = float(input("hitrost izstrelka:"))
kot = float((input("kot:")))*math.pi/180*2

pot = float(hitrost_izstrelka**2*math.sin(kot)/9.807)

print("krogla bo preletela pot", pot, "metrov")

