import unittest
from .svg import PathSegment, Line, Rotation

previousSegment = PathSegment(
    startPosition=(0, 0),
    startDirection=0,
    endPosition=(10, 10),
    endDirection=90,
    d=""
)


class TestMyTurtle(unittest.TestCase):
    def test_line(self):
        line = Line(length=20)
        segment = line.generate(previousSegment)

        self.assertEqual(segment.startPosition, previousSegment.endPosition)
        self.assertEqual(segment.startDirection, previousSegment.endDirection)
        self.assertAlmostEqual(segment.endPosition[0], 10)
        self.assertAlmostEqual(segment.endPosition[1], 30)
        self.assertEqual(segment.endDirection, segment.startDirection)
        self.assertEqual(segment.d, "L 10.0000 30.0000")

    def test_line_without_draw(self):
        line = Line(length=20, draw=False)
        segment = line.generate(previousSegment)

        self.assertEqual(segment.startPosition, previousSegment.endPosition)
        self.assertEqual(segment.startDirection, previousSegment.endDirection)
        self.assertAlmostEqual(segment.endPosition[0], 10)
        self.assertAlmostEqual(segment.endPosition[1], 30)
        self.assertEqual(segment.endDirection, segment.startDirection)
        self.assertEqual(segment.d, "M 10.0000 30.0000")

    def test_rotation(self):
        line = Rotation(angle=122)
        segment = line.generate(previousSegment)

        self.assertEqual(segment.startPosition, previousSegment.endPosition)
        self.assertEqual(segment.startDirection, previousSegment.endDirection)
        self.assertEqual(segment.endPosition, previousSegment.endPosition)
        self.assertAlmostEqual(segment.endDirection, 90-122)
        self.assertEqual(segment.d, "")


if __name__ == '__main__':
    unittest.main()
