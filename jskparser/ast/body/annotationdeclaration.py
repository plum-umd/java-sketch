#!/usr/bin/env python

from __future__ import absolute_import
from . import _import

from .typedeclaration import TypeDeclaration

class AnnotationDeclaration(TypeDeclaration):
    def __init__(self, kwargs={}):
        super(AnnotationDeclaration, self).__init__(kwargs)
