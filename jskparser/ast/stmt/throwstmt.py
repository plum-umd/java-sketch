#!/usr/bin/env python

from __future__ import absolute_import
from .statement import Statement

from . import _import

class ThrowStmt(Statement):
    def __init__(self, kwargs={}):
        super(Statement, self).__init__(kwargs)
    
        locs = _import()
    
        # Expression expr;
        e = kwargs.get(u'expr', {})
        self._expr = locs[e[u'@t']](e) if e else None

        self.add_as_parent([self.expr])
    
    @property
    def expr(self): return self._expr
    @expr.setter
    def expr(self, v): self._expr = v
