#!/usr/bin/env python

from .statement import Statement
from ..utils import utils
from ..expr.nameexpr import NameExpr
from ..expr.literalexpr import LiteralExpr
from ..type.type import Type
from . import _import

class ReturnStmt(Statement):
    def __init__(self, kwargs={}):
        super(ReturnStmt, self).__init__(kwargs)
    
        locs = _import()
    
        # Expression expr;
        e = kwargs.get(u'expr', {})
        self._expr = locs[e[u'@t']](e) if e else None
    
        self._type = u'void'
        def t(n):
            if type(n) == NameExpr: self._type = n
            elif isinstance(n, Type) or isinstance(n, LiteralExpr): self._type = n.typee
        utils.walk(t, self)

        self.add_as_parent([self.expr])
    
    @property
    def expr(self): return self._expr
    @expr.setter
    def expr(self, v): self._expr = v
  
    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v
    
    @property
    def out_set(self): return set([])
    @out_set.setter
    def out_set(self, v): pass
