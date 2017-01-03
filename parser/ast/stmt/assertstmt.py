#!/usr/bin/env python

from .statement import Statement

from . import _import

class AssertStmt(Statement):
  def __init__(self, kwargs={}):
    super(AssertStmt, self).__init__(kwargs)
    locs = _import()

    # Expression check
    check = kwargs.get(u'check', {})
    self._check = locs[check[u'@t']](check) if check else None

    # Expression msg
    msg = kwargs.get(u'msg', {})
    self._msg = locs[msg[u'@t']](msg) if msg else None

  @property
  def check(self): return self._check
  @check.setter
  def check(self, v): self._check = v

  @property
  def msg(self): return self._msg
  @msg.setter
  def msg(self, v): self._msg = v
