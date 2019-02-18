#!/usr/bin/env python

from __future__ import absolute_import
from . import _import
from .bodydeclaration import BodyDeclaration

class FieldDeclaration(BodyDeclaration):
    def __init__(self, kwargs={}):
        super(FieldDeclaration, self).__init__(kwargs)
        locs = _import()
        
        # int modifiers;
        self._modifiers = kwargs.get(u'modifiers', 0)

        # Type
        typdct = kwargs.get(u'type')
        self._type = locs[typdct[u'@t']](typdct)

        # VariableDeclarator variable
        # field with multiple declarations are split up:
        # int x,y; => int x; int y;
        iddct = kwargs.get(u'variables').get(u'@e')
        self._variable = None
        if iddct:
            self._variable = locs[u'VariableDeclarator'](iddct[0])
            if len(iddct[1:]) > 0:
                kwargs[u'variables'][u'@e'] = iddct[1:]
                self.parentNode.members.append(FieldDeclaration(kwargs))

        # # List <VariableDeclarator> variables
        # # unmodified list of variables
        # self._variables = map(lambda v: locs[u'VariableDeclarator'](v) if u'@t' in v else [],
        #                       iddct) if iddct else []

        self.add_as_parent([self.typee, self.variable])

    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def name(self): return self._variable.name
    @name.setter
    def name(self, v): self._name = v

    @property
    def variable(self): return self._variable
    @variable.setter
    def variable(self, v): self._variable = v

    def __str__(self):
        if self.parentNode: return '_'.join([self.sanitize_ty(self.name), str(self.parentNode)])
        else: return self.sanitize_ty(self.name)
