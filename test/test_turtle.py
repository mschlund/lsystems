import my_turtle as myt
import os

def test_creation():
  outfilename = 'curve.svg'
  t = myt.Turtle(outfilename, {'A': 'F', 'B': 'F'}, 60, 50, 500)
  t.write_output()
  assert(os.path.exists(outfilename)) # TODO: use fakefs!