from abc import ABC, abstractmethod
import svg_turtle as st
from math import sin, cos, radians, tan, atan, pi
import svgwrite


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


class PathSegment:
    """
    represents a segment of a svg path
    the start position and start direction (in degree) can be seen as assumptions,
    which should be met by the previous segment to assure the end position and
    end direction. The d contains the path segment as string representation as
    it is required by the svg path tag. The coordinates in d should be absolute.
    """

    def __init__(self,
                 startPosition: tuple[float, float],
                 startDirection: float,
                 endPosition: float,
                 endDirection: float,
                 d: str
                 ):
        self.startPosition = startPosition
        self.startDirection = startDirection
        self.endPosition = endPosition
        self.endDirection = endDirection
        self.d = d


class Movement(ABC):
    @abstractmethod
    def generate(self, previousSegment: PathSegment) -> PathSegment:
        pass


class Line(Movement):
    def __init__(self, length, draw=True):
        self.length = length
        self.draw = draw

    def generate(self, previousSegment):
        x, y = previousSegment.endPosition
        dir = previousSegment.endDirection
        rad = radians(dir)
        xEnd = x + self.length*cos(rad)
        yEnd = y + self.length*sin(rad)
        cmd = "L" if self.draw else "M"
        d = f"{cmd} {xEnd:0.4f} {yEnd:0.4f}"
        return PathSegment(
            startPosition=(x, y),
            startDirection=dir,
            endPosition=(xEnd, yEnd),
            endDirection=dir,
            d=d
        )


class Rotation(Movement):
    def __init__(self, angle):
        # negative because in svg the y axis goes down, not up
        self.angle = -angle

    def generate(self, previousSegment):
        pos = previousSegment.endPosition
        dir = previousSegment.endDirection
        return PathSegment(
            startPosition=pos,
            startDirection=dir,
            endPosition=pos,
            endDirection=dir+self.angle,
            d=""
        )


class Arc(Movement):
    def __init__(self, angle, rx, ry=None):
        self.rx = rx
        self.ry = ry if ry is not None else rx
        # negative because in svg the y axis goes down, not up
        self.angle = -angle
        if self.angle == 0 or self.angle > 360 or self.angle < -360:
            raise Exception(
                f"{angle} needs in interval [-360, 360], but not 0")

    def generate(self, previousSegment):
        x, y = previousSegment.endPosition
        dir = previousSegment.endDirection
        radDir = radians(dir)
        radAngle = atan(tan(radians(self.angle))*self.rx/self.ry) % (2*pi)
        if abs(self.angle) > 90 and abs(self.angle) < 270:
            radAngle = (radAngle+pi) % (2*pi)
        if self.angle < 0:
            radAngle = radAngle - 2*pi
        dx = self.rx*sin(abs(radAngle))
        # rotation left or right defines where the center of rotation is
        dy = (self.ry - self.ry*cos(radAngle)) * (1 if self.angle > 0 else -1)
        xEnd = x + dx * cos(radDir) - dy * sin(radDir)
        yEnd = y + dx * sin(radDir) + dy * cos(radDir)
        largeArc = 1 if abs(self.angle) > 180 else 0
        sweep = 1 if self.angle > 0 else 0
        d = f"A {self.rx:0.4f} {self.ry:0.4f} {dir} {largeArc} {sweep} {xEnd:0.4f} {yEnd:0.4f}"
        return PathSegment(
            startPosition=(x, y),
            startDirection=dir,
            endPosition=(xEnd, yEnd),
            endDirection=dir+self.angle,
            d=d
        )
