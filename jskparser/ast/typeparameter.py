#!/usr/bin/env python

# The TypeParameter is constructed following the syntax:<br>
# TypeParameter ::= <IDENTIFIER> ( "extends" }{@link ClassOrInterfaceType}{@code ( "&" }{@link ClassOrInterfaceType}{@code )* )?

from __future__ import absolute_import
from .node import Node

from .type.classorinterfacetype import ClassOrInterfaceType

from .expr.annotationexpr import AnnotationExpr

class TypeParameter(Node):
    def __init__(self, kwargs={}):
        super(TypeParameter, self).__init__(kwargs)

        # List<AnnotationExpr> annotations;
        annotations = kwargs.get(u'annotations', [])
        self._annotations = [AnnotationExpr(x) if u'@t' in x else [] for x in
                                annotations.get(u'@e', [])] if annotations else []
        
        # List<ClassOrInterfaceType> typeBound;
        typeBound = kwargs.get(u'typeBound', [])
        self._typeBound = [ClassOrInterfaceType(x) if u'@t' in x else [] for x in
                              typeBound.get(u'@e', [])] if typeBound else []

        self.add_as_parent(typeBound)

    @property
    def typeBound(self): return self._typeBound if self._typeBound else [ClassOrInterfaceType({u'name':u'Object'})]
    @typeBound.setter
    def typeBound(self, v): self._typeBound = v

    @property
    def annotations(self): return self._annotations
    @annotations.setter
    def annotations(self, v): self._annotations = v

    def __str__(self): return self.name
