#!/usr/bin/env python

from .expression import Expression

from . import _import

class ArrayRangeAccessExpr(Expression):
    def __init__(self, kwargs={}):
        super(ArrayRangeAccessExpr, self).__init__(kwargs)
        locs = _import()
    
        # unicode name;
        n = kwargs.get(u'name', {})
        self._name = locs[n[u'@t']](n) if n else None
    
        # Expression index;
        iS = kwargs.get(u'indexStart', {})
        self._indexStart = locs[iS[u'@t']](iS) if iS else None

        iE = kwargs.get(u'subLen', {})
        self._subLen = locs[iE[u'@t']](iE) if iE else None

        self.add_as_parent([self.indexStart, self.subLen])
                   
    @property
    def name(self): return self._name.name
    @name.setter
    def name(self, v): self._name = v
  
    @property
    def nameExpr(self): return self._name
  
    @property
    def indexStart(self): return self._indexStart
    @indexStart.setter
    def indexStart(self, v): self._indexStart = v

    @property
    def subLen(self): return self._subLen
    @subLen.setter
    def subLen(self, v): self._subLen = v
  
    @property
    def lbl(self): return (self._name.name, self.ati)
    @lbl.setter
    def lbl(self, v): self._lbl = v

    @property
    def typee(self):
        if self.name in self.symtab:
            return self.symtab[self.name].typee
        return super(ArrayRangeAccessExpr, self).typee
