#!/usr/bin/env python

from .annotationexpr import AnnotationExpr

class NormalAnnotationExpr(AnnotationExpr):
    def __init__(self, kwargs={}):
        super(NormalAnnotationExpr, self).__init__(kwargs)

        # List<MemberValuePair> pairs;
        pairs = kwargs.get(u'pairs', [])
        if pairs: raise Exception('NormalAnnotationExpr unimplimented')
