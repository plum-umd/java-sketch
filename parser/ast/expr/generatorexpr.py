#!/usr/bin/env python

from .expression import Expression

from . import _import

class GeneratorExpr(Expression):
  def __init__(self, kwargs={}):
    super(GeneratorExpr, self).__init__(kwargs)
    locs = _import()

    self._isHole = kwargs.get(u'isHole', False)
    # List Expression
    exprs = kwargs.get(u'exprs', {})
    self._exprs = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                      exprs.get(u'@e', [])) if exprs else []
                
  @property
  def isHole(self): return self._isHole
  @isHole.setter
  def isHole(self, v): self._isHole = v

  @property
  def exprs(self): return self._exprs
  @exprs.setter
  def exprs(self, v): self._exprs = v
