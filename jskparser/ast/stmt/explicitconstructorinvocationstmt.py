#!/usr/bin/env python

from __future__ import absolute_import
from . import _import
from .statement import Statement

from ..expr.methodcallexpr import MethodCallExpr
from ..expr.fieldaccessexpr import FieldAccessExpr
from ..expr.thisexpr import ThisExpr

from ..utils import utils

class ExplicitConstructorInvocationStmt(Statement):
    def __init__(self, kwargs={}):
        super(ExplicitConstructorInvocationStmt, self).__init__(kwargs)
        locs = _import()
    
        # List<Type> typeArgs;
        
        # boolean isThis;
        self._isThis = kwargs.get(u'isThis', False)
        
        # Expression expr;
        expr = kwargs.get(u'expr')
        self._expr = locs[expr[u'@t']](expr) if expr else None
        
        # List<Expression> args;
        args = kwargs.get(u'args', {})
        self._args = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                         args.get(u'@e', [])) if args else []

        self.add_as_parent([self.expr]+self.args)
        
    @property
    def isThis(self): return self._isThis
    @isThis.setter
    def isThis(self, v): self._isThis = v
  
    @property
    def expr(self): return self._expr
    @expr.setter
    def expr(self, v): self._expr = v
  
    @property
    def args(self): return self._args
    @args.setter
    def args(self, v): self._args = v
    

    def arg_typs(self):
        typs = []
        for a in self.args:
            if type(a) == FieldAccessExpr:
                # TODO: if a field from an imported class is only used in a method call
                # this will fail :(
                fld = utils.find_fld(a, None)
                if not fld: return None
                typ = fld.typee
            elif isinstance(a, MethodCallExpr):
                typ = a.typee
            elif isinstance(a, ThisExpr):
                typ = utils.get_coid(self)
            elif not a.typee:
                typ = self.symtab[a.name].typee
            else:
                typ = a.typee
            typs.append(typ)
        return typs
