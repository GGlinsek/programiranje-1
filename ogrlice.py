import random
import collections


ogrlice8 = list(map(str.strip, open("ogrlice8.txt")))
ogrlice20 = list(map(str.strip, open("ogrlice20.txt")))
ogrlice1000 = list(map(str.strip, open("ogrlice1000.txt")))

l1="ogrlice8"
l2="ogrlice20"
l3="ogrlice1000"


def razlicne_ogrlice(ogrlice):
    ogrliceee=[]
    for x in ogrlice:
        ogrliceee.append(list(x))
    a = list(ogrliceee)
    i=0
    for x in ogrliceee:
        print(a, x)
        a.remove(x)
        for elem in a:
            if collections.Counter(elem) == collections.Counter(x):
                index=elem.index(x[0])
                print(index)
                if x[1] == elem[index+1] and  x[-1] == elem[index-1]:
                    print("yes")
                if x[-1] == elem[index+1] and  x[1] == elem[index-1]:
                    print("also yes")
                a.remove(elem)
        a.insert(i,x)
        i+=1
razlicne_ogrlice(ogrlice8)

stevec1 = 0
st_ogrlic = 0
"""
while stevec1 < 1000:
    stevec2 = 0
    videne_ogrlice = []
    while stevec2 < 1000:
        a = random.randint(0,1000)
        if a not in videne_ogrlice:
            videne_ogrlice.append(a)
        stevec2 += 1
    st_ogrlic += len(videne_ogrlice)
    stevec1 += 1

print("povprečno število ogrlic je", st_ogrlic/stevec1)
"""