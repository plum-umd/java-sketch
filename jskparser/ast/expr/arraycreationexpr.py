#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
from .expression import Expression

from . import _import

class ArrayCreationExpr(Expression):
    def __init__(self, kwargs={}):
        super(ArrayCreationExpr, self).__init__(kwargs)
        locs = _import()
    
        # Type type;
        t = kwargs.get(u'type', {})
        self._type = locs[t[u'@t']](t) if t else None
    
        # int arrayCount;
        self._arrayCount = kwargs.get(u'arrayCount', 0)
        
        # ArrayInitializerExpr initializer;
        init = kwargs.get(u'initializer')
        self._initializer = locs[u'ArrayInitializerExpr'](init) if init else None
    
        # List<Expression> dimensions;
        dim = kwargs.get(u'dimensions', {})
        self._dimensions = map(lambda e: locs[e[u'@t']](e) if u'@t' in e else [],
                               dim.get(u'@e', [])) if dim else []
    
        # List<List<AnnotationExpr>> arraysAnnotations;
        self._arraysAnnotations = []
        aa = kwargs.get(u'arraysAnnotations', {})
        ad = [None] if not aa else aa.get(u'@e')
        if ad[0]:
            print('ReferenceType annotations not implemented')
            for a in aa:
                self._arraysAnnotations.append(locs[u'AnnotationExpr'](a) if a else None)
                
        self.add_as_parent([self.typee, self.initializer]+self.dimensions)
                    
    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v
  
    @property
    def arrayCount(self): return self._arrayCount
    @arrayCount.setter
    def arrayCount(self, v): self._arrayCount = v
  
    @property
    def initializer(self): return self._initializer
    @initializer.setter
    def initializer(self, v): self._initializer = v
  
    @property
    def dimensions(self): return self._dimensions
    @dimensions.setter
    def dimensions(self, v): self._dimensions = v
