#!/usr/bin/env python

from __future__ import absolute_import
from .expression import Expression

from . import _import
from ..type.referencetype import ReferenceType

class FieldAccessExpr(Expression):
    def __init__(self, kwargs={}):
        super(FieldAccessExpr, self).__init__(kwargs)
        locs = _import()
    
        # Expression scope
        scope = kwargs.get(u'scope', {})
        self._scope = locs[scope[u'@t']](scope) if scope else None
    
        # List<Type> typeArgs;
    
        # NameExpr field;
        field = kwargs.get(u'field', {})
        self._field = locs[u'NameExpr'](field) if field else None
    
        self.add_as_parent([self.scope, self.field])
        
    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, v): self._scope = v
  
    @property
    def field(self): return self._field
    @field.setter
    def field(self, v): self._field = v
  
    @property
    def name(self): return self.field.name
    @name.setter
    def name(self, v): self.field.name = v

    @property
    def typee(self):
        if self.field:
            if self.field.name in self.field.symtab:
                return self.field.symtab[self.field.name].typee
            
        return None
