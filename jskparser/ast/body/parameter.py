#!/usr/bin/env python

from __future__ import absolute_import
from ..node import Node

from . import _import

class Parameter(Node):
    def __init__(self, kwargs={}):
        super(Parameter, self).__init__(kwargs)
        locs = _import()

        # int modifiers
        self._modifiers = kwargs.get(u'modifiers', 0)

        # Type type
        typdct = kwargs.get(u'type', {})
        if typdct: self._type = locs[typdct[u'@t']](typdct)

        # VariableDeclarator id
        self._id = locs[u'VariableDeclarator'](kwargs)

        # Any
        self._any = kwargs.get(u'any', False)

        # boolean isVarArgs
        self._isVarArgs = kwargs.get(u'isVarArgs', False)

        # List<AnnotationExpr> annotations;
        annotations = kwargs.get(u'annotations', [])
        self._annotations = [locs[x[u'@t']](x) if u'@t' in x else [] for x in annotations.get(u'@e', [])] if annotations else []

        self.add_as_parent([self.idd])

    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def idd(self): return self._id
    @idd.setter
    def idd(self, v): self._id = v

    @property
    def name(self): return self._id.name
    @name.setter
    def name(self, v): self._id.name = v

    @property
    def anyy(self): return self._any
    @anyy.setter
    def anyy(self, v): self._any = v

    @property
    def isVarArgs(self): return self._isVarArgs
    @isVarArgs.setter
    def isVarArgs(self, v): self._isVarArgs = v

    @property
    def lbl(self): return (self._id.name, self._ati)
    @lbl.setter
    def lbl(self, v): self._lbl = v

    @property
    def annotations(self): return self._annotations
    @annotations.setter
    def annotations(self, v): self._annotations = v
