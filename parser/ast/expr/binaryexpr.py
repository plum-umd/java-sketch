#!/usr/bin/env python

from .expression import Expression

from . import _import

class BinaryExpr(Expression):
  def __init__(self, kwargs={}):
    super(BinaryExpr, self).__init__(kwargs)
    locs = _import()

    # Expression left
    left = kwargs.get(u'left', {})
    self._left = locs[left[u'@t']](left) if left else None

    # Expression right
    right = kwargs.get(u'right', {})
    self._right = locs[right[u'@t']](right) if right else None
    
    # Operator op;
    self._op = kwargs.get(u'op', {}).get(u'name')
                
  @property
  def left(self): return self._left
  @left.setter
  def left(self, v): self._left = v

  @property
  def right(self): return self._right
  @right.setter
  def right(self, v): self._right = v

  @property
  def op(self): return self._op
  @op.setter
  def op(self, v): self._op = v

  @property
  def typee(self): return self._right.typee
  @typee.setter
  def typee(self, v): self._type = v
