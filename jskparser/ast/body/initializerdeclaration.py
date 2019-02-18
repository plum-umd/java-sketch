#!/usr/bin/env python

from __future__ import absolute_import
from .bodydeclaration import BodyDeclaration

IMPORTS = vars()

class InitializerDeclaration(BodyDeclaration):
  def __init__(self, kwargs={}):
    super(InitializerDeclaration, self).__init__(kwargs)
    # TODO: unfinished.
    # boolean isStatic;
    # BlockStmt block;

  @property
  def modifiers(self): return self._modifiers
  @modifiers.setter
  def modifiers(self, v): self._modifiers = v

  @property
  def typee(self): return self._type
  @typee.setter
  def typee(self, v): self._type = v
