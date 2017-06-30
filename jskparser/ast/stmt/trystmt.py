#!/usr/bin/env python

from .statement import Statement
from . import _import

class TryStmt(Statement):
    def __init__(self, kwargs={}):
        super(TryStmt, self).__init__(kwargs)
        locs = _import()
    
        # List<VariableDeclarationExpr> resources;
        resources = kwargs.get(u'resources', {})
        self._resources = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                              resources.get(u'@e', [])) if resources else []
    
        # BlockStmt tryBlock;
        tryBlock = kwargs.get(u'tryBlock', {})
        self._tryBlock = locs[u'BlockStmt'](tryBlock) if tryBlock else None
        
        # List<CatchClause> catchs;
        catchs = kwargs.get(u'catchs', [])
        self._catchs = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                           catchs.get(u'@e', [])) if catchs else []
    
        # BlockStmt finallyBlock;
        finallyBlock = kwargs.get(u'finallyBlock', {})
        self._finallyBlock = locs[u'BlockStmt'](finallyBlock) if finallyBlock else None

        self.add_as_parent(self.resources+[self.tryBlock]+self.catchs+[self.finallyBlock])
    
    @property
    def resources(self): return self._resources
    @resources.setter
    def resources(self, v): self._resources = v
  
    @property
    def tryBlock(self): return self._tryBlock
    @tryBlock.setter
    def tryBlock(self, v): self._tryBlock = v
  
    @property
    def catchs(self): return self._catchs
    @catchs.setter
    def catchs(self, v): self._catchs = v
    
    @property
    def finallyBlock(self): return self._finallyBlock
    @finallyBlock.setter
    def finallyBlock(self, v): self._finallyBlock = v
