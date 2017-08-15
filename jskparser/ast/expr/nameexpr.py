#!/usr/bin/env python

from . import _import

from .expression import Expression

class NameExpr(Expression):
    def __init__(self, kwargs={}):
        super(NameExpr, self).__init__(kwargs)
        locs = _import()
  
        # String name;
        self._name = kwargs.get(u'name')

        typdct = kwargs.get(u'type')
        self._type = locs[typdct[u'@t']](typdct) if typdct else None
  
    @property
    def name(self): return self._name
    @name.setter
    def name(self, v): self._name = v
  
    @property
    def out_set(self): return set([])
    @out_set.setter
    def out_set(self, v): pass
  
    # should this return None or raise an Exception?
    @property
    def typee(self):
        t = self.symtab.get(self.name)
        return t.typee if t else None
    @typee.setter
    def typee(self, v): pass
  
    def __str__(self): return self.sanitize_ty(self._name)
