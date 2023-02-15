poteze = [("j", "a"), ("a", "b"), ("b", "j"), ("a", "b"), ("j", "a"),
          ("a", "b"), ("b", "j"), ("a", "b"), ("a", "j"), ("b", "a"),
          ("j", "a"), ("a", "j")]

a = 0
b = 0
for izlijemo, vlijemo in poteze:
    a_max = 7
    b_max = 4
    if izlijemo == "j":  # voda iz jezera
        if vlijemo == "a":  # v vrč a
            a = 7
        else:  # v vrč b
            b = 4
    elif izlijemo == "a":  # voda iz vrča a
        if vlijemo == "b":  # voda v vrča b
            if a + b <= 4:
                b += a
                a = 0
            else:
                a = a - (4 - b)
                b = 4

        else:  # voda v jezero
            a = 0
    else:  # voda iz vrča b
        if vlijemo == "a":  # voda v vrč a
            if a < 4:
                a += b
                b = 0
            else:
                c = 7 - a
                b -= c
                a += c
        else:  # voda v jezero
            b = 0
    print(a, b)

stanja = [(7, 0), (3, 4), (3, 0), (0, 3), (7, 3), (6, 4),
          (6, 0), (2, 4), (0, 4), (4, 0), (7, 0), (0, 0)]

print("\n\n")

vrc_a = 0
vrc_b = 0

for a, b in stanja:
    izlito = "j"
    vlito = "j"
    if a > vrc_a:
        vlito = "a"
        vrc_a = a
    elif a < vrc_a:
        izlito = "a"
        vrc_a = a
    if b > vrc_b:
        vlito = "b"
        vrc_b = b
    elif b < vrc_b:
        izlito = "b"
        vrc_b = b
    print(izlito, vlito)
