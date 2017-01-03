#!/usr/bin/env python

from .expression import Expression

class LiteralExpr(Expression):
  def __init__(self, kwargs={}):
    super(LiteralExpr, self).__init__(kwargs)
