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
from ..meta.expression import Expression, to_expression

class SemanticChecker(object):

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
  def visit(self, node):
    # uninitialized array
    if util.is_array(node.typ) and not node.init:
      comp_typ = util.componentType(node.typ)
      magic_S = 256 # 0x100
      node.init = to_expression(u"new {} [ {} ]".format(comp_typ, magic_S))

  @v.when(Method)
  def visit(self, node):
    self._cur_mtd = node

    # abstract method cannot have a body
    if node.is_abstract and node.body:
      logging.debug("clean up abstract method: {}".format(node.signature))
      node.body = []

    # method without any proper return statement
    if not node.is_init and node.typ != C.J.v and not node.has_return:
      cls = class_lookup(node.typ)
      if not cls: return
      v = util.default_value(cls.JVM_notation)
      cast = u''
      if util.is_class_name(node.typ): cast = u"({})".format(node.typ)
      node.body += to_statements(node, u"return {}{};".format(cast, v))
      logging.debug("filling return value for {}: {}".format(node.signature, v))

  @v.when(Statement)
  def visit(self, node):

    # discard unnecessary branches, if possible
    if node.kind == C.S.IF:
      guard = str(node.e)
      if guard in ["0", "false"]:
        logging.debug("removing true branch in {}".format(self._cur_mtd.name))
        return node.f
      elif guard in ["1", "true"]:
        logging.debug("removing false branch in {}".format(self._cur_mtd.name))
        return node.t

    return [node]

  @v.when(Expression)
  def visit(self, node):
    # if a hole is still there, replace it with any number
    if node.kind == C.E.HOLE: return to_expression(u"0")

    elif node.kind == C.E.ID:
      # self ~> this
      if node.id == C.SK.self: return to_expression(C.J.THIS)

      # maybe translated field name, e.g., fld_clazz
      if '_' in node.id:
        suffix = node.id.split('_')[-1]
        if class_lookup(suffix):
          node.id = u'_'.join(node.id.split('_')[:-1])

    return node

