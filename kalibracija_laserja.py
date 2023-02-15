
from math import pi
import inspect
import sys
import unittest
import contextlib
import random
import ast


def povrsina(koord):
    return sum(povrsina(x) for x in notranji(koord)) + pi*r(koord)**2


def najmanjsi(koord):
    return min([koord] + [najmanjsi(x) for x in notranji(koord)],key=r)


# Ne kopiraj tega slovarja ven iz funkcije!
# Vedno samo kliči funkcijo!
def r(koord):
    return {(0, 10): 7.5,
            (0, 6): 2.5,
            (3.75, 12.5): 2.5,
            (3.75, 11.25): 1.25,
            (-3.75, 12.5): 2.5,
            (-5, 12.5): 1.25,

            (20, 10): 7.5, (20, 6): 2.5,
            (23.75, 12.5): 2.5, (23.75, 11.25): 1.25,
            (16.25, 12.5): 2.5, (15, 12.5): 1.25,
            (20, 10.625): 0.625,

            (-2.5, -8.75): 8.75,
            (-8.125, -4.375): 0.625,
            (-1.875, -9.375): 6.875,
            (-1.25, -10): 5,
            (-1.25, -9.25): 3.75,
            (-0.625, -10.625): 1.875,

            (21.25, -16.25): 11.25,
            (21.25, -7.5): 2.5,
            (22.5, -7.5): 1.25,
            (25.625, -13.125): 3.125,
            (26.875, -11.875): 0.625,
            (26.25, -21.25): 3.75,
            (16.25, -21.25): 3.75,
            (16.25, -22.25): 2.5,
            (16.125, -22.875): 0.875,
            (16.25, -12.5): 3.75
            }[koord]


# Ne kopiraj tega slovarja ven iz funkcije!
# Vedno samo kliči funkcijo!
def notranji(koord):
    noter = {(0, 10): [(0, 6), (3.75, 12.5), (-3.75, 12.5)],
             (0, 6): [],
             (3.75, 12.5): [(3.75, 11.25)],
             (3.75, 11.25): [],
             (-3.75, 12.5): [(-5, 12.5)],
             (-5, 12.5): [],

             (20, 10): [(20, 6), (23.75, 12.5), (16.25, 12.5), (20, 10.625)],
             (20, 6): [],
             (23.75, 12.5): [(23.75, 11.25)],
             (23.75, 11.25): [],
             (16.25, 12.5): [(15, 12.5)],
             (15, 12.5): [],
             (20, 10.625): [],

             (-2.5, -8.75): [(-8.125, -4.375), (-1.875, -9.375)],
             (-8.125, -4.375): [],
             (-1.875, -9.375): [(-1.25, -10)],
             (-1.25, -10): [(-1.25, -9.25)],
             (-1.25, -9.25): [(-0.625, -10.625)],
             (-0.625, -10.625): [],

             (21.25, -16.25): [(21.25, -7.5), (25.625, -13.125),
                               (26.25, -21.25), (16.25, -21.25),
                               (16.25, -12.5)],
             (21.25, -7.5): [(22.5, -7.5)],
             (22.5, -7.5): [],
             (25.625, -13.125): [(26.875, -11.875)],
             (26.875, -11.875): [],
             (26.25, -21.25): [],
             (16.25, -21.25): [(16.25, -22.25)],
             (16.25, -22.25): [(16.125, -22.875)],
             (16.125, -22.875): [],
             (16.25, -12.5): []}[koord]
    random.shuffle(noter)
    return noter

class Test(unittest.TestCase):
    with open(__file__, "r", encoding="utf-8") as f:
        functions = {
            elm.name: elm
            for elm in ast.parse(f.read()).body
            if isinstance(elm, ast.FunctionDef)}

    def assert_proper_shape(self, func):
        code = func.__code__
        self.assertTrue(
            code.co_argcount + code.co_kwonlyargcount == 1
            and not code.co_flags & (inspect.CO_VARARGS | inspect.CO_VARKEYWORDS),
            f"Funkcija '{func.__name__}' naj sprejme en argument"
        )


