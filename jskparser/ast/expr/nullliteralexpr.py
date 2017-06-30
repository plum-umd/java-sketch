#!/usr/bin/env python

from .literalexpr import LiteralExpr

from ..type.primitivetype import PrimitiveType

class NullLiteralExpr(LiteralExpr):
    def __init__(self, kwargs={}):
        super(NullLiteralExpr, self).__init__(kwargs)

        self.add_as_parent([self.typee])

    @property
    def typee(self): return PrimitiveType({u'type': {u'name': u'null'}})
    @typee.setter
    def typee(self, v): pass
