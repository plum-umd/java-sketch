#!/usr/bin/env python

from .type import Type

from . import _import

class ReferenceType(Type):
    def __init__(self, kwargs={}):
        super(ReferenceType, self).__init__(kwargs)
        locs = _import()

        typdct = kwargs.get('type')
        self._type = locs[typdct['@t']](typdct)

        self._arrayCount = kwargs.get(u'arrayCount', 0)

        # List<Expression> values;
        v = kwargs.get(u'values', {})
        if type(v) == list:
            self._values = v
        else:
            self._values = map(lambda e: locs[e[u'@t']](e) if u'@t' in e else [],
                               v.get(u'@e', [])) if v else []

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def name(self): return self._type.name
    @name.setter
    def name(self, v): self._type.name = v

    @property
    def arrayCount(self): return self._arrayCount
    @arrayCount.setter
    def arrayCount(self, v): self._arrayCount = v

    @property
    def values(self): return self._values
    @values.setter
    def values(self, v): self._values = v
  
    def __str__(self): return self.name

