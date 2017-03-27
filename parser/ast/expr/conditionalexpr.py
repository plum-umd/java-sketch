#!/usr/bin/env python

from .expression import Expression

from . import _import

class ConditionalExpr(Expression):
    def __init__(self, kwargs={}):
        super(ConditionalExpr, self).__init__(kwargs)
        locs = _import()

        # Expression condition
        condition = kwargs.get(u'condition', {})
        self._condition = locs[condition[u'@t']](condition) if condition else None
        # Expression thenExpr
        thenExpr = kwargs.get(u'thenExpr', {})
        self._thenExpr = locs[thenExpr[u'@t']](thenExpr) if thenExpr else None
        # Expression elseExpr
        elseExpr = kwargs.get(u'elseExpr', {})
        self._elseExpr = locs[elseExpr[u'@t']](elseExpr) if elseExpr else None

    @property
    def condition(self): return self._condition
    @condition.setter
    def condition(self, v): self._condition = v
    
    @property
    def thenExpr(self): return self._thenExpr
    @thenExpr.setter
    def thenExpr(self, v): self._thenExpr = v
    
    @property
    def elseExpr(self): return self._elseExpr
    @elseExpr.setter
    def elseExpr(self, v): self._elseExpr = v
