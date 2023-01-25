#!/usr/bin/env python

from . import _import

from .expression import Expression

class NameExpr(Expression):
    def __init__(self, kwargs={}, name=None):
        super(NameExpr, self).__init__(kwargs)
        locs = _import()
  
        # String name;
        self._name = kwargs.get(u'name', name)

        typdct = kwargs.get(u'type')
        self._type = locs[typdct[u'@t']](typdct) if typdct else None

        self._axparam = kwargs.get(u'axparam')
        t = self.symtab.get(self.name)
        if self == t:
            raise Exception("Circular")

    @property
    def axparam(self) : return self._axparam
    @axparam.setter
    def axparam(self, v) : self._axparam = v
    
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
        # Catch infinite recursion for axiom parameter params
        if self == t:
            new_name = self.name.replace('self.','', 1)
            t = self.symtab.get(new_name)
        return t.typee if t else None
    @typee.setter
    def typee(self, v): pass
  
    def __str__(self): return self.sanitize_ty(self._name)
