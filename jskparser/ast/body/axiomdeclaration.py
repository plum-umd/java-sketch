#!/usr/bin/env python

from . import _import

from ..body.bodydeclaration import BodyDeclaration

from ..comments.comment import Comment

class AxiomDeclaration(BodyDeclaration):
    def __init__(self, kwargs={}):
        super(AxiomDeclaration, self).__init__(kwargs)
        locs = _import()

        # int modifiers
        self._modifiers = kwargs.get(u'modifiers', 0)

        # This is the return type and will be stored as a child of the method
        typdct = kwargs.get(u'type', {})
        if typdct: self._type = locs[typdct[u'@t']](typdct)

        # List<AxiomParameter> parameters
        params = kwargs.get(u'parameters', [])
        self._parameters = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                               params.get(u'@e', [])) if params else []

        # BlockStmt body;
        body = kwargs.get(u'body')
        self._body = locs[u'BlockStmt'](body) if body else None
        
        if self._body and self._body.childrenNodes:
            chs = filter(lambda c: not isinstance(c, Comment), self._body.childrenNodes)
            if chs: chs[0].in_set = set(map(lambda x: x.lbl, self._parameters))

    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def parameters(self): return self._parameters
    @parameters.setter
    def parameters(self, v): self._parameters = v

    @property
    def body(self): return self._body
    @body.setter
    def body(self, v): self._body = v
