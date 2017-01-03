#!/usr/bin/env python

from .type import Type

class ClassOrInterfaceType(Type):
  def __init__(self, kwargs={}):
    if kwargs:
      super(ClassOrInterfaceType, self).__init__(kwargs)
      # ClassOrInterfaceType
      self._scope = ClassOrInterfaceType(kwargs.get('scope'))
      self._any = kwargs.get('any')
      # TypeArguments
      # self._typeArguments = kwargs.get('typeArguments')

  @property
  def scope(self): return self._scope
  @scope.setter
  def scope(self, v): self._scope = v

  @property
  def anyCIT(self): return self._any
  @anyCIT.setter
  def anyCIT(self, v): self._any = v

  def __str__(self):
      return self.name
