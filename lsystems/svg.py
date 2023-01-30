from abc import ABC, abstractmethod
from math import sin, cos, radians, tan, atan, pi


class Cursor:
    x: float
    y: float
    dir: float

    def __init__(self, x: float, y: float, dir: float):
        self.x = x
        self.y = y
        self.dir = dir

    def __eq__(self, other):
        return abs(self.x - other.x) < 1e-10 and \
            abs(self.y - other.y) < 1e-10 and \
            abs(self.dir - other.dir) < 1e-10

    def __str__(self):
        return f"Cursor(x={self.x:0.4f}, y={self.y:0.4f}, dir={self.dir:0.4f})"


class Movement(ABC):
    @abstractmethod
    def generate(self, previous_cursor: Cursor) -> tuple[str, Cursor]:
        pass


class Line(Movement):
    def __init__(self, length, draw=True):
        self.length = length
        self.draw = draw

    def generate(self, start_cursor):
        rad = radians(start_cursor.dir)
        x_end = start_cursor.x + self.length*cos(rad)
        y_end = start_cursor.y + self.length*sin(rad)
        cmd = "L" if self.draw else "M"
        d = f"{cmd} {x_end:0.4f} {y_end:0.4f}"

        end_cursor = Cursor(x_end, y_end, start_cursor.dir)
        return (d, end_cursor)


class Rotation(Movement):
    def __init__(self, angle):
        # negative because in svg the y axis goes down, not up
        self.angle = -angle

    def generate(self, start_cursor):
        d = ""
        end_cursor = Cursor(
            x=start_cursor.x,
            y=start_cursor.y,
            dir=start_cursor.dir+self.angle
        )

        return d, end_cursor


class Arc(Movement):
    def __init__(self, angle, rx, ry=None):
        self.rx = rx
        self.ry = ry if ry is not None else rx
        # negative because in svg the y axis goes down, not up
        self.angle = -angle
        if self.angle == 0 or self.angle > 360 or self.angle < -360:
            raise Exception(
                f"{angle} needs in interval [-360, 360], but not 0")

    def generate(self, start_cursor):
        x = start_cursor.x
        y = start_cursor.y
        dir = start_cursor.dir
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
        end_cursor = Cursor(x=x_end, y=y_end, dir=dir+self.angle)
        return d, end_cursor


class PushPosition(Movement):
    """["""

    def __init__(self, stack: list):
        self.stack = stack

    def generate(self, start_cursor):
        self.stack.append(start_cursor)

        return "", start_cursor


class PopPosition(Movement):
    """]"""

    def __init__(self, stack: list):
        self.stack = stack

    def generate(self, start_cursor):
        if len(self.stack) == 0:
            raise Exception("PopPosition without corresponding PushPosition found")

        saved_cursor = self.stack.pop()
        d = f"M {saved_cursor.x:0.4f} {saved_cursor.y:0.4f}"

        return d, saved_cursor
