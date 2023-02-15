# Svoj program dopiši tukaj
import math
import unittest
import random


def podatek(kljuc, podatki):
    vrnjen_podatek = None
    for x, y in podatki:
        if kljuc == x:
            vrnjen_podatek = y
            break
        elif kljuc == y:
            vrnjen_podatek = x
            break
    return vrnjen_podatek


def razdalja(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    return math.sqrt((abs((x1 - x2) ** 2 + (abs(y1 - y2) ** 2))))


def oddaljenost(kraj1, kraj2, koordinate):
    return razdalja(podatek(kraj1, koordinate), podatek(kraj2, koordinate))


def visina(kraj1, kraj2, visine):
    return podatek(kraj2, visine) - podatek(kraj1, visine)


def cas(s, h):
    if h >= 0:
        return s * 2.4 + (1 / 12 * h)
    elif h < 0:
        return s * 2.4 - abs(h) / 250


def cas_med(kraj1, kraj2, koordinate, visine):
    return cas(oddaljenost(kraj1, kraj2, koordinate), visina(kraj1, kraj2, visine))


def skupni_cas(kraji, koordinate, visine):
    prejsni_kraj = None
    porabljen_cas = 0
    for x in kraji:
        if prejsni_kraj is None:
            True
        else:
            porabljen_cas += cas_med(prejsni_kraj, x, koordinate, visine)
        prejsni_kraj = x
    return porabljen_cas


def skrajsaj(kraji, koordinate, visine):
    najkrajsi_cas = 0
    izpusceni_kraj = None
    a = list(kraji)
    b = list(kraji)
    i = 0
    for x in a:
        del b[i]
        trenutni_cas = skupni_cas(b,koordinate, visine)
        if trenutni_cas < najkrajsi_cas or najkrajsi_cas == 0:
            najkrajsi_cas = trenutni_cas
            izpusceni_kraj = i
        b.insert(i, x)
        i += 1
    del a[izpusceni_kraj]
    return a


class T:
    koordinate = [('Piran', (0, 0)), ('Koper', (8, 2)),
                  ('Ilirska Bistrica', (49, 5)), ('Postojna', (46, 29)),
                  ('Gorica', (2, 48)), ('Ajdovščina', (24, 42)),
                  ('Idrija', (34, 54)), ('Logatec', (48, 46)),
                  ('Cerknica', (60, 31)), ('Vrhnika', (37, 51)),
                  ('Žiri', (39, 60)), ('Ljubljana', (68, 61)),
                  ('Ribnica', (26, 87)), ('Kočevje', (15, 95)),
                  ('Grosuplje', (49, 82)), ('Litija', (95, 61)),
                  ('Kranj', (58, 82)), ('Kamnik', (78, 80)),
                  ('Škofja Loka', (54, 73)), ('Trbovlje', (112, 71)),
                  ('Novo mesto', (119, 32)), ('Krško', (162, 56)),
                  ('Celje', (129, 80)), ('Maribor', (156, 117)),
                  ('Velenje', (117, 94)), ('Slovenska Bistrica', (150, 97)),
                  ('Murska Sobota', (196, 138)), ('Ptuj', (173, 102)),
                  ('Ormož', (196, 100)), ('Ljutomer', (199, 112)),
                  ('Gornja Radgona', (184, 139))]

    visine = [("Piran", 23), ("Koper", 4), ("Ilirska Bistrica", 440),
              ("Postojna", 555), ("Nova Gorica", 93), ("Ajdovščina", 106),
              ("Idrija", 340), ("Logatec", 481), ("Cerknica", 559),
              ("Vrhnika", 293), ("Žiri", 481), ("Ljubljana", 295),
              ("Ribnica", 492), ("Kočevje", 465), ("Grosuplje", 338),
              ("Litija", 241), ("Kranj", 386), ("Kamnik", 382),
              ("Škofja Loka", 354), ("Trbovlje", 307), ("Novo mesto", 189),
              ("Krško", 162), ("Celje", 238), ("Maribor", 275),
              ("Velenje", 400), ("Slovenska Bistrica", 271),
              ("Murska Sobota", 189), ("Ptuj", 229), ("Ormož", 216),
              ("Ljutomer", 174), ("Gornja Radgona", 209)]

    for k, _ in koordinate:
        if podatek(k, visine) is None:
            print(k)


class TestObvezna(unittest.TestCase, T):
    def test_podatek(self):
        visine = [("Ana", 156), ("Berta", 167), ("Cilka", 160)]
        self.assertEqual(156, podatek("Ana", visine))
        self.assertEqual(167, podatek("Berta", visine))
        self.assertEqual(160, podatek("Cilka", visine))
        self.assertIsNone(podatek("Dani", visine))
        visine.append(("Dani", 180))
        self.assertEqual(180, podatek("Dani", visine))

        koordinate = [("Ljubljana", (4, 5)), ("Brežice", (-1, -6))]
        self.assertEqual((4, 5), podatek("Ljubljana", koordinate))
        self.assertEqual((-1, -6), podatek("Brežice", koordinate))
        self.assertIsNone(podatek("Šentjošt", koordinate))

        self.assertIsNone(podatek("Mugabe", []))

    def test_razdalja(self):
        self.assertAlmostEqual(5, razdalja((4, -3), (1, 1)))
        self.assertAlmostEqual(5, razdalja((4, 3), (1, -1)))
        self.assertAlmostEqual(5, razdalja((4, 3), (7, 7)))
        self.assertAlmostEqual(5, razdalja((-4, 3), (0, 0)))
        self.assertAlmostEqual(5, razdalja((-4, -2), (-7, -6)))
        self.assertAlmostEqual(13, razdalja((1, 2), (6, -10)))

    def test_oddaljenost(self):
        self.assertEqual(0, oddaljenost("Piran", "Piran", self.koordinate))
        self.assertAlmostEqual(63.89053137985315, oddaljenost("Ljubljana", "Celje", self.koordinate))
        self.assertAlmostEqual(63.89053137985315, oddaljenost("Celje", "Ljubljana", self.koordinate))
        self.assertAlmostEqual(104.06248123122954, oddaljenost("Kranj", "Maribor", self.koordinate))
        a, b = str(random.randint(0, 1000)), str(random.randint(0, 1000))
        self.assertEqual(5, oddaljenost(a, b, [(a, (3, 4)), (b, (0, 0))]))

    def test_visine(self):
        self.assertEqual(-4, visina("Maribor", "Slovenska Bistrica", self.visine))
        self.assertEqual(4, visina("Slovenska Bistrica", "Maribor", self.visine))

        a, b = str(random.randint(0, 1000)), str(random.randint(0, 1000))
        self.assertEqual(42, visina(a, b, [(a, 15), (b, 57)]))
        self.assertEqual(-42, visina(b, a, [(a, 15), (b, 57)]))
        self.assertEqual(0, visina(a, a, [(a, 15), (b, 57)]))

    def test_cas(self):
        self.assertAlmostEqual(2.4 + 100 / 12, cas(1, 100))
        self.assertAlmostEqual(4.8 + 300 / 12, cas(2, 300))
        self.assertAlmostEqual(24, cas(10, 0))

        self.assertAlmostEqual(2.4 - 1, cas(1, -250))
        self.assertAlmostEqual(24 - 100 / 250, cas(10, -100))

    def test_cas_med(self):
        self.assertAlmostEqual(19.714907002964768, cas_med("Piran", "Koper", self.koordinate, self.visine))
        self.assertAlmostEqual(21.3742403362981, cas_med("Koper", "Piran", self.koordinate, self.visine))
        self.assertAlmostEqual(75.5, cas_med("Ljubljana", "Logatec", self.koordinate, self.visine))
        self.assertAlmostEqual(59.256, cas_med("Logatec", "Ljubljana", self.koordinate, self.visine))
        self.assertAlmostEqual(589.1329074684095, cas_med("Piran", "Murska Sobota", self.koordinate, self.visine))
        self.assertAlmostEqual(574.6355741350761, cas_med("Murska Sobota", "Piran", self.koordinate, self.visine))

    def test_skupni_cas(self):
        self.assertAlmostEqual(
            842.6918221506322,
            skupni_cas(["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
                        "Ljubljana", "Kranj", "Kamnik", "Celje", "Ptuj",
                        "Maribor", "Murska Sobota"], self.koordinate, self.visine))
        self.assertAlmostEqual(
            19.714907002964768,
            skupni_cas(["Piran", "Koper"], self.koordinate, self.visine))
        self.assertAlmostEqual(
            19.714907002964768 + 21.3742403362981,
            skupni_cas(["Piran", "Koper", "Piran"], self.koordinate, self.visine))


class TestDodatna(unittest.TestCase, T):
    def test_skrajsaj(self):
        koord = self.koordinate
        vis = self.visine
        svarilo = "Pusti seznam, ki si ga dobil kot argument, pri miru!"

        kraji = ["Piran", "Ljubljana", "Koper"]
        self.assertEqual(["Piran", "Koper"], skrajsaj(kraji, koord, vis))
        self.assertEqual(["Piran", "Ljubljana", "Koper"], kraji, svarilo)

        kraji = ["Ljubljana", "Piran", "Koper"]
        self.assertEqual(["Piran", "Koper"], skrajsaj(kraji, koord, vis))
        self.assertEqual(["Ljubljana", "Piran", "Koper"], kraji, svarilo)

        kraji = ["Piran", "Koper", "Ljubljana"]
        self.assertEqual(["Piran", "Koper"], skrajsaj(kraji, koord, vis))
        self.assertEqual(["Piran", "Koper", "Ljubljana"], kraji, svarilo)

        ms = "Murska Sobota"
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj([ms, "Piran", "Koper", "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", "Kamnik", "Celje"],
                     koord, vis))
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", ms, "Koper", "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", "Kamnik", "Celje"],
                     koord, vis))
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", "Koper", ms, "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", "Kamnik", "Celje"],
                     koord, vis))
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", "Koper", "Postojna", ms, "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", "Kamnik", "Celje"],
                     koord, vis))
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", "Koper", "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", ms, "Kranj", "Kamnik", "Celje"],
                     koord, vis))
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", "Koper", "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", ms, "Kamnik", "Celje"],
                     koord, vis))
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", "Koper", "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", "Kamnik", ms, "Celje"],
                     koord, vis))
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", "Koper", "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", "Kamnik", "Celje", ms],
                     koord, vis))

        pi = "Piran"
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", "Koper", "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", pi, "Kamnik", "Celje"],
                     koord, vis))
        self.assertEqual(
            ["Piran", "Koper", "Postojna", "Logatec", "Vrhnika",
             "Ljubljana", "Kranj", "Kamnik", "Celje"],
            skrajsaj(["Piran", "Koper", "Postojna", "Logatec",
                      "Vrhnika", "Ljubljana", "Kranj", "Kamnik", "Celje", pi],
                     koord, vis))


if __name__ == "__main__":
    unittest.main()
