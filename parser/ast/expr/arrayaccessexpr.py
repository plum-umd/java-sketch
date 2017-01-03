#!/usr/bin/env python

from .expression import Expression

from . import _import

class ArrayAccessExpr(Expression):
  def __init__(self, kwargs={}):
    super(ArrayAccessExpr, self).__init__(kwargs)
    locs = _import()

    #Expression name;
    n = kwargs.get(u'name', {})
    self._name = locs[n[u'@t']](n) if n else None

    #Expression index;
    i = kwargs.get(u'index', {})
    self._index = locs[i[u'@t']](i) if i else None
               
  @property
  def name(self): return self._name.name
  @name.setter
  def name(self, v): self._name = v

  @property
  def nameExpr(self): return self._name

  @property
  def index(self): return self._index
  @index.setter
  def index(self, v): self._index = v

  @property
  def lbl(self): return (self._name.name, self.ati)
  @lbl.setter
  def lbl(self, v): self._lbl = v
