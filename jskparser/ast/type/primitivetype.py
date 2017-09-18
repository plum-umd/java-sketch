#!/usr/bin/env python

from .type import Type

class PrimitiveType(Type):
    def __init__(self, kwargs={}):
        super(PrimitiveType, self).__init__(kwargs)
        typdct = kwargs.get('type')
        self._type = typdct
        self._name = typdct['name'].lower()
        self._nameOfBoxedType = typdct.get(u'nameOfBoxedType', '')
                
    @property
    def nameOfBoxedType(self): return self._nameOfBoxedType
    @nameOfBoxedType.setter
    def nameOfBoxedType(self, v): self._nameOfBoxedType = v

    @property
    def typee(self): return self
    @typee.setter
    def typee(self, v): pass

    @property
    def in_set(self): return set([])
    @in_set.setter
    def in_set(self, v): pass

    @property
    def out_set(self): return set([])
    @out_set.setter
    def out_set(self, v): pass

    def __str__(self):
        return self.name
