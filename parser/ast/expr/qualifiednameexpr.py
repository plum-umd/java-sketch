#!/usr/bin/env python

from .nameexpr import NameExpr

from . import _import

class QualifiedNameExpr(NameExpr):
    def __init__(self, kwargs={}):
        super(QualifiedNameExpr, self).__init__(kwargs)
        locs = _import()
        self._qualifier = locs[u'NameExpr'](kwargs.get(u'qualifier', {}))
        
    @property
    def qualifier(self): return self._qualifier
    @qualifier.setter
    def qualifier(self, v): self._qualifier = v
