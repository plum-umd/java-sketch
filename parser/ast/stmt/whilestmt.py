#!/usr/bin/env python

from .statement import Statement
from . import _import

class WhileStmt(Statement):
  def __init__(self, kwargs={}):
    super(WhileStmt, self).__init__(kwargs)
    locs = _import()

    # Expression compare;
    condition = kwargs.get(u'condition', {})
    self._condition = locs[condition[u'@t']](condition) if condition else None
    
    # Statement body;
    body = kwargs.get(u'body', {})
    self._body = locs[body[u'@t']](body) if body else None

  @property
  def condition(self): return self._condition
  @condition.setter
  def condition(self, v): self._condition = v

  @property
  def body(self): return self._body
  @body.setter
  def body(self, v): self._body = v
