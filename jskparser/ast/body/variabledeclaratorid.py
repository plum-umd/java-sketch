#!/usr/bin/env python

from ..node import Node

class VariableDeclaratorId(Node):
    def __init__(self, kwargs={}, name_str=""):
        super(VariableDeclaratorId, self).__init__(kwargs)
      
        # int arrayCount
        self._arrayCount = kwargs.get(u'arrayCount', 0)

        if name_str:
            self.name = name_str
  
    @property
    def arrayCount(self): return self._arrayCount
    @arrayCount.setter
    def arrayCount(self, v): self._arrayCount = v
  
    @property
    def in_set(self): return set([])
    @in_set.setter
    def in_set(self, v): pass
  
    @property
    def out_set(self): return set([])
    @out_set.setter
    def out_set(self, v): pass
  
    def __str__(self):
      return self.sanitize_ty(self.name)
