import svgwrite
from .svg import PathSegment, Line, Rotation, Arc


class Turtle:
    def __init__(self, movementMap, width=600, height=400, stroke=3, startDirection=0) -> None:
        self.movementMap = movementMap
        self.stroke = stroke
        self.width = width
        self.height = height
        self.startDirection = -startDirection  # negative, because svg y axis goes down

    def _toDrawing(self, sequence):
        path = svgwrite.path.Path(fill="none")
        path.stroke(color="black", width=self.stroke,
                    linecap="round", linejoin="round")

        xmin = 0
        xmax = 0
        ymin = 0
        ymax = 0
        segment = PathSegment(
            startPosition=(0, 0),
            startDirection=self.startDirection,
            endPosition=(0, 0),
            endDirection=self.startDirection,
            d="M 0 0"
        )
        path.push("M 0 0")

        for char in sequence:
            if char not in self.movementMap:
                raise Exception(f"{char} not defined in movement map")

            movement = self.movementMap[char]
            segment = movement.generate(previousSegment=segment)
            path.push(segment.d)
            xmin = min(xmin, segment.endPosition[0])
            xmax = max(xmax, segment.endPosition[0])
            ymin = min(ymin, segment.endPosition[1])
            ymax = max(ymax, segment.endPosition[1])

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
        svg = self._toDrawing(sequence)
        if writeToFilename is not None:
            svg.saveas(writeToFilename)
        return svg.tostring()


class SimpleTurtle(Turtle):
    def __init__(self, angle, stride, size, width=3):
        movementMap = {
            "O": Line(length=stride, draw=False),
            "F": Line(length=stride),
            "+": Rotation(angle=angle),
            "-": Rotation(angle=-angle),
            "L": Rotation(angle=angle),
            "R": Rotation(angle=-angle),
            ")": Arc(angle=angle, rx=stride, ry=stride),
            "(": Arc(angle=-angle, rx=stride, ry=stride)
        }
        super().__init__(movementMap, width=size, height=size, stroke=width)
