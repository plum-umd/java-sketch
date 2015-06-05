import logging

import lib.visit as v
import lib.const as C

from ..meta.program import Program
from ..meta.clazz import Clazz
from ..meta.method import Method
from ..meta.field import Field
from ..meta.statement import Statement
from ..meta.expression import Expression


"""
Finding hole declarations
"""
class HFinder(object):

  def __init__(self):
    self._holes = []

  @property
  def holes(self):
    return self._holes

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
    if node.init and node.init.kind == C.E.HOLE:
      logging.debug("hole: {}.{}".format(node.clazz.name, node.name))
      self._holes.append(node)

  @v.when(Method)
  def visit(self, node): pass

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node): return node


"""
Finding generators {| e* |}
"""
class GFinder(object):

  def __init__(self):
    self._gens = []

    self._cur_mtd = None

  @property
  def gens(self):
    return self._gens

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
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node):
    if node.kind == C.E.GEN:
      logging.debug("generator@{}: {}".format(self._cur_mtd.name, str(node)))
      self._gens.append(node)

    return node

