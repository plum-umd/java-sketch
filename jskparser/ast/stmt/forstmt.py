#!/usr/bin/env python

from __future__ import absolute_import
from .statement import Statement
from . import _import

class ForStmt(Statement):
    def __init__(self, kwargs={}):
        super(ForStmt, self).__init__(kwargs)
        locs = _import()
    
        # List<Expression> init;
        init = kwargs.get(u'init', {})
        self._init = [locs[x[u'@t']](x) if u'@t' in x else [] for x in
                         init.get(u'@e', [])] if init else []
        
        # Expression compare;
        compare = kwargs.get(u'compare', {})
        self._compare = locs[compare[u'@t']](compare) if compare else None
        
        # List<Expression> update;
        update = kwargs.get(u'update', {})
        self._update = [locs[x[u'@t']](x) if u'@t' in x else [] for x in
                         update.get(u'@e', [])] if update else []
        
        # Statement body;
        body = kwargs.get(u'body', {})
        self._body = locs[body[u'@t']](body) if body else None

        self.add_as_parent(self.init+[self.compare]+self.update+[self.body])
    
    @property
    def init(self): return self._init
    @init.setter
    def init(self, v): self._init = v
  
    @property
    def compare(self): return self._compare
    @compare.setter
    def compare(self, v): self._compare = v
  
    @property
    def update(self): return self._update
    @update.setter
    def update(self, v): self._update = v
  
    @property
    def body(self): return self._body
    @body.setter
    def body(self, v): self._body = v
