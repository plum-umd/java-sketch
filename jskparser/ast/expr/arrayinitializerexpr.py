#!/usr/bin/env python

from __future__ import absolute_import
from .expression import Expression

from . import _import

class ArrayInitializerExpr(Expression):
    def __init__(self, kwargs={}):
        super(ArrayInitializerExpr, self).__init__(kwargs)
        locs = _import()
    
        # List<Expression> values;
        v = kwargs.get(u'values', {})
        self._values = map(lambda e: locs[e[u'@t']](e) if u'@t' in e else [],
                           v.get(u'@e', [])) if v else []

        self.add_as_parent(self.values)
                    
    @property
    def values(self): return self._values
    @values.setter
    def values(self, v): self._values = v
