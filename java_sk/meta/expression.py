import cStringIO
import ast
import operator as op
from functools import partial

import antlr3
from antlr3.tree import CommonTree as AST
from grammar.JavaLexer import JavaLexer as Lexer
from grammar.JavaParser import JavaParser as Parser

from lib.typecheck import *
import lib.const as C
from lib.enum import enum
import lib.visit as v

from .. import util
from ..anno import parse_anno

from . import class_lookup
import clazz

# e ::= anno | ?? | {| e* |} | c | id | uop e | e bop e | e.e | e[e] | new e | e(e*) | (e)e
C.E = enum("ANNO", "HOLE", "GEN", "C", "ID", "UOP", "BOP", "DOT", "IDX", "NEW", "CALL", "CAST")
C.uop = ['+', '-', '~', '!', "++", "--"]
C.bop = ["||", "&&", '|', '^', '&'] \
      + ['+', '-', '*', '/', '%'] \
      + ["<<", ">>>", ">>"]
C.rop = ["==", "!=", "<=", ">=", '<', '>']

class Expression(v.BaseNode):

  def __init__(self, k, **kwargs):
    self._kind = k
    for key in kwargs:
      setattr(self, key, kwargs[key])

  @property
  def kind(self):
    return self._kind

  def __str__(self):
    buf = cStringIO.StringIO()
    if self._kind == C.E.ANNO:
      buf.write(str(self.anno))

    elif self._kind == C.E.HOLE:
      buf.write(C.T.HOLE)

    elif self._kind == C.E.GEN:
      if self.consts:
        buf.write("{| ")
        buf.write(" | ".join(map(str, self.consts)))
        buf.write(" |}")
      else:
        buf.write(C.T.HOLE)

    elif self._kind == C.E.C:
      buf.write(str(self.c))

    elif self._kind == C.E.ID:
      if hasattr(self, "ty"): buf.write(self.ty + ' ')
      buf.write(self.id)

    elif self._kind == C.E.UOP:
      buf.write(self.op + ' ' + str(self.e))

    elif self._kind == C.E.BOP:
      buf.write(str(self.le) + ' ' + self.op + ' ' + str(self.re))

    elif self._kind == C.E.DOT:
      buf.write(str(self.le) + '.' + str(self.re))

    elif self._kind == C.E.IDX:
      buf.write(str(self.e) + '[' + str(self.idx) + ']')

    elif self._kind == C.E.NEW:
      buf.write(C.J.NEW + ' ' + str(self.e))
      if self.init: buf.write(self.init)

    elif self._kind == C.E.CALL:
      buf.write(str(self.f) + '(' + ", ".join(map(str, self.a)) + ')')

    elif self._kind == C.E.CAST:
      buf.write('(' + str(self.ty) + ')' + str(self.e))

    return buf.getvalue()

  def __repr__(self):
    return self.__str__()

  # retrieve the type of the Expression
  def typ(self, mtd):
    curried = lambda e: e.typ(mtd)
    if self.kind == C.E.ANNO:
      anno = self.anno
      if anno.name in [C.A.NEW, C.A.OBJ]: return anno.typ
      elif anno.name in [C.A.CMP, C.A.CMP_STR]: return C.J.i

    elif self.kind == C.E.C:
      if self.c == C.J.N: return C.J.OBJ
      elif self.c in [C.J.TRUE, C.J.FALSE]: return C.J.z
      else: return C.J.i

    elif self.kind == C.E.ID:
      if hasattr(self, "ty"): return self.ty
      v = self.id
      try: return mtd.vars[v]
      except (AttributeError, KeyError):
        if util.is_class_name(v): return v
        elif util.is_str(v): return C.J.STR
        else:
          fld = None
          if mtd: fld = clazz.find_fld(mtd.clazz.name, v)
          if fld: return fld.typ
          else: return C.J.OBJ

    elif self.kind == C.E.UOP:
      return C.J.i

    elif self.kind == C.E.BOP:
      return C.J.i

    elif self.kind == C.E.DOT:
      # with package names, e.g., javax.swing.SwingUtilities
      # also, avoid constant, e.g., KeyEvent.VK_*
      if util.is_class_name(self.re.id) and class_lookup(self.re.id):
        return self.re.id
      else:
        rcv_ty = curried(self.le)
        if self.re.id == C.J.THIS: # ClassName.this
          return rcv_ty
        else: # instance field
          fld = clazz.find_fld(rcv_ty, self.re.id)
          return fld.typ

    elif self.kind == C.E.IDX:
      typ = curried(self.e)
      return typ[:-2] # trim last "[]"

    elif self.kind == C.E.NEW:
      return curried(self.e)

    elif self.kind == C.E.CALL:
      arg_typs = map(curried, self.a)
      if self.f.kind == C.E.DOT:
        # inner class's <init>, e.g., ViewGroup.LayoutParams(...)
        if util.is_class_name(self.f.re.id):
          return unicode(self.f)
        else: # rcv.mid
          rcv_ty = curried(self.f.le)
          mname = self.f.re.id
          mtd_callee = clazz.find_mtd_by_sig(rcv_ty, mname, arg_typs)
          return mtd_callee.typ
      else: # mid
        mname = self.f.id
        if mname in C.typ_arrays:
          return C.J.i
        elif util.is_class_name(mname): # <init>
          return mname
        elif mname == C.J.SUP and mtd.is_init: # super() inside <init>
          return mtd.clazz.sup
        else:
          if mname == C.J.SUP: # super(...)
            mtd_callee = clazz.find_mtd_by_sig(mtd.clazz.sup, mtd.name, mtd.param_typs)
          else: # member methods
            mtd_callee = clazz.find_mtd_by_sig(mtd.clazz.name, mname, arg_typs)
          return mtd_callee.typ

    elif self.kind == C.E.CAST:
      return curried(self.ty)

    else: # HOLE, GEN
      return C.J.i

  def accept(self, visitor):
    f = op.methodcaller("accept", visitor)
    if self._kind == C.E.GEN:
      self.consts = map(f, self.consts)
    elif self._kind in [C.E.BOP, C.E.DOT]:
      self.le = f(self.le)
      self.re = f(self.re)
    elif self._kind == C.E.IDX:
      self.e = f(self.e)
      self.idx = f(self.idx)
    elif self._kind in [C.E.UOP, C.E.NEW]:
      self.e = f(self.e)
    elif self._kind == C.E.CALL:
      self.f = f(self.f)
      self.a = map(f, self.a)
    elif self._kind == C.E.CAST:
      self.ty = f(self.ty)
      self.e = f(self.e)
    return visitor.visit(self)

  def exists(self, pred):
    if pred(self): return True
    f = op.methodcaller("exists", pred)
    if self._kind == C.E.GEN:
      return util.exists(f, self.consts)
    elif self._kind in [C.E.BOP, C.E.DOT]:
      return f(self.le) or f(self.re)
    elif self._kind == C.E.IDX:
      return f(self.e) or f(self.idx)
    elif self._kind in [C.E.UOP, C.E.NEW]:
      return f(self.e)
    elif self._kind == C.E.CALL:
      return f(self.f) or util.exists(f, self.a)
    elif self._kind == C.E.CAST:
      return f(self.ty) or f(self.e)
    else:
      return False

  @property
  def has_call(self):
    f = lambda e: e.kind == C.E.CALL
    return self.exists(f)

  @property
  def has_str(self):
    f = lambda e: e.kind == C.E.ID and util.is_str(e.id)
    return self.exists(f)


