#!/usr/bin/env python

from .literalexpr import LiteralExpr

from ..type.referencetype import ReferenceType

class StringLiteralExpr(LiteralExpr):
  def __init__(self, kwargs={}):
    super(StringLiteralExpr, self).__init__(kwargs)

    # Expression value
    self._value = kwargs.get(u'value', '')

    self.add_as_parent([self.typee])
    
  @property
  def value(self): return self._value
  @value.setter
  def value(self, v): self._value = v

  @property
  def typee(self):
    return ReferenceType({u'type': {u'@t':u'ClassOrInterfaceType', u'name': u'String'}})
  @typee.setter
  def typee(self, v): pass
