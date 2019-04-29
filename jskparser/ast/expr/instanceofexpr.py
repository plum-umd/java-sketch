#!/usr/bin/env python

from __future__ import absolute_import
from .expression import Expression

from . import _import

class InstanceOfExpr(Expression):
    def __init__(self, kwargs={}):
        super(InstanceOfExpr, self).__init__(kwargs)
        locs = _import()
    
        # Expression expr;
        e = kwargs.get(u'expr', {})
        self._expr = locs[e[u'@t']](e) if e else None
    
        # Type type
        t = kwargs.get(u'type', {})
        self._type = locs[t[u'@t']](t) if t else None

        self.add_as_parent([self.expr, self.typee])
    
    @property
    def expr(self): return self._expr
    @expr.setter
    def expr(self, v): self._expr = v
  
    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v
