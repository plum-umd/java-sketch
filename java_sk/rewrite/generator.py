import copy
import logging

import lib.const as C
import lib.visit as v

from .. import util
from ..meta import class_nonce, register_class, class_lookup
from ..meta.program import Program
from ..meta.clazz import Clazz
from ..meta.method import Method
from ..meta.field import Field
from ..meta.statement import Statement
from ..meta.expression import Expression

"""
generator class Automaton { body_of_Automaton }

class RegularLanguage extends Automaton { ... }
class DBConnection {
    class Monitor extends Automaton { ... }
}

  =>

class Automaton1 { copy_of_body_of_Automaton }
class Automaton2 { copy_of_body_of_Automaton }

class RegularLanague extends Automaton1 { ... }
class DBConnection {
    class Monitor extends Automaton2 { ... }
}
"""
class CGenerator(object):

  # to avoid name conflict, use fresh counter as suffix
  __cnt = 0
  @classmethod
  def fresh_cnt(cls):
    cls.__cnt = cls.__cnt + 1
    return cls.__cnt

  def __init__(self): pass

  @v.on("node")
  def visit(self, node):
    """
    This is the generic method to initialize the dynamic dispatcher
    """

  @v.when(Program)
  def visit(self, node):
    self._pgr = node
    # collect class-level generators
    self._cgens = []
    for cls in node.classes:
      if C.mod.GN in cls.mods: self._cgens.append(cls)

  @v.when(Clazz)
  def visit(self, node):
    if not node.sup: return
    sup = class_lookup(node.sup)
    if sup not in self._cgens: return

    specialized_cls_name = u"{}{}".format(node.sup, CGenerator.fresh_cnt())
    specialized_cls = copy.deepcopy(sup)
    specialized_cls.name = specialized_cls_name
    register_class(specialized_cls)
    self._pgr.add_classes([specialized_cls])

    node.sup = specialized_cls_name
    logging.debug("specializing {} for {}".format(specialized_cls_name, node.name))

  @v.when(Field)
  def visit(self, node): pass

  @v.when(Method)
  def visit(self, node): pass

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node): return node

