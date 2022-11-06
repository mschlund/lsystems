import lsystem

sierpinski_spec = 'A -> B - A - B; B -> A + B + A;'

def test_sierpinski():
  L = lsystem.LSystem(sierpinski_spec, start_symbol='A')
  assert(L.run(0) == 'A')
  assert(L.run(1) == 'B-A-B')
  assert(L.run(2) == 'A+B+A-B-A-B-A+B+A')

def test_get():
  L = lsystem.LSystem(sierpinski_spec, start_symbol='A')
  assert(L.get_variables() == set(['A', 'B']))
  assert(L.get_constants() == set(['+', '-']))

def test_run_from_different_start():
  L = lsystem.LSystem(sierpinski_spec, start_symbol='A')
  assert(L.run_from('AA', 1) == 'B-A-BB-A-B')
