#!/usr/bin/env python

from . import _import
from .statement import Statement


class BlockStmt(Statement):
    def __init__(self, kwargs={}):
        super(BlockStmt, self).__init__(kwargs)
        locs = _import()
    
        # List<Statement> stmts
        self._stmts = []
    
        json_stmts = kwargs.get(u'stmts', {})
        if json_stmts:
            for s in json_stmts.get(u'@e', []):
                stmt = locs[s[u'@t']](s)
                if stmt: self._stmts.append(stmt)
    
        self.add_as_parent(self.stmts)
    
    @property
    def stmts(self): return self._stmts
    @stmts.setter
    def stmts(self, v): self._stmts = v
