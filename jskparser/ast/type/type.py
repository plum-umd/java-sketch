#!/usr/bin/env python

from . import _import

from ..node import Node

class Type(Node):
  def __init__(self, kwargs={}):
    super(Type, self).__init__(kwargs)

    locs = _import()

    # List<AnnotationExpr> annotations;
    annotations = kwargs.get(u'annotations', [])
    self._annotations = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                            annotations.get(u'@e', [])) if annotations else []

  @property
  def annotations(self): return self._annotations
  @annotations.setter
  def annotations(self, v): self._annotations = v

