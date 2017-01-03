#!/usr/bin/env python

from .literalexpr import LiteralExpr
from ..type.primitivetype import PrimitiveType

class BooleanLiteralExpr(LiteralExpr):
  def __init__(self, kwargs={}):
    super(BooleanLiteralExpr, self).__init__(kwargs)

    # boolean value
    self._value = str(kwargs.get(u'value', False)).lower()
                
  @property
  def value(self): return self._value
  @value.setter
  def value(self, v): self._value = v

  @property
  def typee(self): return PrimitiveType({u'type': {u'name':u'boolean'}})
  @typee.setter
  def typee(self, v): self._type = v
