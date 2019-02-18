from __future__ import absolute_import
import logging

import lib.const as C
import lib.visit as v

from .. import util
from ..meta.program import Program
from ..meta.clazz import Clazz
from ..meta.method import Method
from ..meta.field import Field
from ..meta.statement import Statement, to_statements
from ..meta.expression import Expression

class Desugar(object):

  def __init__(self):
    self._cur_mtd = None

  @v.on("node")
  def visit(self, node):
    """
    This is the generic method to initialize the dynamic dispatcher
    """

  @v.when(Program)
  def visit(self, node): pass

  @v.when(Clazz)
  def visit(self, node): pass

  @v.when(Field)
  def visit(self, node): pass

  @v.when(Method)
  def visit(self, node):
    self._cur_mtd = node

  @v.when(Statement)
  def visit(self, node):
    if node.kind == C.S.MINREPEAT:
      b = '\n'.join(map(str, node.b))
      body = u""
      for i in xrange(9): # TODO: parameterize
        body += u"""
          if (??) {{ {} }}
        """.format(b)
      logging.debug("desugaring minrepeat @ {}".format(self._cur_mtd.name))
      return to_statements(self._cur_mtd, body)

    return [node]

  @v.when(Expression)
  def visit(self, node): return node

