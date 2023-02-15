import time
import ast
import unittest
from math import pi, sqrt


def polmeri(krogi):
    return {r for x, y, r in krogi}


def veliki(r0, krogi):
    return {(x, y) for x, y, r in krogi if r >= r0}


def obsegi(krogi):
    return sum(2 * pi * r for x, y, r in krogi)


def najlevo(krogi):
    return min({x - r for x, y, r in krogi})


def povrsina(krogi):
    return (max(x + r for x, y, r in krogi) - min(x - r for x, y, r in krogi)) * (
                max(y + r for x, y, r in krogi) - min(y - r for x, y, r in krogi))


def ocisti_slovar(d):
    return {x: y for x, y in d.items() if y != 0}


def znotraj(x0, y0, r0, krogi):
    return [(x, y, r) for x, y, r in krogi if r0 > sqrt((x0 - x) ** 2 + (y0 - y) ** 2) and r0 > r]


def vsebovanost(krogi):
    return ocisti_slovar(
        {(x, y, r): set(znotraj(x, y, r, krogi)) for x, y, r in sorted(krogi) if len(znotraj(x, y, r, krogi)) != 0})


def notranjost(krogi):
    return set().union(*map(set, vsebovanost(krogi).values()))


def ptici0(vsebovani, notranji):
    return {(x, y) for (x, y, r), notr_krogi in vsebovani.items() if len(notr_krogi) == 2 and (x, y, r) not in notranji and sorted(notr_krogi)[0] not in vsebovani and sorted(notr_krogi)[1] not in vsebovani}


def ptici(krogi):
    return ptici0(vsebovanost(krogi), notranjost(krogi))


def letala0(vsebovani, notranji):
    return {(x, y) for (x, y, r), notr_krogi in vsebovani.items() if len(notr_krogi) > 0 and len(notr_krogi) != 2 and (x, y, r) not in notranji and all(d not in vsebovani for d in notr_krogi)}


def letala(krogi):
    return letala0(vsebovanost(krogi), notranjost(krogi))


def sumljivi0(krogi, vsebovani, notranji):
    return {(x, y) for (x, y, r) in krogi if (x, y, r) not in notranji and ((x, y, r) not in vsebovani or [(x, y) for vkrog in vsebovani[(x, y, r)] if vkrog in vsebovani])}


def sumljivi(krogi):
   return sumljivi0(krogi, vsebovanost(krogi), notranjost(krogi))


krogi = [
    (164.4, 136.8, 50.8),
    (59.2, 182.8, 50.8),
    (282.8, 71.5, 45.6),
    (391, 229.4, 58.4),
    (259.9, 186, 47.6),
    (428, 89, 63.2),
    (88.6, 44.3, 37.5),
    (371.6, 233.6, 10.6),
    (408.7, 210.5, 8.9),
    (398.1, 95.5, 13),
    (449.5, 99.6, 13.6),
    (455.4, 66.5, 12.4),
    (139.6, 138, 10.6),
    (185, 138, 10.6),
    (69.8, 46.5, 10.6),
    (267.4, 51.7, 17.2),
    (225.8, 187.3, 7.5),
    (242.8, 187.3, 7.5),
    (259.8, 187.3, 7.5),
    (276.7, 187.3, 7.5),
    (293.7, 187.3, 7.5),
    (267.4, 51.7, 10.6),
    (99.6, 43.1, 17.2),
    (99.6, 43.1, 10.6),
    (150.3, 245.5, 50.8),
    (144.3, 243.6, 38.8),
    (127.3, 245.5, 7.5),
    (161.3, 245.5, 7.5)]



class TestOneLineMixin:
    functions = {
        elm.name: elm
        for elm in ast.parse(open(__file__, "r", encoding="utf-8").read()).body
        if isinstance(elm, ast.FunctionDef)}

    def assert_is_one_line(self, func):
        func
        body = self.functions[func.__code__.co_name].body
        self.assertEqual(len(body), 1, "\nFunkcija ni dolga le eno vrstico")
        self.assertIsInstance(body[0], ast.Return, "\nFunkcija naj bi vsebovala le return")

    def test_nedovoljene_funkcije(self):
        dovoljene_funkcije = {
            "polmeri", "veliki", "obsegi", "najlevo", "povrsina",
            "znotraj", "ocisti_slovar", "vsebovanost", "notranjost",
            "ptici0", "ptici", "letala0", "letala", "sumljivi0", "sumljivi"}
        for func in self.functions:
            self.assertIn(func, dovoljene_funkcije, f"\nFunkcija {func} ni dovoljena.")


