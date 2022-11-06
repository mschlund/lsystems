import re
from abc import ABC
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

  def get_svg(self, iters: int) -> str:
    self.turtle.draw(self.startpoint+self.lsys.run(iters))
    return self.turtle.to_svg()

  def run_from(self, init_str: str, iters: int) -> str:
    self.turtle.draw(self.run_str_from(init_str, iters))
    return self.turtle.to_svg()

  def run(self, iters: int) -> str:
    self.turtle.draw(self.run_str(iters))
    return self.turtle.to_svg()

  def run_str(self, iters: int) -> str:
    return self.lsys.run(iters)

  def run_str_from(self, init_str: str, iters: int) -> str:
    return self.lsys.run_from(init_str, iters)

class Sierpinski(Curve):

  def __init__(self):
    self.lsys = ls.LSystem('A -> B - A - B; B -> A + B + A;', start_symbol='A') # sierpinski-curve
    self.turtle = mt.Turtle('sierpinski_curve.svg', {'A': 'F', 'B': 'F', '+': 'L', '-': 'R', 'O': 'O'}, 60, 50, 2000)
    self.startpoint = '---'+'O'*8+'+++'+'--'+'O'*5+'+++'


class Dragon(Curve):

  def __init__(self):
    self.lsys = ls.LSystem('F -> F + G; G -> F - G;', start_symbol='F') # dragon-curve
    self.turtle = mt.Turtle('dragon_curve.svg', {'F': 'F', 'G': 'F', '+': 'L', '-': 'R', 'O': 'O'}, 90, 50, 1000)
    self.startpoint = ''

  def run_curved_str(self, iters) -> str:
    raw_str = self.lsys.run(iters)    
    f_string = post_process(raw_str, {'G' : 'F'})
    return post_process(f_string, {'F+F' : '(', 'F-F' : ')'})

  def run_curved(self, iters):
    self.turtle.draw(self.run_curved_str(iters))
    return self.turtle.to_svg()

def post_process(curve_string: str, replacements: dict) -> str:
  pattern = re.compile('|'.join([re.escape(x) for x in replacements.keys()]))
  return pattern.sub(lambda x: replacements[x.group(0)], curve_string)


# returns an svg-string
def draw_random_curve(seed: int, curve: Curve, iters: int) -> str:
  vars = curve.get_variables()
  consts = curve.get_constants()
  rng = np.random.default_rng(seed)
  random_string = ''.join(list(rng.choice(list(vars) + list(consts), iters)))
  return curve.run_from(random_string, iters=iters)
