import unittest

import clc


class TestCalculator(unittest.TestCase):
  longMessage = True


def run_test(self, expr, want):
  got = clc.Calculator().calculate(expr)
  self.assertEqual(got, want, f"Expression: {expr}, Want: {want}, Got: {got}")


def create_tests():
  test_cases = [
      ("2+3", 5),
      ("2-3+4", 3),
      ("2+(-2*3)", -4),
      ("(5*6)-2", 28),
      ("10/2/5", 1),
      ("-1*3", -3),
      ("-(-1+1)+1", 1),
      # Add more test cases
  ]
  for e, w in test_cases:
    test_name = f"test_expression_{e}"
    test_method = lambda self, expr=e, want=w: run_test(self, expr, want)
    setattr(TestCalculator, test_name, test_method)


if __name__ == "__main__":
  create_tests()
  unittest.main()
