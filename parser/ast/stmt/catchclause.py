#!/usr/bin/env python

from .statement import Statement
from . import _import

class CatchClause(Statement):
  def __init__(self, kwargs={}):
    super(CatchClause, self).__init__(kwargs)
    locs = _import()

    # Parameter param;
    param = kwargs.get(u'param', {})
    self._param = locs[u'Parameter'](param) if param else None
    
    # BlockStmt catchBlock;
    catchBlock = kwargs.get(u'catchBlock', {})
    self._catchBlock = locs[u'BlockStmt'](catchBlock) if catchBlock else None

  @property
  def param(self): return self._param
  @param.setter
  def param(self, v): self._param = v
  
  @property
  def catchBlock(self): return self._catchBlock
  @catchBlock.setter
  def catchBlock(self, v): self._catchBlock = v
