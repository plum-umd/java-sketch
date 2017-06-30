#!/usr/bin/env python

from .bodydeclaration import BodyDeclaration

from ..type.classorinterfacetype import ClassOrInterfaceType
from ..typeparameter import TypeParameter

from . import _import

class ConstructorDeclaration(BodyDeclaration):
    def __init__(self, kwargs={}):
        super(ConstructorDeclaration, self).__init__(kwargs)
        locs = _import()
    
        # int modifiers
        self._modifiers = kwargs.get(u'modifiers', 0)
    
        # int arrayCount;
        self._arrayCount = kwargs.get(u'arrayCount', 0)
    
        # List<Parameter>
        params = kwargs.get(u'parameters', {})
        self._parameters = map(lambda x: locs[x[u'@t']](x),
                               params.get(u'@e', [])) if params else []

        # List<TypeParameter>
        typeParameters = kwargs.get(u'typeParameters', {})
        self._typeParameters = map(lambda x: TypeParameter(x) if u'@t' in x else [],
                                   typeParameters.get(u'@e', [])) if typeParameters else []

        # Type (just the class name wrapped in a Type)
        self._type = ClassOrInterfaceType(kwargs.get(u'name',{}))
    
        # List<NameExpr> throws_;
        throws = kwargs.get(u'throws_', {})
        self._throws = map(lambda x: locs[u'NameExpr'](x) if u'@t' in x else [],
                           throws.get(u'@e', [])) if throws else []
    
        # BlockStmt block;
        body = kwargs.get(u'block')
        self._body = locs[u'BlockStmt'](body) if body else None
    
        # List<TypeParameter>
        # self._typeParameters = None

        self.add_as_parent(self.parameters+self.typeParameters+[self.typee]+self.throws+[self.body])
    
    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v
  
    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v
  
    @property
    def parameters(self): return self._parameters
    @parameters.setter
    def parameters(self, v): self._parameters = v
  
    @property
    def body(self): return self._body
    @body.setter
    def body(self, v): self._body = v
  
    @property
    def arrayCount(self): return self._arrayCount
    @arrayCount.setter
    def arrayCount(self, v): self._arrayCount = v
  
    @property
    def throws(self): return self._throws
    @throws.setter
    def throws(self, v): self._throws = v

    @property
    def typeParameters(self): return self._typeParameters
    @typeParameters.setter
    def typeParameters(self, v): self._typeParameters = v
  
    def param_typs(self): return map(lambda p: p.typee, self.parameters)
    def param_names(self): return map(lambda p: p.name, self.parameters)

    def sig(self):
        return 'm{}'.format(str(self))
  
    def __str__(self):
        cls = self.get_coid()
        nm = '{0}_{0}'.format(str(cls))
        if cls.isinner(): nm += '_{}'.format(str(cls.get_coid()))
        params = map(self.sanitize_ty, map(lambda p: p.typee.name, self.parameters))
        return u'_'.join([nm] + params)
