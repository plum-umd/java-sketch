#!/usr/bin/env python

from __future__ import absolute_import
from ..body.variabledeclarator import VariableDeclarator
from .expression import Expression
from . import _import

class VariableDeclarationExpr(Expression):
    def __init__(self, kwargs={}):
        super(VariableDeclarationExpr, self).__init__(kwargs)
        locs = _import()

        # int modifiers
        self._modifiers = kwargs.get(u'modifiers', 0)
        
        # Type type
        t = kwargs.get(u'type', {})
        self._type = locs[t[u'@t']](t) if t else None

        # List<VariableDeclarator> vars
        var = kwargs.get(u'vars', {}).get(u'@e')
        self._varss = map(lambda v: VariableDeclarator(v), var)

        self._arrayCount = kwargs.get(u'arrayCount', 0)

        # List<AnnotationExpr> annotations
        annotations = kwargs.get(u'annotations', [])
        self._annotations = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                                annotations.get(u'@e', [])) if annotations else []
        
        self.add_as_parent([self.typee]+self.varss)

    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def varss(self): return self._varss
    @varss.setter
    def varss(self, v): self._varss = v

    @property
    def arrayCount(self): return self._arrayCount
    @arrayCount.setter
    def arrayCount(self, v): self._arrayCount = v
        
    @property
    def annotations(self): return self._annotations
    @annotations.setter
    def annotations(self, v): self._annotations = v
