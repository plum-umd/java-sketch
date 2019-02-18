#!/usr/bin/env python

from __future__ import absolute_import
from .statement import Statement

from . import _import

class SwitchEntryStmt(Statement):
    def __init__(self, kwargs={}):
        super(SwitchEntryStmt, self).__init__(kwargs)
        locs = _import()
    
        # Expression label;
        s = kwargs.get(u'label', {})
        self._label = locs[s[u'@t']](s) if s else None
    
        # List<Statement> stmts;
        s = kwargs.get(u'stmts', {})
        self._stmts = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                          s.get(u'@e', [])) if s else []

        self.add_as_parent([self.label]+self.stmts)

        self._adt_mtds = kwargs.get(u'adt_mtds', [])
        
    @property
    def label(self): return self._label
    @label.setter
    def label(self, v): self._label = v

    @property
    def adt_mtds(self): return self._adt_mtds
    @adt_mtds.setter
    def adt_mtds(self, v): self._adt_mtds = v
    
    @property
    def stmts(self): return self._stmts
    @stmts.setter
    def stmts(self, v): self._stmts = v
    
