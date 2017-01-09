#!/usr/bin/env python

from ..node import Node
from . import _import

class VariableDeclarator(Node):
  def __init__(self, kwargs={}):
    if kwargs.get(u'id', ''):
      super(VariableDeclarator, self).__init__(kwargs)
      locs = _import()

      # VariableDeclaratorId
      self._id = locs[u'VariableDeclaratorId'](kwargs.get(u'id', ''))

      # Expression
      i = kwargs.get('init', None)
      self._init = locs[i[u'@t']](i) if i else None
      if self._init and not self.typee:
        self._init.typee = self.parentNode.typee
      
  @property
  def idd(self): return self._id
  @idd.setter
  def idd(self, v): self._id = v

  @property
  def name(self): return self._id.name
  @name.setter
  def name(self, v): self._id.name = v

  @property
  def init(self): return self._init
  @init.setter
  def init(self, v): self._init = v

  @property
  def lbl(self): return (self._id.name, self.ati)
  @lbl.setter
  def lbl(self, v): self._lbl = v

  @property
  def typee(self): return self.parentNode.typee
  @typee.setter
  def typee(self, v): self._type = v

  def gen(self): return set([self.lbl]) if self._init else set([])

  def __str__(self):
    return str(self.idd)
