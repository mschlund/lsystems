import unittest
from lsystems.svg import Line, Rotation, Arc, PopPosition, PushPosition, Cursor


class TestSvg(unittest.TestCase):
    def test_line(self):
        line = Line(length=20)
        start_cursor = Cursor(x=11, y=10, dir=90)

        segment, end_cursor = line.generate(start_cursor)

        self.assertEqual(segment, "L 11.0000 30.0000")
        self.assertEqual(end_cursor, Cursor(x=11, y=30, dir=90), f"Wrong Cursor: {end_cursor}")

    def test_line_without_draw(self):
        line = Line(length=20, draw=False)
        start_cursor = Cursor(x=11, y=10, dir=90)

        segment, end_cursor = line.generate(start_cursor)

        self.assertEqual(segment, "M 11.0000 30.0000")
        self.assertEqual(end_cursor, Cursor(x=11, y=30, dir=90), f"Wrong Cursor: {end_cursor}")

    def test_rotation(self):
        line = Rotation(angle=122)
        start_cursor = Cursor(x=11, y=10, dir=90)

        segment, end_cursor = line.generate(start_cursor)

        self.assertEqual(end_cursor, Cursor(x=11, y=10, dir=90-122), f"Wrong Cursor: {end_cursor}")
        self.assertEqual(segment, "")

    def test_arc(self):
        arc = Arc(angle=90, rx=10, ry=10)
        start_cursor = Cursor(x=0, y=0, dir=0)

        segment, end_cursor = arc.generate(start_cursor)

        self.assertEqual(end_cursor, Cursor(x=10, y=-10, dir=-90), f"Wrong Cursor: {end_cursor}")
        self.assertEqual(segment, "A 10.0000 10.0000 0 0 0 10.0000 -10.0000")

    def test_push_pop_position(self):
        stack = []
        push = PushPosition(stack=stack)
        push_start_cursor = Cursor(x=11, y=10, dir=90)

        push_segment, push_end_cursor = push.generate(push_start_cursor)

        self.assertEqual(push_end_cursor, Cursor(x=11, y=10, dir=90), f"Wrong Cursor: {push_end_cursor}")
        self.assertEqual(push_segment, "")
        self.assertEqual(len(stack), 1)

        pop = PopPosition(stack=stack)
        pop_start_cursor = Cursor(x=50, y=100, dir=12)
        pop_segment, pop_end_cursor = pop.generate(pop_start_cursor)

        self.assertEqual(pop_end_cursor, Cursor(x=11, y=10, dir=90), f"Wrong Cursor: {pop_end_cursor}")
        self.assertEqual(pop_segment, "M 11.0000 10.0000")
        self.assertEqual(len(stack), 0)


if __name__ == '__main__':
    unittest.main()