class TestObvezna(Test):
    def setUp(cls):
        sys.setrecursionlimit(10000)

    @staticmethod
    def r0(koord):
        x, _ = koord
        return 2 ** f"{x:b}"[::-1].index("1")

    @classmethod
    def notranji0(cls, koord):
        x, y = koord
        r0 = cls.r0(koord) // 2
        return r0 and [(x - r0, y), (y + r0, y)] or []

    @staticmethod
    def r1(koord):
        x, _ = koord
        return 1000 - x

    @staticmethod
    def notranji1(koord):
        x, _ = koord
        return [(x + 1, 0)] if x < 999 else []

    @classmethod
    @contextlib.contextmanager
    def patched_with(cls, new_r, new_notranji):
        global r, notranji
        try:
            r, orig_r = new_r, r
            notranji, orig_notranji = new_notranji, notranji
            yield
        finally:
            r = orig_r
            notranji = orig_notranji

    def test_00_oblika_funkcij(self):
        for func in self.functions:
            self.assertIn(func, {"povrsina", "najmanjsi", "r", "notranji"},
                          f"\nFunkcija {func} ni dovoljena.")

    def test_01_povrsina(self):
        self.assert_proper_shape(povrsina)
        self.assertAlmostEqual(pi * 78.125, povrsina((0, 10)))
        self.assertAlmostEqual(pi * 78.515625, povrsina((20, 10)))
        self.assertAlmostEqual(pi * 166.796875, povrsina((-2.5, -8.75)))
        self.assertAlmostEqual(pi * 193.734375, povrsina((21.25, -16.25)))

        with self.patched_with(self.r0, self.notranji0):
            self.assertAlmostEqual(
                sum(pi * 2 ** i * (2 ** (10 - i)) ** 2 for i in range(11)),
                povrsina((1024, 0)), places=3)
            self.assertAlmostEqual(
                sum(pi * 2 ** i * (2 ** (8 - i)) ** 2 for i in range(9)),
                povrsina((256, 0)), places=3)

        with self.patched_with(self.r1, self.notranji1):
            self.assertAlmostEqual(
                sum(pi * i ** 2 for i in range(1001)),
                povrsina((0, 0)), places=3)

            sys.setrecursionlimit(1000)
            # Če pade ta test, to pomeni, da funkcija ne preiskuje krogov
            # rekurzivno. Piši profesorju ali asistentom
            self.assertRaises(RecursionError, povrsina, (0, 0))

    def test_02_najmanjsi(self):
        self.assert_proper_shape(najmanjsi)
        self.assertEqual((20, 10.625), najmanjsi((20, 10)))
        self.assertEqual((-8.125, -4.375), najmanjsi((-2.5, -8.75)))
        self.assertEqual((26.875, -11.875), najmanjsi((21.25, -16.25)))
        self.assertIn(najmanjsi((0, 10)), {(3.75, 11.25), (-5, 12.5)})

        with self.patched_with(self.r0, self.notranji0):
            for x0 in (64, 256, 1024):
                x, y = najmanjsi((x0, 0))
                self.assertEqual(0, y)
                self.assertEqual(1, x % 2)

        with self.patched_with(self.r1, self.notranji1):
            self.assertEqual((999, 0), najmanjsi((0, 0)))

            sys.setrecursionlimit(1000)
            # Če pade ta test, to pomeni, da funkcija ne preiskuje krogov
            # rekurzivno. Piši profesorju ali asistentom
            self.assertRaises(RecursionError, najmanjsi, (0, 0))


class TestDodatna(Test):
    def test_oneline(self):
        for funcname in {"povrsina", "najmanjsi"}:
            body = self.functions[funcname].body
            self.assertEqual(len(body), 1, "\nFunkcija ni dolga le eno vrstico")
            self.assertIsInstance(body[0], ast.Return, "\nFunkcija naj bi vsebovala le return")


if __name__ == "__main__":
    unittest.main()
