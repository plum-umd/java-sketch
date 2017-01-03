#!/usr/bin/env python

from .statement import Statement
from .switchentrystmt import SwitchEntryStmt

from . import _import

class SwitchStmt(Statement):
  def __init__(self, kwargs={}):
    super(SwitchStmt, self).__init__(kwargs)
    locs = _import()

    # Expression selector;
    s = kwargs.get(u'selector', {})
    self._selector = locs[s[u'@t']](s) if s else None

    # List<SwitchEntryStmt> entries;
    en = kwargs.get(u'entries', {}).get(u'@e')
    self._entries = map(lambda e: SwitchEntryStmt(e), en)

  @property
  def selector(self): return self._selector
  @selector.setter
  def selector(self, v): self._selector = v

  @property
  def entries(self): return self._entries
  @entries.setter
  def entries(self, v): self._entries = v

