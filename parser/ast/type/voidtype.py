#!/usr/bin/env python

from .type import Type

class VoidType(Type):
    def __init__(self, kwargs={}):
        super(VoidType, self).__init__(kwargs)
        self._name = u'void'

    def __str__(self):
        return self._name
