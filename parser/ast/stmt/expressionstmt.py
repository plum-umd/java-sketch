#!/usr/bin/env python

from .statement import Statement
from . import _import

class ExpressionStmt(Statement):
    def __init__(self, kwargs={}):
        super(ExpressionStmt, self).__init__(kwargs)
        locs = _import()
    
        # Expression expr;
        expr = kwargs.get(u'expr', {})
        self._expr = locs[expr[u'@t']](expr) if expr else None
        
        self.add_as_parent([self.expr])
        
    @property
    def expr(self): return self._expr
    @expr.setter
    def expr(self, v): self._expr = v
