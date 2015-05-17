import logging

import lib.const as C
import lib.visit as v

from ..meta.program import Program
from ..meta.clazz import Clazz
from ..meta.method import Method
from ..meta.field import Field
from ..meta.statement import Statement
from ..meta.expression import Expression, to_expression

"""
class A {
    ... foo() {
        if (??) { doXoptional }
        if (??) { doYoptional }
    }
}

  =>

class A {
    static int e_h1 = ??;
    static int e_h2 = ??;
    ... foo() {
        if (A.e_h1) { doXoptional }
        if (A.e_h2) { doYoptional }
    }
}
"""
class EHole(object):

  # to avoid name conflict, use fresh counter as suffix
  __cnt = 0
  @classmethod
  def fresh_cnt(cls):
    cls.__cnt = cls.__cnt + 1
    return cls.__cnt

  def __init__(self):
    self._cur_mtd = None
    self._cur_s = None

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
    # to avoid introducing another hole variable
    # reset the context statement
    self._cur_s = None

  @v.when(Method)
  def visit(self, node):
    self._cur_mtd = node

  @v.when(Statement)
  def visit(self, node):
    self._cur_s = node
    return [node]

  @v.when(Expression)
  def visit(self, node):
    # in case of visiting field initializing Expression
    if not self._cur_s: return node

    if node.kind == C.E.HOLE:
      cls = self._cur_mtd.clazz
      hname = u"e_h{}".format(EHole.fresh_cnt())
      hole = Field(clazz=cls, mods=[C.mod.ST], typ=C.J.i, name=hname, init=node)
      cls.add_fld(hole)
      logging.debug("introducing e_hole {} @ {}".format(hname, self._cur_mtd.signature))
      return to_expression(hname)

    return node

