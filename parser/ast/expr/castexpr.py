#!/usr/bin/env python

from .expression import Expression

from . import _import

class CastExpr(Expression):
    def __init__(self, kwargs={}):
        super(CastExpr, self).__init__(kwargs)
        locs = _import()
    
        # Type type
        t = kwargs.get(u'type', {})
        self._type = locs[t[u'@t']](t) if t else None
    
        # Expression expr;
        e = kwargs.get(u'expr', {})
        self._expr = locs[e[u'@t']](e) if e else None

        self.add_as_parent([self.typee, self.expr])
                   
    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v
  
    @property
    def expr(self): return self._expr
    @expr.setter
    def expr(self, v): self._expr = v
