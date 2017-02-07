#!/usr/bin/env python

from .expression import Expression

from . import _import

class ArrayInitializerExpr(Expression):
  def __init__(self, kwargs={}):
    super(ArrayInitializerExpr, self).__init__(kwargs)
    locs = _import()

    # List<Expression> values;
    v = kwargs.get(u'values', {})
    self._values = map(lambda e: locs[e[u'@t']](e) if u'@t' in e else [],
                       v.get(u'@e', [])) if v else []
                
  @property
  def values(self): return self._values
  @values.setter
  def values(self, v): self._values = v
