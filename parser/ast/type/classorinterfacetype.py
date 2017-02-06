#!/usr/bin/env python

from .type import Type

from ..typearguments import TypeArguments

class ClassOrInterfaceType(Type):
    def __init__(self, kwargs={}):
        if kwargs:
            super(ClassOrInterfaceType, self).__init__(kwargs)
            # ClassOrInterfaceType
            self._scope = None
            scope = kwargs.get(u'scope')
            if scope:
                scope.update({u'@t':u'ClassOrInterfaceType'})
                self._scope = ClassOrInterfaceType(scope)
            self._any = kwargs.get('any')

            # TypeArguments typeArguments
            self._typeArguments = TypeArguments(kwargs.get(u'typeArguments', {}))
            
            # boolean any = false;
            self._any = False

    @property
    def typee(self): return self
    @typee.setter
    def typee(self, v): pass
  
    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, v): self._scope = v

    @property
    def anyy(self): return self._any
    @anyy.setter
    def anyy(self, v): self._any = v

    @property
    def typeArguments(self): return self._typeArguments
    @typeArguments.setter
    def typeArguments(self, v): self._typeArguments = v

    def typeArgs(self):
        return self.typeArguments.typeArguments
        
    def isUsingDiamondOperator(self):
        return self.typeArguments.isUsingDiamondOperator() if self.typeArguments else False

    def __str__(self):
        return '{}${}'.format(str(self.scope), self.name) if self.scope else self.name
