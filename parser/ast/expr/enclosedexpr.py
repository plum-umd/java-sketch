#!/usr/bin/env python

from .expression import Expression

from . import _import

class EnclosedExpr(Expression):
    def __init__(self, kwargs={}):
        super(EnclosedExpr, self).__init__(kwargs)
        locs = _import()
        
        # Expression inner
        inner = kwargs.get(u'inner', {})
        self._inner = locs[inner[u'@t']](inner) if inner else None

        self.add_as_parent([self.inner])
        
    @property
    def inner(self): return self._inner
    @inner.setter
    def inner(self, v): self._inner = v
