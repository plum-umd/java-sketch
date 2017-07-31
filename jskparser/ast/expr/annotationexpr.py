#!/usr/bin/env python

from .expression import Expression
from .nameexpr import NameExpr

class AnnotationExpr(Expression):
    def __init__(self, kwargs={}):
        super(AnnotationExpr, self).__init__(kwargs)

        # NameExpr name;
        name = kwargs.get(u'name', {})
        self._name = NameExpr(name)

    def __str__(self):
        return str(self._name)
