#!/usr/bin/env python

from .statement import Statement
from . import _import

class MinrepeatStmt(Statement):
  def __init__(self, kwargs={}):
    super(MinrepeatStmt, self).__init__(kwargs)
    locs = _import()
    
    # Statement body;
    body = kwargs.get(u'body', {})
    self._body = locs[body[u'@t']](body) if body else None

  @property
  def body(self): return self._body
  @body.setter
  def body(self, v): self._body = v
