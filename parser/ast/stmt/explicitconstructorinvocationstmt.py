#!/usr/bin/env python

from .statement import Statement
from . import _import

class ExplicitConstructorInvocationStmt(Statement):
  def __init__(self, kwargs={}):
    super(ExplicitConstructorInvocationStmt, self).__init__(kwargs)
    locs = _import()

    #List<Type> typeArgs;
    
    #boolean isThis;
    self._isThis = kwargs.get(u'isThis', False)
    
    #Expression expr;
    expr = kwargs.get(u'expr')
    self._expr = locs[expr[u'@t']](expr) if expr else None
    
    #List<Expression> args;
    args = kwargs.get(u'args', {})
    self._args = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                     args.get(u'@e', [])) if args else []
    
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
  
