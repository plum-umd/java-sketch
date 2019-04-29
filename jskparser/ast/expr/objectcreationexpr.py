#!/usr/bin/env python

from __future__ import absolute_import
from .expression import Expression
from ..type.classorinterfacetype import ClassOrInterfaceType
from ..body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

from . import _import

class ObjectCreationExpr(Expression):
    def __init__(self, kwargs={}):
        super(ObjectCreationExpr, self).__init__(kwargs)
        locs = _import()

        # Expression scope
        scope = kwargs.get(u'scope', {})
        self._scope = locs[scope[u'@t']](scope) if scope else None

        # ClassOrInterfaceType type;
        typ = kwargs.get(u'type', {})
        if isinstance(typ, ClassOrInterfaceDeclaration):
            self._type = typ
        else:
            self._type = ClassOrInterfaceType(kwargs.get(u'type', {}))

        # List<Type> typeArgs;
        typeArgs = kwargs.get(u'typeArgs', {})
        self._typeArgs = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                             typeArgs.get(u'@e', [])) if typeArgs else []

        # List<Expression> args;
        args = kwargs.get(u'args', {})
        self._tmpargs = args
        self._args = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                         args.get(u'@e', [])) if args else []

        # This can be null, to indicate there is no body
        # List<BodyDeclaration> anonymousClassBody;
        anon = kwargs.get(u'anonymousClassBody', {})
        self._anonymousClassBody = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                                       anon.get(u'@e', [])) if anon else []

        box = kwargs.get(u'box', {})
        self._box = box if box else False
        if not self._box:
            self.add_as_parent([self.scope, self.typee]+self.typeArgs+self.args+self.anonymousClassBody)

    @property
    def box(self): return self._box
    @box.setter
    def box(self, v): self._box = v

    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, v): self._scope = v

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def args(self): return self._args
    @args.setter
    def args(self, v): self._args = v

    @property
    def typeArgs(self): return self._typeArgs
    @typeArgs.setter
    def typeArgs(self, v): self._typeArgs = v

    @property
    def anonymousClassBody(self): return self._anonymousClassBody
    @anonymousClassBody.setter
    def anonymousClassBody(self, v): self._anonymousClassBody = v
