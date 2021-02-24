import operator as op
import re
import logging

import lib.const as C
import lib.visit as v

from .. import util
from ..meta.program import Program
from ..meta.clazz import Clazz, find_fld
from ..meta.method import Method
from ..meta.field import Field
from ..meta.statement import Statement, to_statements
from ..meta.expression import Expression, to_expression


"""
Replacing holes with solutions
"""
class HReplacer(object):

  def __init__(self, output_path, holes):
    self._output = output_path
    self._holes = holes

    self._cur_mtd = None

    self._sol = {} # { v : n }

    ## hole assignments for roles
    ## glblInit_fid__cid_????,StmtAssign,accessor_???? = n
    names = map(op.attrgetter("name"), self._holes)
    regex_role = r"({})__(\S+)_\S+ = (\d+)$".format('|'.join(names))

    # interpret the synthesis result
    with open(self._output, 'r') as f:
      for line in f:
        line = line.strip()
        try:
          items = line.split(',')
          func, kind, msg = items[0], items[1], ','.join(items[2:])
          m = re.match(regex_role, msg)
          if m:
            fid, cid, n = m.group(1), m.group(2), m.group(3)
            for hole in self._holes:
              if hole.name == fid and cid in repr(hole.clazz):
                logging.debug("solution: {} = {}".format(repr(hole), n))
                self._sol[hole] = n
        except IndexError: # not a line generated by custom codegen
          pass # if "Total time" in line: logging.info(line)

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
    if node in self._holes:
      cname = node.clazz.name
      fname = node.name
      if node in self._sol:
        n = self._sol[node]
        node.init = to_expression(unicode(n))
        logging.debug("replaced: {}.{} = {}".format(cname, fname, n))
      else: # solution not found?
        logging.debug("unresolved: {}.{}".format(cname, fname))

  @v.when(Method)
  def visit(self, node):
    self._cur_mtd = node

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node):
    if node.kind == C.E.ID:
      fld = find_fld(self._cur_mtd.clazz.name, node.id)
      if fld and fld in self._sol:
        n = self._sol[fld]
        logging.debug("replaced: {} @ {} with {}".format(node.id, self._cur_mtd.signature, n))
        return to_expression(unicode(n))

    return node


"""
Replacing regex generators with solutions
"""
class EGReplacer(object):

  def __init__(self, output_path, egens):
    self._output = output_path

    self._cur_mtd = None

    ## assignment appearances
    self._assigns = {} # { mtd : exp* }

    # interpret the synthesis result
    with open(self._output, 'r') as f:
      for line in f:
        line = line.strip()
        try:
          items = line.split(',')
          func, kind, msg = items[0], items[1], ','.join(items[2:])
          if kind == "StmtAssign":
            util.mk_or_append(self._assigns, func, msg.split('=')[-1].strip())
        except IndexError: # not a line generated by custom codegen
          pass # if "Total time" in line: logging.info(line)

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
      try:
        _assigns = self._assigns[repr(self._cur_mtd)]
        for e in node.es:
          s_e = str(e)
          for _exp in _assigns:
            if s_e in _exp:
              logging.debug("{} => {}".format(str(node), s_e))
              return e
      except KeyError:
        logging.debug("no expressions for {}".format(self._cur_mtd))

    return node


"""
Replacing method generators
"""
class MGReplacer(object):

  def __init__(self, output_path):
    self._output = output_path

    ## assignment appearances
    self._assigns = {} # { mtd : exp* }

    # interpret the synthesis result
    with open(self._output, 'r') as f:
      for line in f:
        line = line.strip()
        try:
          items = line.split(',')
          func, kind, msg = items[0], items[1], ','.join(items[2:])
          if kind in ["StmtAssign", "StmtVarDecl"]:
            util.mk_or_append(self._assigns, func, msg)
        except IndexError: # not a line generated by custom codegen
          pass # if "Total time" in line: logging.info(line)

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
    if not hasattr(node, "generator"): return
    logging.debug("retrieving {}.{}".format(node.clazz.name, node.name))
    # reset the body, which was previously delegated to the generator
    node.body = []

    # retrieve assignments from Sketch output
    mname = repr(node)
    if mname in self._assigns:
      # prologue: define return variable: _out
      rty = node.typ if node.typ != C.J.v else C.J.OBJ
      node.body = to_statements(node, u"{} _out;".format(rty))

      op_strip = op.methodcaller("strip")
      _assigns = self._assigns[mname]
      for _assign in _assigns:
        lhs, rhs = map(op_strip, _assign.split('='))
        if len(lhs.split(' ')) > 1: # i.e., var decl
          ty, v = map(op_strip, lhs.split(' '))
          ty = ty.split('@')[0] # TODO: cleaner way to retrieve/sanitize type
          node.body += to_statements(node, u"{} {} = {};".format(ty, v, rhs))
        else: # stmt assign
          node.body += to_statements(node, u"{};".format(_assign))

      # epilogue: return _out if necessary
      if node.typ != C.J.v:
        node.body += to_statements(node, u"return _out;")

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node): return node

