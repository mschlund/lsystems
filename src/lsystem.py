import re
#rules dict: V->replacement

class LSystem:
  def _parse_spec(self, spec: str) -> dict:
    rule_dict = {}
    one_line_spec = "".join(spec.splitlines())
    rules = one_line_spec.split(';')
    for r in filter(None, rules):
      parts = r.split('->')
      var = parts[0].replace(' ', '')
      tail = parts[1].replace(' ', '')
      rule_dict[var] = tail
    return rule_dict

  def __init__(self, spec: str, start_symbol: str):
    self.start_symbol = start_symbol
    self.rules = self._parse_spec(spec)

  def run(self, number_of_iterations: int):
    current_string = self.start_symbol
    i=0
    while i < number_of_iterations:
      # https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
      # in each iteration, we have to apply all rules at once!
      pattern = re.compile('|'.join([re.escape(x) for x in self.rules.keys()]))
      current_string = pattern.sub(lambda x: self.rules[x.group(0)], current_string)
      i += 1
    return current_string  
