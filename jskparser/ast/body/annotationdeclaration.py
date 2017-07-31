#!/usr/bin/env python

from . import _import

from .typedeclaration import TypeDeclaration

class AnnotationDeclaration(TypeDeclaration):
    def __init__(self, kwargs={}):
        super(AnnotationDeclaration, self).__init__(kwargs)
