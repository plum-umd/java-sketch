from __future__ import absolute_import
try: unicode
except: unicode = u"".__class__
from lib.typecheck import *
import lib.visit as v
import lib.const as C

from .. import util
from ..meta import class_lookup
from ..meta.program import Program
from ..meta.clazz import Clazz
from ..meta.method import Method
from ..meta.field import Field
from ..meta.statement import Statement
from ..meta.expression import Expression


"""
Replacing collections of interface types with actual classes
"""
class Collection(object):

  __impl = { \
    C.J.MAP: C.J.TMAP, \
    C.J.LST: C.J.LNK, \
    C.J.LNK: C.J.LNK, \
    C.J.STK: C.J.STK, \
    C.J.QUE: C.J.DEQ }

  # autobox type parameters and/or replace interfaces with implementing classes
  # e.g., List<T> x = new List<T>(); => new ArrayList<T>();
  # this should *not* be recursive, e.g., Map<K, List<V>> => TreeMap<K, List<V>>
  @staticmethod
  def repl_itf(tname, init=True):
    if not util.is_collection(tname): return tname
    _ids = util.of_collection(tname)
    ids = [util.autoboxing(i) for i in _ids]
    collection = ids[0]
    if init: collection = Collection.__impl[collection]
    generics = ids[1:] # don't be recursive, like map(repl_itf, ids[1:])
    return u"{}<{}>".format(collection, ','.join(generics))


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
    node.typ = Collection.repl_itf(node.typ, False)

  @v.when(Method)
  def visit(self, node): pass

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node):
    if node.kind == C.E.NEW:
      if node.e.kind == C.E.CALL:
        mid = unicode(node.e.f)
        if util.is_class_name(mid):
          node.e.f.id = Collection.repl_itf(mid)

    return node


