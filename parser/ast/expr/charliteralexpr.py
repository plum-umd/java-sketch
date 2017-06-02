#!/usr/bin/env python

from .stringliteralexpr import StringLiteralExpr

from ..type.primitivetype import PrimitiveType

class CharLiteralExpr(StringLiteralExpr):
    def __init__(self, kwargs={}):
        super(CharLiteralExpr, self).__init__(kwargs)

        self.add_as_parent([self.typee])

    @property
    def typee(self): return PrimitiveType({u'type': {u'name': u'char'}})
    @typee.setter
    def typee(self, v): pass
