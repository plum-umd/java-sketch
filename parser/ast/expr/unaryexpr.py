#!/usr/bin/env python

from .expression import Expression

from . import _import


class UnaryExpr(Expression):
  PRE_OPS = {u'positive':u'+', u'negative':u'-', u'preIncrement':u'++',
             u'preDecrement':u'--', u'not':u'!', u'inverse':u'~'}
  POST_OPS = {u'posIncrement':u'++', u'posDecrement':u'--'}
  def __init__(self, kwargs={}):
    super(UnaryExpr, self).__init__(kwargs)
    locs = _import()

    # Expression expr
    e = kwargs.get(u'expr', {})
    self._expr = locs[e[u'@t']](e) if e else None

    # Operator op;
    self._op = kwargs.get(u'op', {}).get(u'name')
                
  @property
  def expr(self): return self._expr
  @expr.setter
  def expr(self, v): self._expr = v

  @property
  def op(self): return self._op
  @op.setter
  def op(self, v): self._op = v
