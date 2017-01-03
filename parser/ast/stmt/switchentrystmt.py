#!/usr/bin/env python

from .statement import Statement

from . import _import

class SwitchEntryStmt(Statement):
  def __init__(self, kwargs={}):
    super(SwitchEntryStmt, self).__init__(kwargs)
    locs = _import()

    # Expression label;
    s = kwargs.get(u'label', {})
    self._label = locs[s[u'@t']](s) if s else None

    # List<Statement> stmts;
    s = kwargs.get(u'stmts', {})
    self._stmts = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                      s.get(u'@e', [])) if s else []
  @property
  def label(self): return self._label
  @label.setter
  def label(self, v): self._label = v

  @property
  def stmts(self): return self._stmts
  @stmts.setter
  def stmts(self, v): self._stmts = v
  
