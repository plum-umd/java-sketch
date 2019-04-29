#!/usr/bin/env python

from __future__ import absolute_import
from .node import Node
from . import _import

class CompilationUnit(Node):
    def __init__(self, kwargs={}):
        if kwargs.get(u'GSYMTAB'): self.GSYMTAB.clear()

        super(CompilationUnit, self).__init__(kwargs)
        locs = _import()
      
        # PackageDeclaration
        self._package = kwargs.get('pakage', {})
      
        # List<ImportDeclaration>
        imports = kwargs.get('imports')
        self._imports = [locs[u'ImportDeclaration'](x) for x in
                         imports.get('@e', [])] if imports else []
        
        # for i in self._imports: print i.name
        # List<TypeDeclaration>
        types = kwargs.get('types')
        self._types = [locs[x['@t']](x) for x in
                       types.get('@e', [])] if types else []
        self._gsymtab = self.GSYMTAB
          
    @property
    def package(self): return self._package
    @package.setter
    def package(self, v): self._package = v
    
    @property
    def imports(self): return self._imports
    @imports.setter
    def imports(self, v): self._imports = v
    
    @property
    def types(self): return self._types
    @types.setter
    def types(self, v): self._types = v
  
    @property
    def gsymtab(self): return self._gsymtab
    @gsymtab.setter
    def gsymtab(self, v): self._gsymtab = v
