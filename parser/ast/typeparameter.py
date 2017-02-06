#!/usr/bin/env python

# The TypeParameter is constructed following the syntax:<br>
# TypeParameter ::= <IDENTIFIER> ( "extends" }{@link ClassOrInterfaceType}{@code ( "&" }{@link ClassOrInterfaceType}{@code )* )?

from . import _import

from node import Node

class TypeParameter(Node):
    def __init__(self, kwargs={}):
        super(TypeParameter, self).__init__(kwargs)
        locs = _import()

        # List<AnnotationExpr> annotations; TODO
        
        # List<ClassOrInterfaceType> typeBound;
        typeBound = kwargs.get(u'typeBound', [])
        self._typeBound = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                              typeBound.get(u'@e', [])) if typeBound else []

    @property
    def typeBound(self): return self._typeBound
    @typeBound.setter
    def typeBound(self, v): self._typeBound = v
