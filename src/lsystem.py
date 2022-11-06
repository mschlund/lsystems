import re
#rules dict: V->replacement
from typing import Tuple

class LSystem:
  def _parse_spec(self, spec: str) -> Tuple[dict, set, set]:
    rule_dict = {}
    vars = set([])
    all_elements = set([])
    one_line_spec = "".join(spec.splitlines())
    rules = one_line_spec.split(';')
    for r in filter(None, rules):
      parts = r.split('->')
      var = parts[0].replace(' ', '')
      vars.add(var)
      all_elements.add(var)
      tail = parts[1].replace(' ', '')
      all_elements = all_elements.union(tail) # "tail" is a list of characters
      rule_dict[var] = tail
    return rule_dict, vars, all_elements.difference(vars)

  def __init__(self, spec: str, start_symbol: str):
    self.start_symbol = start_symbol
    self.rules, self.variables, self.constants = self._parse_spec(spec)

  def run_from(self, initial_string: str, number_of_iterations: int) -> str:
    current_string = initial_string
    i=0
    while i < number_of_iterations:
      # https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
      # in each iteration, we have to apply all rules at once!
      pattern = re.compile('|'.join([re.escape(x) for x in self.rules.keys()]))
      current_string = pattern.sub(lambda x: self.rules[x.group(0)], current_string)
      i += 1
    return current_string

  def run(self, number_of_iterations: int) -> str:
    return self.run_from(initial_string=self.start_symbol, number_of_iterations=number_of_iterations)

  def get_variables(self) -> set:
    return self.variables

  def get_constants(self) -> set:
    return self.constants
