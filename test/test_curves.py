import curves

def test_postprocess():
  d = curves.Dragon()
  raw_str = d.run_str(3)
  assert(raw_str == 'F+G+F-G+F+G-F-G')

  curved_str = '(+)+(-)'
  assert(d.run_curved(3) == curved_str)