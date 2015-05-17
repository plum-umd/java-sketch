import logging

import lib.const as C
import lib.visit as v

from .. import util
from ..meta import class_lookup
from ..meta.program import Program
from ..meta.clazz import Clazz
from ..meta.method import Method
from ..meta.field import Field
from ..meta.statement import Statement, to_statements
from ..meta.expression import Expression

class SemanticChecker(object):

  def __init__(self): pass

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

    # method without any proper return statement
    if not node.is_init and node.typ != C.J.v and not node.has_return:
      cls = class_lookup(node.typ)
      if not cls: return
      v = util.default_value("java", cls.JVM_notation, node.name)
      cast = u''
      if util.is_class_name(node.typ): cast = u"({})".format(node.typ)
      node.body += to_statements(node, u"return {}{};".format(cast, v))
      logging.debug("filling return value for {}: {}".format(node.signature, v))

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node): return node

