#!/usr/bin/env python

from .stringliteralexpr import StringLiteralExpr
from ..type.primitivetype import PrimitiveType

class IntegerLiteralExpr(StringLiteralExpr):
  def __init__(self, kwargs={}):
    super(IntegerLiteralExpr, self).__init__(kwargs)
    #  String UNSIGNED_MIN_VALUE = "2147483648";
    self._UNSIGNED_MIN_VALUE = "2147483648"
    #  String MIN_VALUE = "-" + self._UNSIGNED_MIN_VALUE;
    self._MIN_VALUE = "-" + self._UNSIGNED_MIN_VALUE
    self._value = kwargs.get(u'value')
                
  @property
  def UNSIGNED_MIN_VALUE(self): return self._UNSIGNED_MIN_VALUE
  @UNSIGNED_MIN_VALUE.setter
  def UNSIGNED_MIN_VALUE(self, v): self._UNSIGNED_MIN_VALUE = v

  @property
  def MIN_VALUE(self): return self._MIN_VALUE
  @MIN_VALUE.setter
  def MIN_VALUE(self, v): self._MIN_VALUE = v

  @property
  def value(self): return self._value
  @value.setter
  def value(self, v): self._value = v

  # Maybe this is wonky, but I'm going to make the name of an
  # IntegerLiteralExpr the same as it's name.
  @property
  def name(self): return self._value
  @name.setter
  def name(self, v): self._value = v

  @property
  def in_set(self): return set([])
  @in_set.setter
  def in_set(self, v): pass

  @property
  def out_set(self): return set([])
  @out_set.setter
  def out_set(self, v): pass

  @property
  def typee(self): return PrimitiveType({u'type': {u'name': u'int'}})
  @typee.setter
  def typee(self, v): pass
