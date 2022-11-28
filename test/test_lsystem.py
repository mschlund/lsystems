import unittest
from lsystems import lsystem

sierpinski_spec = 'A -> B - A - B; B -> A + B + A;'


class TestSvg(unittest.TestCase):
    def test_sierpinski(self):
        L = lsystem.LSystem(sierpinski_spec, start_symbol='A')

        self.assertEqual(L.run(0), 'A')
        self.assertEqual(L.run(1), 'B-A-B')
        self.assertEqual(L.run(2), 'A+B+A-B-A-B-A+B+A')

    def test_get(self):
        L = lsystem.LSystem(sierpinski_spec, start_symbol='A')
        self.assertEqual(L.get_variables(), set(['A', 'B']))
        self.assertEqual(L.get_constants(), set(['+', '-']))

    def test_run_from_different_start(self):
        L = lsystem.LSystem(sierpinski_spec, start_symbol='A')
        self.assertEqual(L.run_from('AA', 1), 'B-A-BB-A-B')


if __name__ == '__main__':
    unittest.main()
