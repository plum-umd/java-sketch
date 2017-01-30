#!/usr/bin/env python

from .type import Type

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
            # TypeArguments
            # self._typeArguments = kwargs.get('typeArguments')

    @property
    def typee(self): return self
    @typee.setter
    def typee(self, v): pass
  
    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, v): self._scope = v

    @property
    def anyCIT(self): return self._any
    @anyCIT.setter
    def anyCIT(self, v): self._any = v

    def __str__(self):
        return '{}${}'.format(str(self.scope), self.name) if self.scope else self.name
