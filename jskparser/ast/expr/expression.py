#!/usr/bin/env python

from __future__ import absolute_import
from . import _import

from ..node import Node

class Expression(Node):
    def __init__(self, kwargs={}):
        super(Expression, self).__init__(kwargs)
        # locs = _import()

        # # This is the return type and will be stored as a child of the method
        # typdct = kwargs.get(u'type', {})
        # self._type = locs[typdct[u'@t']](typdct) if typdct and u'@t' in typdct else None

        
    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v
