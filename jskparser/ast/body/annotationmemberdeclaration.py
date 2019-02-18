#!/usr/bin/env python

from __future__ import absolute_import
from . import _import

from .typedeclaration import TypeDeclaration

class AnnotationMemberDeclaration(TypeDeclaration):
    def __init__(self, kwargs={}):
        super(AnnotationDeclaration, self).__init__(kwargs)

        locs = _import()

        self._modifiers = kwargs.get(u'modifiers', 0)

        # Type type
        t = kwargs.get(u'type', {})
        self._type = locs[t[u'@t']](t) if t else None

        # Expression defaultValue
        defaultValue = kwargs.get(u'defaultValue')
        self._defaultValue = locs[defaultValue[u'@t']](defaultValue) if defaultValue else None

    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def defaultValue(self): return self._defaultValue
    @defaultValue.setter
    def defaultValue(self, v): self._defaultValue = v
