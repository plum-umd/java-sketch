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

        # List<List<AnnotationExpr>> arraysAnnotations;
        self._arraysAnnotations = []

        aa = kwargs.get(u'arraysAnnotations', {})
        ad = [None] if not aa else aa.get(u'@e')
        if ad[0]:
            print 'ReferenceType annotations not implemented'
            for a in aa:
                self._arraysAnnotations.append(locs[u'AnnotationExpr'](a) if a else None)

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