# for easier currying
@takes(optional("Method"), Expression)
@returns(unicode)
def typ_of_e(mtd, e):
  return e.typ(mtd)


# @Anno -> E(ANNO, @Anno)
#@takes(anno.Anno) # can't check due to mutual import
@returns(Expression)
def gen_E_anno(x):
  return Expression(C.E.ANNO, anno=x)


# () -> E(HOLE)
@takes(nothing)
@returns(Expression)
def gen_E_hole():
  return Expression(C.E.HOLE)


@takes(optional(list_of(Expression)))
@returns(Expression)
def gen_E_gen(consts=[]):
  return Expression(C.E.GEN, consts=consts)


# x -> E(C, x)
@takes((int, unicode))
@returns(Expression)
def gen_E_c(x):
  return Expression(C.E.C, c=x)


# str(, str) -> E(ID, str(, str))
@takes(unicode, optional(unicode))
@returns(Expression)
def gen_E_id(name, ty=None):
  if ty: return Expression(C.E.ID, id=name, ty=ty)
  else: return Expression(C.E.ID, id=name)


# op, e -> E(UOP, op, e)
@takes(unicode, Expression)
@returns(Expression)
def gen_E_uop(op, e):
  return Expression(C.E.UOP, op=op, e=e)


# op, le, re -> E(BOP, op, le, re)
@takes(unicode, Expression, Expression)
@returns(Expression)
def gen_E_bop(op, le, re):
  return Expression(C.E.BOP, op=op, le=le, re=re)


# le, re -> E(DOT, le, re)
@takes(Expression, Expression)
@returns(Expression)
def gen_E_dot(le, re):
  return Expression(C.E.DOT, le=le, re=re)


# e, idx -> E(IDX, e, idx)
@takes(Expression, Expression)
@returns(Expression)
def gen_E_idx(e, idx):
  return Expression(C.E.IDX, e=e, idx=idx)


# e(, str) -> E(NEW, e)
@takes(Expression, optional(unicode))
@returns(Expression)
def gen_E_new(e, init=None):
  return Expression(C.E.NEW, e=e, init=init)


# f, a -> E(CALL, f, a)
@takes(Expression, list_of(Expression))
@returns(Expression)
def gen_E_call(f, a):
  return Expression(C.E.CALL, f=f, a=a)


# ty, e -> E(CAST, ty, e)
@takes(Expression, Expression)
@returns(Expression)
def gen_E_cast(ty, e):
  return Expression(C.E.CAST, ty=ty, e=e)


