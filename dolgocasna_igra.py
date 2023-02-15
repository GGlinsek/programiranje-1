from random import *

def najbolsi_met(n):
    seed(n)
    stevilo_metov = 0
    stevilo_petk = 0
    stevilo_pik = 0

    while stevilo_petk < 100:
        stevilo_pik += randint(1, 6)
        stevilo_metov += 1
        if stevilo_pik > 5:
            stevilo_pik -= 6
        if stevilo_pik == 5:
            stevilo_petk += 1
    return stevilo_metov

print(najbolsi_met(8))

st_seed = 0
najmanj_metov = najbolsi_met(0)

for x in range(1, 100000):
    st_metov = najbolsi_met(x)
    if st_metov < najmanj_metov :
        st_seed=x
        najmanj_metov = st_metov

print("najmanj metov dobimo pri seedu:", st_seed, "in potrebujemo:", najmanj_metov, "metov")

