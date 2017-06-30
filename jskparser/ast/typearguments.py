#!/usr/bin/env python

from . import _import

class TypeArguments(object):
    def __init__(self, kwargs={}):
        locs = _import()
        
        # List<Type> typeArguments;
        typeArguments = kwargs.get(u'typeArguments', [])
        self._typeArguments = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                                  typeArguments.get(u'@e', [])) if typeArguments else []

        # boolean usesDiamondOperator;
        self._usesDiamondOperator = kwargs.get(u'usesDiamondOperator', False)

    @property
    def typeArguments(self): return self._typeArguments

    def isUsingDiamondOperator(self): return self._usesDiamondOperator
