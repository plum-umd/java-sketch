#!/usr/bin/env python

# The TypeParameter is constructed following the syntax:<br>
# TypeParameter ::= <IDENTIFIER> ( "extends" }{@link ClassOrInterfaceType}{@code ( "&" }{@link ClassOrInterfaceType}{@code )* )?

from node import Node

from .type.classorinterfacetype import ClassOrInterfaceType

class TypeParameter(Node):
    def __init__(self, kwargs={}):
        super(TypeParameter, self).__init__(kwargs)
        # List<AnnotationExpr> annotations; TODO
        
        # List<ClassOrInterfaceType> typeBound;
        typeBound = kwargs.get(u'typeBound', [])
        self._typeBound = map(lambda x: ClassOrInterfaceType(x) if u'@t' in x else [],
                              typeBound.get(u'@e', [])) if typeBound else []

    @property
    def typeBound(self): return self._typeBound if self._typeBound else [ClassOrInterfaceType({u'name':u'Object'})]
    @typeBound.setter
    def typeBound(self, v): self._typeBound = v

    def __str__(self): return self.name
