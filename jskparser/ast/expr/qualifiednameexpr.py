#!/usr/bin/env python

from __future__ import absolute_import
from . import _import

from .nameexpr import NameExpr

class QualifiedNameExpr(NameExpr):
    def __init__(self, kwargs={}):
        super(QualifiedNameExpr, self).__init__(kwargs)

        locs = _import()

        # NameExpr qualifier;
        qualifier = kwargs.get(u'qualifier', {})
        self._qualifier = locs[qualifier[u'@t']](qualifier) if u'@t' in qualifier else locs[u'NameExpr'](qualifier)

        self.add_as_parent([self.qualifier])
        
    @property
    def qualifier(self): return self._qualifier
    @qualifier.setter
    def qualifier(self, v): self._qualifier = v

    def __str__(self):
        return '{}.{}'.format(str(self.qualifier), self.name)
