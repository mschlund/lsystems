import svgwrite
from .svg import PathSegment, Line, Rotation, Arc


class Turtle:
    def __init__(self, movement_map, width=600, height=400, stroke=3, start_direction=0) -> None:
        self.movement_map = movement_map
        self.stroke = stroke
        self.width = width
        self.height = height
        self.start_direction = -start_direction  # negative, because svg y axis goes down

    def _to_drawing(self, sequence):
        path = svgwrite.path.Path(fill="none")
        path.stroke(color="black", width=self.stroke,
                    linecap="round", linejoin="round")

        xmin = 0
        xmax = 0
        ymin = 0
        ymax = 0
        segment = PathSegment(
            start_position=(0, 0),
            start_direction=self.start_direction,
            end_position=(0, 0),
            end_direction=self.start_direction,
            d="M 0 0"
        )
        path.push("M 0 0")

        for char in sequence:
            if char not in self.movement_map:
                raise Exception(f"{char} not defined in movement map")

            movement = self.movement_map[char]
            segment = movement.generate(previous_segment=segment)
            path.push(segment.d)
            xmin = min(xmin, segment.end_position[0])
            xmax = max(xmax, segment.end_position[0])
            ymin = min(ymin, segment.end_position[1])
            ymax = max(ymax, segment.end_position[1])

        # add some margin around the path
        viewboxWidth = xmax-xmin+self.width*0.2
        viewboxHeight = ymax-ymin+self.height*0.2
        viewboxX = xmin-self.width*0.1
        viewboxY = ymin-self.height*0.1
        viewbox = f"{viewboxX} {viewboxY} {viewboxWidth} {viewboxHeight}"
        svg = svgwrite.Drawing(
            size=(self.width, self.height),
            viewBox=viewbox
        )
        svg.add(path)
        return svg

    def asSvgString(self, sequence, writeToFilename=None):
        svg = self._to_drawing(sequence)
        if writeToFilename is not None:
            svg.saveas(writeToFilename)
        return svg.tostring()


class SimpleTurtle(Turtle):
    def __init__(self, angle, stride, size, width=3):
        movement_map = {
            "O": Line(length=stride, draw=False),
            "F": Line(length=stride),
            "+": Rotation(angle=angle),
            "-": Rotation(angle=-angle),
            "L": Rotation(angle=angle),
            "R": Rotation(angle=-angle),
            ")": Arc(angle=angle, rx=stride, ry=stride),
            "(": Arc(angle=-angle, rx=stride, ry=stride)
        }
        super().__init__(movement_map, width=size, height=size, stroke=width)
