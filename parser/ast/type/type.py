#!/usr/bin/env python

from ..node import Node

class Type(Node):
  def __init__(self, kwargs={}):
    super(Type, self).__init__(kwargs)
    self._annotations = kwargs.get('annotations', [])

  @property
  def annotations(self): return self._annotations
  @annotations.setter
  def annotations(self, v): self._annotations = v

