#!/usr/bin/env python

from .type import Type

_type_dicts = {
    "bit":{u'ordinal': 0, u'nameOfBoxedType': u'Bit', u'name': u'Bit'},
    "boolean":{u'ordinal': 1, u'nameOfBoxedType': u'Boolean', u'name': u'Boolean'},
    "char":{u'ordinal': 2, u'nameOfBoxedType': u'Character', u'name': u'Char'},
    "byte":{u'ordinal': 3, u'nameOfBoxedType': u'Byte', u'name': u'Byte'},
    "short":{u'ordinal': 4, u'nameOfBoxedType': u'Short', u'name': u'Short'},
    "int":{u'ordinal': 5, u'nameOfBoxedType': u'Integer', u'name': u'Int'},
    "long":{u'ordinal': 6, u'nameOfBoxedType': u'Long', u'name': u'Long'},
    "float":{u'ordinal': 7, u'nameOfBoxedType': u'Float', u'name': u'Float'},
    "double":{u'ordinal': 8, u'nameOfBoxedType': u'Double', u'name': u'Double'}
}

class PrimitiveType(Type):
    def __init__(self, kwargs={}, type_name=None):
        super(PrimitiveType, self).__init__(kwargs)
        if type_name:
            typdct = _type_dicts.get(type_name)
        else:
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
