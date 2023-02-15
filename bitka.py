import random
import sys
from math import radians, cos, sin, sqrt
import risar
import time
from PyQt5.QtWidgets import QMessageBox


class Krog:
    def __init__(self):
        self.x = random.randint(11, risar.maxX - 10)
        self.y = random.randint(11, risar.maxY - 10)
        self.angle = 360 * random.random()
        self.color = risar.nakljucna_barva()
        self.telo = risar.krog(risar.maxX * random.random(), risar.maxY * random.random(), 10, self.color, 1)
        self.pritisnjeno = False
        self.time = 0

    def update(self):
        self.telo.setPos(self.x, self.y)
        risar.obnovi()

    def forward(self, a):
        phi = radians(90 - self.angle)
        nx = self.x + a * cos(phi)
        ny = self.y - a * sin(phi)
        self.x = nx
        self.y = ny
        self.update()

    def rob(self):
        if self.x < 10 or self.x > risar.maxX - 10:
            self.angle = 360 - self.angle
        elif self.y < 10 or self.y > risar.maxY - 10:
            self.angle = 180 - self.angle

    def fly(self):
        if self.pritisnjeno is False:
            self.x, self.y = risar.miska()
            self.update()

    def klikanje(self, destroyed):
        self.pritisnjeno = True
        destroyed.add(self)
        self.time = time.time()

    def zadet(self):
        self.telo.setRect(-30, -30, 60, 60)
        c = self.telo.pen().color().lighter()
        c.setAlpha(192)
        self.telo.setBrush(c)

    def iskanje(self, destroyed):
        for ladja in destroyed:
            if sqrt((ladja.x - self.x) ** 2 + (ladja.y - self.y) ** 2) < 40:
                self.klikanje(destroyed)
                self.zadet()
                break

    def cas(self, adios):
        if time.time() - self.time > 4:
            adios.add(self)
            self.telo.hide()


def igra(stevilo_ladij, level, pogoj):
    goal = "potrebno je uničiti vsaj " + pogoj + " ladij!"
    QMessageBox.information(None, level, goal)
    krogi = []

    for i in range(stevilo_ladij):
        t = Krog()
        krogi.append(t)

    miska = Krog()
    miska.telo.setRect(-30, -30, 60, 60)
    risar.klik()
    destroyed = set()
    adios = set()
    counter = 0
    while len(destroyed) != 0 or counter == 0:
        for krog in krogi:
            krog.forward(5)
            krog.rob()
            if miska.pritisnjeno:
                krog.iskanje(destroyed)
        for krog in destroyed:
            krog.cas(adios)
            if krog in krogi:
                krogi.remove(krog)
        for ship in adios:
            destroyed.remove(ship)
            counter += 1
        adios = set()
        if risar.klik() is not None:
            miska.klikanje(destroyed)
        else:
            miska.fly()
        risar.cakaj(0.02)
    for krog in krogi:
        krog.telo.hide()
    return counter - 1


def sporocilo(d):
    besedilo = "Komandant, uspešno ste uničili " + str(d) + " ladij! Žal je to premalo. Poskusite znova"
    QMessageBox.information(None, "Eksplodirane ladje", besedilo)


def stopnja(stopnja_igre, st_unicenih_ladij, st_ladij):
    completed = False
    zahtevnost = str(st_unicenih_ladij) + " od " + str(st_ladij)
    while not completed:
        d = igra(st_ladij, stopnja_igre, zahtevnost)
        if d >= st_unicenih_ladij:
            completed = True
        else:
            sporocilo(d)


stopnja("stopnja 1", 1, 2)
stopnja("stopnja 2", 2, 2)
stopnja("stopnja 3", 3, 5)
stopnja("stopnja 4", 3, 4)
stopnja("stopnja 5", 4, 8)
stopnja("stopnja 6", 6, 10)
stopnja("stopnja 7", 8, 12)
stopnja("stopnja 8", 10, 14)
stopnja("stopnja 9", 13, 18)
stopnja("stopnja 10", 15, 20)

QMessageBox.information(None, "Zahvala",
                        "Odlično ste se odrezali v bitki z marsovci. Zahvaljujemo se vam za vaše delo!")
sys.exit()
