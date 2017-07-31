#!/usr/bin/env python

from .annotationexpr import AnnotationExpr

class MarkerAnnotationExpr(AnnotationExpr):
    def __init__(self, kwargs={}):
        super(MarkerAnnotationExpr, self).__init__(kwargs)
