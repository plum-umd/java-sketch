#!/usr/bin/env python

from __future__ import absolute_import
from .expression import Expression
from . import _import

class AssignExpr(Expression):
    def __init__(self, kwargs={}):
        super(AssignExpr, self).__init__(kwargs)
        locs = _import()
    
        # Expression target
        t = kwargs.get(u'target', {})
        self._target = locs[t[u'@t']](t) if t else None
    
        # Expression value
        v = kwargs.get(u'value', {})
        self._value = locs[v[u'@t']](v) if v else None
    
        # Operator op
        self._op = kwargs.get(u'op', {}).get(u'name')

        self.add_as_parent([self.target, self.value])
        
    @property
    def target(self): return self._target
    @target.setter
    def target(self, v): self._target = v
  
    @property
    def value(self): return self._value
    @value.setter
    def value(self, v): self._value = v
  
    @property
    def op(self): return self._op
    @op.setter
    def op(self, v): self._op = v
  
    @property
    def typee(self): return self._value
    @typee.setter
    def typee(self, v): self._type = v
  
    def gen(self): return set([self._target.lbl])
    def kill(self): return set([self._target.lbl])
