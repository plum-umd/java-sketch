#!/usr/bin/env python

from __future__ import absolute_import
from . import _import

from .expression import Expression

from ..type.primitivetype import PrimitiveType

class GeneratorExpr(Expression):
    def __init__(self, kwargs={}):
        super(GeneratorExpr, self).__init__(kwargs)

        locs = _import()

        # boolean isHole
        self._isHole = kwargs.get(u'isHole', False)

        # List Expression
        exprs = kwargs.get(u'exprs', {})
        self._exprs = [locs[x[u'@t']](x) if u'@t' in x else [] for x in
                          exprs.get(u'@e', [])] if exprs else []

        self.add_as_parent(self.exprs)

        self._my_typ = PrimitiveType({u'type': {u'name': u'int'}})
        
    @property
    def isHole(self): return self._isHole
    @isHole.setter
    def isHole(self, v): self._isHole = v
  
    @property
    def my_typ(self): return self._my_typ
    @my_typ.setter
    def my_typ(self, v): self._my_typ = v
  
    @property
    def exprs(self): return self._exprs
    @exprs.setter
    def exprs(self, v): self._exprs = v

    @property
    def typee(self):
        return self.my_typ if self.isHole else \
            self.symtab.get(self._exprs[0].name).typee
    @typee.setter
    def typee(self, v): self._typee = v
