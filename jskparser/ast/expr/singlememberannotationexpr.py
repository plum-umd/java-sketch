#!/usr/bin/env python

from . import _import

from .annotationexpr import AnnotationExpr

class SingleMemberAnnotationExpr(AnnotationExpr):
    def __init__(self, kwargs={}):
        super(SingleMemberAnnotationExpr, self).__init__(kwargs)

        locs = _import()
    
        # Expression expr;
        memberValue = kwargs.get(u'memberValue', {})
        self._memberValue = locs[memberValue[u'@t']](memberValue) if memberValue else None

    @property
    def memberValue(self): return self._memberValue
    @memberValue.setter
    def memberValue(self, v): self._memberValue = v
