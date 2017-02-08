#!/usr/bin/env python

from .statement import Statement
from . import _import

class ForeachStmt(Statement):
  def __init__(self, kwargs={}):
    super(ForeachStmt, self).__init__(kwargs)
    locs = _import()

    # VariableDeclarationExpr var
    var = kwargs.get(u'var', {})
    self._var = locs[u'VariableDeclarationExpr'](var) if var else None
    
    # Expression iterable;
    iterable = kwargs.get(u'iterable', {})
    self._iterable = locs[iterable[u'@t']](iterable) if iterable else None
    
    # Statement body;
    body = kwargs.get(u'body', {})
    self._body = locs[body[u'@t']](body) if body else None

  @property
  def var(self): return self._var
  @var.setter
  def var(self, v): self._var = v

  @property
  def iterable(self): return self._iterable
  @iterable.setter
  def iterable(self, v): self._iterable = v

  @property
  def body(self): return self._body
  @body.setter
  def body(self, v): self._body = v
