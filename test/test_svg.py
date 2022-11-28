import unittest
from lsystems.svg import PathSegment, Line, Rotation

previous_segment = PathSegment(
    start_position=(0, 0),
    start_direction=0,
    end_position=(10, 10),
    end_direction=90,
    d=""
)


class TestSvg(unittest.TestCase):
    def test_line(self):
        line = Line(length=20)
        segment = line.generate(previous_segment)

        self.assertEqual(segment.start_position, previous_segment.end_position)
        self.assertEqual(segment.start_direction, previous_segment.end_direction)
        self.assertAlmostEqual(segment.end_position[0], 10)
        self.assertAlmostEqual(segment.end_position[1], 30)
        self.assertEqual(segment.end_direction, segment.start_direction)
        self.assertEqual(segment.d, "L 10.0000 30.0000")

    def test_line_without_draw(self):
        line = Line(length=20, draw=False)
        segment = line.generate(previous_segment)

        self.assertEqual(segment.start_position, previous_segment.end_position)
        self.assertEqual(segment.start_direction, previous_segment.end_direction)
        self.assertAlmostEqual(segment.end_position[0], 10)
        self.assertAlmostEqual(segment.end_position[1], 30)
        self.assertEqual(segment.end_direction, segment.start_direction)
        self.assertEqual(segment.d, "M 10.0000 30.0000")

    def test_rotation(self):
        line = Rotation(angle=122)
        segment = line.generate(previous_segment)

        self.assertEqual(segment.start_position, previous_segment.end_position)
        self.assertEqual(segment.start_direction, previous_segment.end_direction)
        self.assertEqual(segment.end_position, previous_segment.end_position)
        self.assertAlmostEqual(segment.end_direction, 90-122)
        self.assertEqual(segment.d, "")


if __name__ == '__main__':
    unittest.main()
