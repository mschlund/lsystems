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
                 start_position: tuple[float, float],
                 start_direction: float,
                 end_position: tuple[float, float],
                 end_direction: float,
                 d: str
                 ):
        self.start_position = start_position
        self.start_direction = start_direction
        self.end_position = end_position
        self.end_direction = end_direction
        self.d = d


class Movement(ABC):
    @abstractmethod
    def generate(self, previous_segment: PathSegment) -> PathSegment:
        pass


class Line(Movement):
    def __init__(self, length, draw=True):
        self.length = length
        self.draw = draw

    def generate(self, previous_segment):
        x, y = previous_segment.end_position
        dir = previous_segment.end_direction
        rad = radians(dir)
        x_end = x + self.length*cos(rad)
        y_end = y + self.length*sin(rad)
        cmd = "L" if self.draw else "M"
        d = f"{cmd} {x_end:0.4f} {y_end:0.4f}"
        return PathSegment(
            start_position=(x, y),
            start_direction=dir,
            end_position=(x_end, y_end),
            end_direction=dir,
            d=d
        )


class Rotation(Movement):
    def __init__(self, angle):
        # negative because in svg the y axis goes down, not up
        self.angle = -angle

    def generate(self, previous_segment):
        pos = previous_segment.end_position
        dir = previous_segment.end_direction
        return PathSegment(
            start_position=pos,
            start_direction=dir,
            end_position=pos,
            end_direction=dir+self.angle,
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

    def generate(self, previous_segment):
        x, y = previous_segment.end_position
        dir = previous_segment.end_direction
        rad_dir = radians(dir)
        rad_angle = atan(tan(radians(self.angle))*self.rx/self.ry) % (2*pi)
        if abs(self.angle) > 90 and abs(self.angle) < 270:
            rad_angle = (rad_angle+pi) % (2*pi)
        if self.angle < 0:
            rad_angle = rad_angle - 2*pi
        dx = self.rx*sin(abs(rad_angle))
        # rotation left or right defines where the center of rotation is
        dy = (self.ry - self.ry*cos(rad_angle)) * (1 if self.angle > 0 else -1)
        x_end = x + dx * cos(rad_dir) - dy * sin(rad_dir)
        y_end = y + dx * sin(rad_dir) + dy * cos(rad_dir)
        large_arc = 1 if abs(self.angle) > 180 else 0
        sweep = 1 if self.angle > 0 else 0
        d = f"A {self.rx:0.4f} {self.ry:0.4f} {dir} {large_arc} {sweep} {x_end:0.4f} {y_end:0.4f}"
        return PathSegment(
            start_position=(x, y),
            start_direction=dir,
            end_position=(x_end, y_end),
            end_direction=dir+self.angle,
            d=d
        )


class PushPosition(Movement):
    """["""

    def __init__(self, stack: list):
        self.stack = stack

    def generate(self, previous_segment):
        pos = previous_segment.end_position
        dir = previous_segment.end_direction
        self.stack.append((pos, dir))
        
        return PathSegment(
            start_position=pos,
            start_direction=dir,
            end_position=pos,
            end_direction=dir,
            d=""
        )


class PopPosition(Movement):
    """]"""

    def __init__(self, stack: list):
        self.stack = stack

    def generate(self, previous_segment):
        if len(self.stack) == 0:
            raise Exception("PopPosition without corresponding PushPosition found")

        pos, dir = self.stack.pop()
        d = f"M {pos[0]:0.4f} {pos[1]:0.4f}"

        return PathSegment(
            start_position=previous_segment.end_position,
            start_direction=previous_segment.end_direction,
            end_position=pos,
            end_direction=dir,
            d=d
        )
