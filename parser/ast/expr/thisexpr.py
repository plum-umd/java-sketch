#!/usr/bin/env python

from .expression import Expression

class ThisExpr(Expression):
  def __init__(self, kwargs={}):
    super(ThisExpr, self).__init__(kwargs)

    # Expression classExpr
    self._classExpr = kwargs.get(u'classExpr', None)

  @property
  def classExpr(self): return self._classExpr
  @classExpr.setter
  def classExpr(self, v): self._classExpr = v
