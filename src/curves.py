import re
from abc import ABC, abstractmethod
import numpy as np

import lsystem as ls
import my_turtle as mt


class Curve(ABC):

  lsys : ls.LSystem
  turtle : mt.Turtle
  startpoint : str

  def get_variables(self) -> set:
    return self.lsys.get_variables()

  def get_constants(self) -> set:
    return self.lsys.get_constants()

  def run_svg(self, iters: int) -> str:
    self.turtle.draw(self.run_str(iters))
    return self.turtle.to_svg()

  def write_output(self, iters: int):
    self.turtle.draw(self.startpoint+self.run_str(iters))
    return self.turtle.write_output()

  def run_svg_from(self, init_str: str, iters: int) -> str:
    self.turtle.draw(self.startpoint+self.run_str_from(init_str, iters))
    return self.turtle.to_svg()

  def run_str(self, iters: int) -> str:
    return self.startpoint + self.lsys.run(iters)

  def run_str_from(self, init_str: str, iters: int) -> str:
    return self.startpoint + self.lsys.run_from(init_str, iters)

  @abstractmethod # already includes the start-string
  def run_curved_str(self, iters: int) -> str:
    return ''

  # returns an svg string
  def run_curved_svg(self, iters) -> str:
    self.turtle.draw(self.run_curved_str(iters))
    return self.turtle.to_svg()

  def write_output(self):
    self.turtle.write_output()


class Sierpinski(Curve):

  def __init__(self, size=1500, start = '', width=3):
    self.lsys = ls.LSystem('A -> B - A - B; B -> A + B + A;', start_symbol='A') # sierpinski-curve
    self.turtle = mt.Turtle('sierpinski_curve.svg', {'A': 'F', 'B': 'F', 'X': 'F'}, 60, 50, size, width=width)
    self.startpoint = start

  def run_curved_str(self, iters) -> str:
    raw_str = self.startpoint + self.lsys.run(iters)
    f_string = _post_process(raw_str, {'A' : 'F', 'B': 'F'})
    split_string = _post_process(f_string, {'F' : 'XX'})
    return _post_process(split_string, {'X+X' : ')', 'X-X': '('})

class Dragon(Curve):

  def __init__(self, size=1000, start='', width=3):
    self.lsys = ls.LSystem('F -> F + G; G -> F - G;', start_symbol='F') # dragon-curve
    self.turtle = mt.Turtle('dragon_curve.svg', {'F': 'F', 'G': 'F', 'X': 'F'}, 90, 50, size, width=width)
    self.startpoint = start

  def run_curved_str(self, iters) -> str:
    raw_str = self.lsys.run(iters)    
    f_string = _post_process(raw_str, {'G' : 'F'})
    split_string = _post_process(f_string, {'F' : 'XX'})
    return _post_process(split_string, {'X+X' : ')', 'X-X': '('})


class Hilbert(Curve):

  def __init__(self, size=1000, start = '', width=3):
    self.lsys = ls.LSystem('A -> +BF-AFA-FB+; B -> -AF+BFB+FA-;', start_symbol='A') # hilbert-curve
    self.turtle = mt.Turtle('hilbert_curve.svg', {'A': '', 'B': ''}, 90, 10, size, width=width)
    self.startpoint = start

  def run_curved_str(self, iters) -> str:
    raw_str = self.lsys.run(iters)
    f_string = _post_process(raw_str, {'A' : '', 'B': '', '+-': '', '-+':''})
    split_string = _post_process(f_string, {'F' : 'XX'})
    curved_string = _post_process(split_string, {'X+X' : ')', 'X-X': '('})
    return _post_process(curved_string, {'X' : 'F'})


# Peano-curve with middle removed
class FractalPeano(Curve):

  def __init__(self, size=1000, start = '', width=3):
    self.lsys = ls.LSystem('A -> AFBFA-F-BFCFB+F+AFBFA; B -> BFAFB+F+AFDFA-F-BFAFB; C -> CODOC-O-DOCOD+O+CODOC; D -> DOCOD+O+COCOC-O-DOCOD;', start_symbol='A') # peano-curve
    self.turtle = mt.Turtle('fractal_peano_curve.svg', {'A': '', 'B': '', 'C': '', 'D': ''}, 90, 10, size, width=width)
    self.startpoint = start

  def run_curved_str(self, iters) -> str:
    raw_str = self.lsys.run(iters)
    f_string = _post_process(raw_str, {'A' : '', 'B': '', 'C': '', 'D': '', '+-': '', '-+':''})
    trimmed_string = _post_process(f_string, {'FO': 'OO', 'OF': 'OO'})
    split_string = _post_process(trimmed_string, {'F' : 'XX', 'O': 'YY'})
    curved_string = _post_process(split_string, {'X+X' : ')', 'X-X': '('})
    return self.startpoint + _post_process(curved_string, {'X' : 'F', 'Y': 'O'})



class Hendragon(Curve):

  def __init__(self, size=1000, start = '', width=3):
    rules = \
      "M -> lFrFRFMFLFlFr;" + \
      "l -> lFRFrFLFlFlFr;" + \
      "r -> rFLFlFRFrFrFl;" + \
      "L -> rFlFLFRFLFlFr;" + \
      "R -> lFrFRFLFRFrFl;"
    self.lsys = ls.LSystem(rules, start_symbol='M')
    self.turtle = mt.Turtle(
      'hendragon_curve.svg',
      {'l': 'L', 'r': 'R', 'M': '', 'F': 'F', '+': 'L', '-': 'R'},
      60,
      10,
      size,
      width
    )
    self.startpoint = start

  def run_str(self, iters: int) -> str:
    curve_str = self.startpoint+self.lsys.run(iters)
    return _post_process(curve_str, {'L': 'll', 'R': 'rr'})
  
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
