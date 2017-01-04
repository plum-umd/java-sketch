#!/usr/bin/env python

from node import Node

from . import _import

class ImportDeclaration(Node):
    def __init__(self, kwargs={}):
        super(ImportDeclaration, self).__init__(kwargs)
        
        locs = _import()

        # NameExpr name;
        name = kwargs.get(u'name', {})
        self._name = locs[name[u'@t']](name) if name else None
        # boolean static_;
        self.static = kwargs.get(u'static_', False)
        # boolean asterisk;
        self.asterisk = kwargs.get(u'asterisk', False)
        # boolean isEmptyImportDeclaration;
        self.isEmptyDeclaration = kwargs.get(u'isEmptyImportDeclarationasterisk', False)

    @property
    def static(self): return self._static
    @static.setter
    def static(self, v): self._static = v
  
    @property
    def asterisk(self): return self._asterisk
    @asterisk.setter
    def asterisk(self, v): self._asterisk = v
  
    @property
    def isEmptyDeclaration(self): return self._isEmptyDeclaration
    @isEmptyDeclaration.setter
    def isEmptyDeclaration(self, v): self._isEmptyDeclaration = v

    def __str__(self): return str(self.name)