class TestOgrevanje(unittest.TestCase, TestOneLineMixin):
    def test_polmeri(self):
        self.assert_is_one_line(polmeri)

        self.assertEqual({50.8}, polmeri(krogi[:1]))
        self.assertEqual({50.8, 45.6, 58.4}, polmeri(krogi[:4]))

    def test_veliki(self):
        self.assert_is_one_line(veliki)

        self.assertEqual({(391, 229.4), (428, 89)}, veliki(55, krogi))
        self.assertEqual({(428, 89)}, veliki(60, krogi))
        self.assertEqual(
            {(391, 229.4), (428, 89), (59.2, 182.8),
             (150.3, 245.5), (164.4, 136.8)},
            veliki(50, krogi))

    def test_obsegi(self):
        self.assert_is_one_line(obsegi)

        self.assertAlmostEqual(2 * pi * 50.8, obsegi(krogi[:1]))
        self.assertAlmostEqual(2 * pi * (50.8 + 50.8 + 45.6), obsegi(krogi[:3]))
        self.assertAlmostEqual(4033.1766486785764, obsegi(krogi))

    def test_najlevo(self):
        self.assertEqual(1, najlevo([(3, 0, 1), (5, 10, 4)]))

    def test_povrsina(self):
        self.assert_is_one_line(povrsina)

        self.assertEqual(10 * 10, povrsina([(0, 0, 5)]))
        self.assertEqual(10 * 10, povrsina([(0, 0, 5), (0, 0, 1)]))
        self.assertEqual((23 - (-5)) * 10, povrsina([(0, 0, 5), (20, 0, 3)]))
        self.assertEqual((23 - (-5)) ** 2, povrsina([(0, 0, 5), (20, 20, 3)]))
        self.assertAlmostEqual((2 * 50.8) ** 2, povrsina(krogi[:1]))
        self.assertAlmostEqual(66464.0, povrsina(krogi[:3]))
        self.assertAlmostEqual(139770.59999999998, povrsina(krogi))


class TestObvezna(unittest.TestCase, TestOneLineMixin):
    def setUp(self):
        self.zacetek = time.time()

    def tearDown(self):
        self.assertLess(time.time() - self.zacetek, 15,
                        "vsak test se mora končati hitreje kot v 15 sekundah")

    def test_znotraj(self):
        self.assertEqual([], znotraj(-100, -100, 5, krogi))
        self.assertEqual([], znotraj(-100, -100, 5, krogi))
        self.assertEqual([], znotraj(59.2, 182.8, 50, krogi))
        self.assertEqual([(59.2, 182.8, 50.8)], znotraj(59.2, 182.8, 51, krogi))
        self.assertEqual([], znotraj(59.2, 182.8, 50.8, krogi))
        self.assertEqual(krogi, znotraj(0, 0, 10000, krogi))
        self.assertEqual({(99.6, 43.1, 17.2),
                          (99.6, 43.1, 10.6),
                          (69.8, 46.5, 10.6)},
                         set(znotraj(88.6, 44.3, 37.5, krogi)))

    def test_vsebovanost(self):
        self.assertEqual({(88.6, 44.3, 37.5): {(69.8, 46.5, 10.6),
                                               (99.6, 43.1, 17.2),
                                               (99.6, 43.1, 10.6)},
                          (99.6, 43.1, 17.2): {(99.6, 43.1, 10.6)},
                          (144.3, 243.6, 38.8): {(127.3, 245.5, 7.5),
                                                 (161.3, 245.5, 7.5)},
                          (150.3, 245.5, 50.8): {(144.3, 243.6, 38.8),
                                                 (127.3, 245.5, 7.5),
                                                 (161.3, 245.5, 7.5)},
                          (164.4, 136.8, 50.8): {(139.6, 138, 10.6),
                                                 (185, 138, 10.6)},
                          (259.9, 186, 47.6): {(225.8, 187.3, 7.5),
                                               (242.8, 187.3, 7.5),
                                               (259.8, 187.3, 7.5),
                                               (276.7, 187.3, 7.5),
                                               (293.7, 187.3, 7.5)},
                          (267.4, 51.7, 17.2): {(267.4, 51.7, 10.6)},
                          (282.8, 71.5, 45.6): {(267.4, 51.7, 17.2),
                                                (267.4, 51.7, 10.6)},
                          (391, 229.4, 58.4): {(371.6, 233.6, 10.6),
                                               (408.7, 210.5, 8.9)},
                          (428, 89, 63.2): {(398.1, 95.5, 13),
                                            (449.5, 99.6, 13.6),
                                            (455.4, 66.5, 12.4)}},
                         {k: set(v) for k, v in vsebovanost(krogi).items()})

    def test_ptici(self):
        self.assert_is_one_line(ptici)
        self.assert_is_one_line(ptici0)

        self.assertEqual({(164.4, 136.8), (391, 229.4)}, ptici(krogi))

        self.assertEqual(set(), ptici([(x, x, 0.5) for x in range(1000)]))

        self.assertEqual(set(), ptici([(0, 0, x) for x in range(1000)]))

        self.assertEqual(set(), ptici([(x, x, r)
                                       for x in range(30 * 100, 100)
                                       for r in range(30)]))

        self.assertEqual({(-100, -100)},
                         ptici([(-100, -100, 10),
                                (-102, -100, 1),
                                (-99, -100, 1)] +
                               [(x, x, r)
                                for x in range(30 * 100, 100)
                                for r in range(50)]))


