#!/usr/bin/env python

from .stringliteralexpr import StringLiteralExpr
from ..type.primitivetype import PrimitiveType

class DoubleLiteralExpr(StringLiteralExpr):
    def __init__(self, kwargs={}):
        super(DoubleLiteralExpr, self).__init__(kwargs)

    @property
    def typee(self): PrimitiveType({u'type': {u'name': u'double'}})
    @typee.setter
    def typee(self, v): pass
