#!/usr/bin/env python

from __future__ import absolute_import
from .statement import Statement

from . import _import

class IfStmt(Statement):
    def __init__(self, kwargs={}):
        super(IfStmt, self).__init__(kwargs)
        locs = _import()
    
        # Expression condition;
        con = kwargs.get(u'condition', {})
        self._condition = locs[con[u'@t']](con) if con else None
    
        # Statement thenStmt;
        then = kwargs.get(u'thenStmt', {})
        self._thenStmt = locs[then[u'@t']](then) if then else None
    
        # Statement elseStmt;
        el = kwargs.get(u'elseStmt', {})
        self._elseStmt = locs[el[u'@t']](el) if el else None

        self.add_as_parent([self.condition, self.thenStmt, self.elseStmt])
    
    @property
    def condition(self): return self._condition
    @condition.setter
    def condition(self, v): self._condition = v
  
    @property
    def thenStmt(self): return self._thenStmt
    @thenStmt.setter
    def thenStmt(self, v): self._thenStmt = v
  
    @property
    def elseStmt(self): return self._elseStmt
    @elseStmt.setter
    def elseStmt(self, v): self._elseStmt = v