class TestDodatna(unittest.TestCase, TestOneLineMixin):
    def setUp(self):
        self.zacetek = time.time()

    def tearDown(self):
        self.assertLess(time.time() - self.zacetek, 15,
                        "vsak test se mora končati hitreje kot v 15 sekundah")

    def test_letala(self):
        self.assert_is_one_line(letala)
        self.assert_is_one_line(letala0)

        self.assertEqual({(259.9, 186), (428, 89)}, letala(krogi))

        self.assertEqual(set(), letala([(x, x, 0.5) for x in range(1000)]))
        self.assertEqual(set(), letala([(0, 0, x) for x in range(1000)]))

        self.assertEqual(set(), letala([(x, x, r)
                                        for x in range(30 * 100, 100)
                                        for r in range(30)]))

        self.assertEqual({(0, 0), (100000, 0), },
                         letala([(0, 0, 10000),
                                 (100000, 0, 1), (100000, 0, 0.5),
                                 (200000, 0, 1)]
                                + [(x, 0, 0.5) for x in range(1000)]))

        self.assertEqual({(100000, 0)},
                         letala([(0, 0, 10000),
                                 (100000, 0, 1), (100000, 0, 0.5),
                                 (200000, 0, 1)]
                                + [(x, 0, 0.5) for x in range(500)]
                                + [(x, 0, 0.3) for x in range(500)]))

    def test_sumljivi(self):
        self.assert_is_one_line(sumljivi)
        self.assert_is_one_line(sumljivi0)

        self.assertEqual({(59.2, 182.8),
                          (88.6, 44.3),
                          (150.3, 245.5),
                          (282.8, 71.5)},
                         sumljivi(krogi))

        crta = [(x, x, 0.5) for x in range(1000)]
        self.assertEqual({(x, y) for x, y, _ in crta}, sumljivi(crta))

        self.assertEqual({(0, 0)}, sumljivi([(0, 0, x) for x in range(1000)]))

        crta = {(x, x, 29) for x in range(30 * 100, 100)}
        self.assertEqual(crta,
                         sumljivi([(x, x, r)
                                   for x in range(30 * 100, 100)
                                   for r in range(30)]))

        self.assertEqual(crta,
                         sumljivi([(-100, -100, 10),
                                   (-102, -100, 1),
                                   (-99, -100, 1)] +
                                  [(x, x, r)
                                   for x in range(30 * 100, 100)
                                   for r in range(50)]))

        self.assertEqual({(200000, 0), },
                         sumljivi([(0, 0, 10000),
                                   (100000, 0, 1), (100000, 0, 0.5),
                                   (200000, 0, 1)]
                                  + [(x, 0, 0.5) for x in range(1000)]))

        self.assertEqual({(0, 0), (200000, 0)},
                         sumljivi([(0, 0, 10000),
                                   (100000, 0, 1), (100000, 0, 0.5),
                                   (200000, 0, 1)]
                                  + [(x, 0, 0.5) for x in range(500)]
                                  + [(x, 0, 0.3) for x in range(500)]))


if __name__ == "__main__":
    unittest.main()
