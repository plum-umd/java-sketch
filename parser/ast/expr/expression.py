#!/usr/bin/env python

from ..node import Node

class Expression(Node):
  def __init__(self, kwargs={}):
    super(Expression, self).__init__(kwargs)
