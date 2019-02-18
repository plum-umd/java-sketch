#!/usr/bin/env python

from __future__ import absolute_import
from . import _import

from ..node import Node

class AxiomParameter(Node):
    def __init__(self, kwargs={}):
        super(AxiomParameter, self).__init__(kwargs)
        locs = _import()

        # int modifiers
        self._modifiers = kwargs.get(u'modifiers', 0)

        # Type type
        typdct = kwargs.get(u'type', {})
        if typdct: self._type = locs[typdct[u'@t']](typdct)

        # VariableDeclarator id
        idd = kwargs.get(u'id', {})
        self._id = locs[u'VariableDeclarator'](kwargs) if idd else None

        # AxiomDeclaration method
        method = kwargs.get(u'method', {})
        self._method = locs[u'AxiomDeclaration'](method) if method else None

        # List<AnnotationExpr> annotations;
        annotations = kwargs.get(u'annotations', [])
        self._annotations = [locs[x[u'@t']](x) if u'@t' in x else [] for x in annotations.get(u'@e', [])] if annotations else []

        self.add_as_parent([self.typee]+[self.annotations])
        if self._id: self.add_as_parent([self._id])
        elif self._method: self.add_as_parent([self._method])

    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v

    @property
    def typee(self): return self._type if self._type else self._method.typee
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def idd(self): return self._id
    @idd.setter
    def idd(self, v): self._id = v

    @property
    def name(self): return self._id.name if self._id else self._method.name
    @name.setter
    def name(self, v): self._name = v

    @property
    def method(self): return self._method
    @method.setter
    def method(self, v): self._method = v

    @property
    def lbl(self): return (self._id.name, self._ati)
    @lbl.setter
    def lbl(self, v): self._lbl = v

    @property
    def annotations(self): return self._annotations
    @annotations.setter
    def annotations(self, v): self._annotations = v

    def __str__(self): return self.name
