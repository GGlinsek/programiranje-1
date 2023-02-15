import math

a = int(input("Vpiši a: "))
b = int(input("Vpiši b: "))
c = int(input("Vpiši c: "))
if b**2-4*a*c < 0:
    print("Enačba nima realnih rešitev")
else:
    resitev_1 = (-b + math.sqrt(b**2-4*a*c))/2*a
    resitev_2 = (-b - math.sqrt(b**2-4*a*c))/2*a
    if resitev_1 == resitev_2:
        print("enačba ima eno realno rešitev:", resitev_1)
    else:
        print("Enačba ima dve realni rešitvi:",resitev_1,"in",  resitev_2)


