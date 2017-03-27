#!/usr/bin/env python

from ..node import Node

class Statement(Node):
  def __init__(self, kwargs={}):
    super(Statement, self).__init__(kwargs)
