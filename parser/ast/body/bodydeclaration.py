#!/usr/bin/env python

from ..node import Node

class BodyDeclaration(Node):
  def __init__(self, kwargs={}):
    super(BodyDeclaration, self).__init__(kwargs)
    # List<AnnotationExpr>
    # self._annotations = kwargs.get('annotations', [])

  @property
  def annotations(self): return self._annotations
  @annotations.setter
  def annotations(self, v): self._annotations = v
