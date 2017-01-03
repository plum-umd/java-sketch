#!/usr/bin/env python

from .literalexpr import LiteralExpr

class NullLiteralExpr(LiteralExpr):
  def __init__(self, kwargs={}):
    super(NullLiteralExpr, self).__init__(kwargs)
