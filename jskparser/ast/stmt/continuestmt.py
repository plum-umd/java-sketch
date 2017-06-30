#!/usr/bin/env python

from .statement import Statement

class ContinueStmt(Statement):
    def __init__(self, kwargs={}):
        super(ContinueStmt, self).__init__(kwargs)
        
        # String id;
        self._id = kwargs.get(u'id', '')
        
    @property
    def idd(self): return self._id
    @idd.setter
    def idd(self, v): self._id = v
