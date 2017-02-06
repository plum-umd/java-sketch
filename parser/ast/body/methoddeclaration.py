#!/usr/bin/env python

from . import _import

from .bodydeclaration import BodyDeclaration

from ..typeparameter import TypeParameter
from ..comments.comment import Comment

class MethodDeclaration(BodyDeclaration):
    def __init__(self, kwargs={}):
        super(MethodDeclaration, self).__init__(kwargs)

        locs = _import()

        self._modifiers = kwargs.get(u'modifiers', 0)
        # This is the return type and will be stored as a child of the method
        typdct = kwargs.get(u'type')
        self._type = locs[typdct[u'@t']](typdct)

        # List<Parameter> parameters
        params = kwargs.get(u'parameters', {})
        self._parameters = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                               params.get(u'@e', [])) if params else []

        # List<TypeParameter>
        typeParameters = kwargs.get(u'typeParameters', {})
        self._typeParameters = map(lambda x: TypeParameter(x) if u'@t' in x else [],
                                   typeParameters.get(u'@e', [])) if typeParameters else []

        # int arrayCount;
        self._arrayCount = kwargs.get(u'arrayCount', 0)

        # List<ReferenceType> throws_;
        throws = kwargs.get(u'throws_', {})
        self._throws = map(lambda x: locs[u'ReferenceType'](x) if u'@t' in x else [],
                           throws.get(u'@e', [])) if throws else []

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

    @property
    def arrayCount(self): return self._arrayCount
    @arrayCount.setter
    def arrayCount(self, v): self._arrayCount = v

    @property
    def throws(self): return self._throws
    @throws.setter
    def throws(self, v): self._throws = v

    @property
    def typeParameters(self): return self._typeParameters
    @typeParameters.setter
    def typeParameters(self, v): self._typeParameters = v

    def param_typs(self): return map(lambda p: p.typee, self.parameters)
    def param_names(self): return map(lambda p: p.name, self.parameters)

    def __str__(self):
        params = map(self.sanitize_ty, map(lambda p: p.typee.name, self.parameters))
        return u'_'.join([self.sanitize_ty(self.name)] + params)
