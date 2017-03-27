#!/usr/bin/env python

from .statement import Statement

class BreakStmt(Statement):
  def __init__(self, kwargs={}):
    super(BreakStmt, self).__init__(kwargs)

    # String id;
    self._id = kwargs.get(u'id', '')

  @property
  def idd(self): return self._id
  @idd.setter
  def idd(self, v): self._id = v
