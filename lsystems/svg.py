from abc import ABC, abstractmethod
from math import sin, cos, radians, tan, atan, pi


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