# parse an expression
# (EXPRESSION ...)
@takes(AST, optional("Clazz"))
@returns(Expression)
def parse_e(node, cls=None):
  curried_e = lambda n: parse_e(n, cls)

  kind = node.getText()
  _nodes = node.getChildren()
  # (E... STH) or (None STH) (i.e., synthetic node)
  if len(_nodes) == 1 and (not kind or kind == C.T.EXP): # unwrap
    return curried_e(node.getChild(0))
  else: # already in a recursive expression
    _node = node

  # (A... )
  if kind == C.T.ANNO:
    a = parse_anno(_node)
    e = Expression(C.E.ANNO, anno=a)

  # ??
  elif kind == C.T.HOLE:
    e = gen_E_hole()

  # (CAST (TYPE (E... ty)) e)
  elif kind == C.T.CAST:
    t_node = _node.getChild(0).getChild(0)
    e_node = util.mk_v_node_w_children(_node.getChildren()[1:])
    ty = curried_e(t_node)
    re = curried_e(e_node)
    e = gen_E_cast(ty, re)

  # (bop le re)
  elif kind in C.bop + C.rop and _node.getChildCount() == 2:
    le = curried_e(_node.getChild(0))
    re = curried_e(_node.getChild(1))
    e = gen_E_bop(kind, le, re)

  # (uop e)
  elif kind in C.uop:
    e_node = util.mk_v_node_w_children(_node.getChildren())
    re = curried_e(e_node)
    e = gen_E_uop(kind, re)

  # const or id
  elif len(_nodes) <= 1:
    if kind:
      try:
        if kind in [C.J.TRUE, C.J.FALSE, C.J.N]: e = gen_E_c(unicode(kind))
        else: e = gen_E_c(ast.literal_eval(kind))
      except Exception: e = gen_E_id(unicode(kind))
    else: e = gen_E_id(_nodes[0].getText())

  # (E... new Clazz (ARGUMENT ...) ('{' (DECL ...)* '}')?)
  # (E... new typ([])* '{' ... '}')
  # (E... new typ '[' sz ']')
  elif _nodes[0].getText() == C.J.NEW:
    is_init = util.exists(lambda n: n.getText() == C.T.ARG, _nodes)
    if is_init: # class <init>
      if _nodes[-1].getText() == '}': # anonymous inner class
        for i, n in enumerate(_nodes):
          if n.getText() == '{':
            c_node = util.mk_v_node_w_children(_nodes[1:i])
            decl_nodes = _nodes[i+1:-1]
            break
        c = curried_e(c_node)
        name = clazz.anony_name(cls)
        anony = clazz.Clazz(name=name, itfs=[unicode(c.f)], outer=cls)
        map(partial(clazz.parse_decl, anony), decl_nodes)
        cls.inners.append(anony)
        c.f.id = name
        e = gen_E_new(c)
      else:
        c_node = util.mk_v_node_w_children(_nodes[1:])
        c = curried_e(c_node)
        e = gen_E_new(c)
    else: # array (w/ initial values)
      w_init_vals = util.exists(lambda n: n.getText() in ['{', '}'], _nodes)
      if w_init_vals:
        what_to_find = '{' # starting point of initial values
      else:
        what_to_find = '[' # starting point of array size
      for i, n in enumerate(_nodes):
        if n.getText() == what_to_find:
          t_node = util.mk_v_node_w_children(_nodes[1:i])
          init_node = util.mk_v_node_w_children(_nodes[i:])
          break
      t = gen_E_id(util.implode_id(t_node))
      init = util.implode_id(init_node)
      e = gen_E_new(t, init)

  # (E... ... (ARGV ...))
  elif _nodes[-1].getText() == C.T.ARG:
    f_node = util.mk_v_node_w_children(_nodes[:-1])
    f = curried_e(f_node)
    a = map(curried_e, _nodes[-1].getChildren())
    e = gen_E_call(f, a)

  # (E... ... '[' (E... ) ']')
  elif _nodes[-1].getText() == ']' and _nodes[-3].getText() == '[':
    idx = curried_e(_nodes[-2])
    le_node = util.mk_v_node_w_children(_nodes[:-3])
    le = curried_e(le_node)
    e = gen_E_idx(le, idx)

  # (... '.' ...)
  elif any(filter(lambda n: n.getText() == '.', _nodes)):
    i = [i for i, n in enumerate(_nodes) if n.getText() == '.'][-1]
    l_node = util.mk_v_node_w_children(_nodes[:i])
    le = curried_e(l_node)
    r_node = util.mk_v_node_w_children(_nodes[i+1:])
    re = curried_e(r_node)
    e = gen_E_dot(le, re)

  # (... '<' ... '>') # e.g., Collection<T>
  elif _nodes[-1].getText() == '>':
    e = gen_E_id(util.implode_id(_node))

  else: raise Exception("unhandled expression", node.toStringTree())

  return e


# parse and generate an expression
@takes(unicode)
@returns(Expression)
def to_expression(e):
  s_stream = antlr3.StringStream(e)
  lexer = Lexer(s_stream)
  t_stream = antlr3.CommonTokenStream(lexer)
  parser = Parser(t_stream)
  try:
    ast = parser.expression()
    return parse_e(ast.tree)
  except antlr3.RecognitionException:
    traceback.print_stack()

