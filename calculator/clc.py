#!/usr/bin/env python3

import string
import sys

DEBUG = False


class Node:

  def __init__(self, op, val=None, rchild=None, lchild=None):
    self._op = op
    self._val = val
    self._lchild = lchild
    self._rchild = rchild

  def eval(self):
    if self._val is not None:
      return self._val
    assert (
        self._lchild is not None and self._rchild is not None
    ), 'f{self._val, self._op, self._lchild, self._rchild}'

    l, r = self._lchild.eval(), self._rchild.eval()
    if self._op == '*':
      return l * r
    elif self._op == '/':
      return l / r
    elif self._op == '+':
      return l + r
    elif self._op == '-':
      return l - r

  def print(self, n=0):
    if self._rchild:
      self._rchild.print(n + 4)
    if self._op:
      print(' ' * n + self._op + ' ' * 2)
    if self._val is not None:
      print(' ' * n + str(self._val) + ' ' * 2)
    if self._lchild:
      self._lchild.print(n + 4)


class Calculator:

  def tokenize(self, s):
    tokens = []
    i = 0
    while i < len(s):
      if s[i].isspace():
        i += 1
      elif s[i] in ('(', ')', '+', '-', '*', '/'):
        tokens.append(s[i])
        i += 1
      elif s[i] in string.digits:
        start = i
        while i < len(s) and s[i] in string.digits:
          i += 1
        tokens.append(s[start:i])
      else:
        assert False, f'Error: unknown char f{s[i]}'
    return tokens

  def AST(self, tokens):
    opS = []
    valS = []
    num_val_before_neg_sign = (
        0  # use it to detect -n or (-n) to convert them to 0-n or (0-n)
    )
    for t in tokens:
      if t == '(':
        opS.append(t)
        num_val_before_neg_sign = 0
      elif t == ')':
        while opS[-1] != '(':
          op = opS.pop()
          r = valS.pop()
          l = valS.pop()
          valS.append(Node(op, None, r, l))
        opS.pop()
        num_val_before_neg_sign = 1
      elif t == '+':
        while len(opS) > 0 and opS[-1] in ('+', '-', '*', '/'):
          op = opS.pop()
          r = valS.pop()
          l = valS.pop()
          valS.append(Node(op, None, r, l))
        opS.append(t)
        num_val_before_neg_sign = 0
      elif t == '-':
        while len(opS) > 0 and opS[-1] in ('+', '-', '*', '/'):
          op = opS.pop()
          r = valS.pop()
          l = valS.pop()
          valS.append(Node(op, None, r, l))
        if num_val_before_neg_sign == 0:
          valS.append(Node(None, 0, None, None))  # turn -2 to 0-2
        opS.append(t)
      elif t == '/' or t == '*':
        while len(opS) > 0 and opS[-1] in ('*', '/'):
          op = opS.pop()
          r = valS.pop()
          l = valS.pop()
          valS.append(Node(op, None, r, l))
        opS.append(t)
      else:
        # value
        valS.append(Node(None, int(t), None, None))
        num_val_before_neg_sign = 1
    assert len(valS) == 1
    return valS.pop()

  def calculate(self, s: str) -> int:
    tokens = self.tokenize('(' + s + ')')
    ast = self.AST(tokens)
    if DEBUG:
      print(tokens)
      ast.print()
    return ast.eval()


if __name__ == '__main__':
  c = Calculator()
  for line in sys.stdin:
    print(c.calculate(line))
