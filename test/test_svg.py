import unittest
from lsystems.svg import PathSegment, Line, Rotation, PopPosition, PushPosition

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

    def test_push_pop_position(self):
        stack = []
        push = PushPosition(stack=stack)
        segment = push.generate(previous_segment)

        self.assertEqual(len(stack), 1)
        self.assertEqual(segment.start_position, previous_segment.end_position)
        self.assertEqual(segment.start_direction, previous_segment.end_direction)
        self.assertEqual(segment.end_position, previous_segment.end_position)
        self.assertEqual(segment.end_direction, previous_segment.end_direction)
        self.assertEqual(segment.d, "")

        input_segment_to_pop = PathSegment(
            start_position=(1, 2),
            start_direction=3,
            end_position=(20, 20),
            end_direction=120,
            d=""
        )

        pop = PopPosition(stack=stack)
        popped_segment = pop.generate(input_segment_to_pop)
        
        self.assertEqual(len(stack), 0)
        self.assertEqual(popped_segment.start_position, input_segment_to_pop.end_position)
        self.assertEqual(popped_segment.start_direction, input_segment_to_pop.end_direction)
        self.assertEqual(popped_segment.end_position, segment.end_position)
        self.assertEqual(popped_segment.end_direction, segment.end_direction)
        self.assertEqual(popped_segment.d, "M 10.0000 10.0000")


if __name__ == '__main__':
    unittest.main()
