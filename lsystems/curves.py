import re
from abc import ABC, abstractmethod
import numpy as np

from .lsystem import LSystem
from .turtle import SimpleTurtle


class Curve(ABC):

    lsys: LSystem
    turtle: SimpleTurtle
    filename: str
    postProcessMap: any

    def get_variables(self) -> set:
        return self.lsys.get_variables()

    def get_constants(self) -> set:
        return self.lsys.get_constants()

    def run(self, iters: int, init_str: str = "", writeOutput=False) -> str:
        sequence = self.run_str(iters, init_str)
        if self.postProcessMap is not None:
            sequence = _post_process(sequence, self.postProcessMap)
        filename = None if not writeOutput else self.filename
        return self.turtle.asSvgString(sequence, writeToFilename=filename)

    def run_str(self, iters: int, init_str: str = "") -> str:
        if init_str == "":
            sequence = self.lsys.run(iters)
        else:
            sequence = self.lsys.run_from(init_str, iters)

        return sequence

    @abstractmethod
    def run_curved_str(self, iters: int) -> str:
        return ''

    # returns an svg string
    def run_curved(self, iters: int, writeOutput=False) -> str:
        sequence = self.run_curved_str(iters)
        if self.postProcessMap is not None:
            sequence = _post_process(sequence, self.postProcessMap)
        filename = None if not writeOutput else self.filename
        return self.turtle.asSvgString(sequence, writeToFilename=filename)


class Sierpinski(Curve):

    def __init__(self, size=1000, width=3, filename='sierpinski_curve.svg'):
        self.filename = filename
        self.lsys = LSystem(
            'A -> B - A - B; B -> A + B + A;', start_symbol='A')  # sierpinski-curve
        self.postProcessMap = {'A': 'F', 'B': 'F', 'X': 'F'}
        self.turtle = SimpleTurtle(60, 50, size, width=width)

    def run_curved_str(self, iters) -> str:
        raw_str = self.run_str(iters)
        f_string = _post_process(raw_str, {'A': 'F', 'B': 'F'})
        split_string = _post_process(f_string, {'F': 'XX'})
        return _post_process(split_string, {'X+X': ')', 'X-X': '('})


class Dragon(Curve):

    def __init__(self, size=1000, width=3, filename='dragon_curve.svg'):
        self.filename = filename
        self.lsys = LSystem('F -> F + G; G -> F - G;', start_symbol='F')  # dragon-curve
        self.postProcessMap = {'F': 'F', 'G': 'F', 'X': 'F'}
        self.turtle = SimpleTurtle(90, 50, size, width=width)

    def run_curved_str(self, iters) -> str:
        raw_str = self.run_str(iters)
        f_string = _post_process(raw_str, {'G': 'F'})
        split_string = _post_process(f_string, {'F': 'XX'})
        return _post_process(split_string, {'X+X': ')', 'X-X': '('})


class Hilbert(Curve):

    def __init__(self, size=1000, width=3):
        self.filename = 'hilbert_curve.svg'
        self.lsys = LSystem('A -> +BF-AFA-FB+; B -> -AF+BFB+FA-;', start_symbol='A')  # hilbert-curve
        self.postProcessMap = {'A': '', 'B': ''}
        self.turtle = SimpleTurtle(90, 10, size, width=width)

    def run_curved_str(self, iters) -> str:
        raw_str = self.run_str(iters)
        f_string = _post_process(raw_str, {'A': '', 'B': '', '+-': '', '-+': ''})
        split_string = _post_process(f_string, {'F': 'XX'})
        curved_string = _post_process(split_string, {'X+X': ')', 'X-X': '('})
        return _post_process(curved_string, {'X': 'F'})


# Peano-curve with middle removed
class FractalPeano(Curve):

    def __init__(self, size=1000, width=3):
        self.filename = 'fractal_peano_curve.svg'
        self.lsys = LSystem(
            'A -> AFBFA-F-BFCFB+F+AFBFA; B -> BFAFB+F+AFDFA-F-BFAFB; C -> CODOC-O-DOCOD+O+CODOC; D -> DOCOD+O+COCOC-O-DOCOD;',
            start_symbol='A')  # peano-curve
        self.postProcessMap = {'A': '', 'B': '', 'C': '', 'D': ''}
        self.turtle = SimpleTurtle(90, 10, size, width=width)

    def run_curved_str(self, iters) -> str:
        raw_str = self.run_str(iters)
        f_string = _post_process(
            raw_str, {'A': '', 'B': '', 'C': '', 'D': '', '+-': '', '-+': ''})
        trimmed_string = _post_process(f_string, {'FO': 'OO', 'OF': 'OO'})
        split_string = _post_process(trimmed_string, {'F': 'XX', 'O': 'YY'})
        curved_string = _post_process(split_string, {'X+X': ')', 'X-X': '('})
        return _post_process(curved_string, {'X': 'F', 'Y': 'O'})


class Hendragon(Curve):

    def __init__(self, size=1000, width=3):
        self.filename = 'hendragon_curve.svg'
        rules = \
            "M -> lFrFRFMFLFlFr;" + \
            "l -> lFRFrFLFlFlFr;" + \
            "r -> rFLFlFRFrFrFl;" + \
            "L -> rFlFLFRFLFlFr;" + \
            "R -> lFrFRFLFRFrFl;"
        self.lsys = LSystem(rules, start_symbol='M')
        self.postProcessMap = {'l': 'L', 'r': 'R', 'M': '', 'F': 'F', '+': 'L', '-': 'R'}
        self.turtle = SimpleTurtle(
            60,
            10,
            size,
            width
        )

    def run_str(self, iters: int) -> str:
        curve_str = self.lsys.run(iters)
        return _post_process(curve_str, {'L': 'll', 'R': 'rr'})

    def run_curved_str(self, iters) -> str:
        return self.run_str(iters)


class Hendragon2(Curve):

    def __init__(self, size=1000, width=3):
        self.filename = 'hendragon2_curve.svg'

        rules = \
            "M -> MRrLllr;" + \
            "r -> MrRMLlr;" + \
            "R -> MrrRlLr;" + \
            "l -> rRLlllr;" + \
            "Ll-> rRLlllMlRrLllr;" + \
            "Lr-> rRLlllMrLlRrrl;" + \
            "LR-> rRLlllMMLRrrrl;"

        self.lsys = LSystem(rules, start_symbol='rrrrRLR')
        self.postProcessMap = {'F': 'F', '+': 'L', '-': 'R'}
        self.turtle = SimpleTurtle(
            60,
            5,
            size,
            width
        )

    def run_str(self, iters: int) -> str:
        curve_str = self.lsys.run(iters)
        post_str = _post_process(curve_str, {
            'M': 'FF',
            'r': 'F-F',
            'l': 'F+F',
            'R': 'F--F',
            'L': 'F++F'
        })
        return post_str[1:-1]+'FF'

    def run_curved_str(self, iters) -> str:
        return self.run_str(iters)


def _post_process(curve_string: str, replacements: dict) -> str:
    pattern = re.compile('|'.join([re.escape(x) for x in replacements.keys()]))
    return pattern.sub(lambda x: replacements[x.group(0)], curve_string)


# returns an svg-string
def draw_random_curve(seed: int, curve: Curve, iters: int) -> str:
    vars = curve.get_variables()
    consts = curve.get_constants()
    rng = np.random.default_rng(seed)
    random_string = ''.join(list(rng.choice(list(vars) + list(consts), iters)))
    return curve.run_from(random_string, iters=iters)
