import unittest
from lsystems import curves


class TestCurves(unittest.TestCase):
    def test_postprocess(self):
        d = curves.Dragon()
        raw_str = d.run_str(3)
        self.assertEqual(raw_str, 'F+G+F-G+F+G-F-G')

        result = d.run_curved_str(3)
        curved_str = 'X))())((X'
        self.assertEqual(result, curved_str)


if __name__ == '__main__':
    unittest.main()
