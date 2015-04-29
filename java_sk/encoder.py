import cStringIO
import os
import copy as cp
from itertools import chain, ifilter, ifilterfalse
from functools import partial
import re
import operator as op
from string import Template as T
import logging

from lib.typecheck import *
import lib.const as C
from lib.enum import enum

import util
from meta import methods, classes, class_lookup
from meta.program import Program
from meta.clazz import Clazz, find_fld, find_mtds_by_name, find_mtd_by_sig, find_base
from meta.method import Method, sig_match
from meta.field import Field
from meta.statement import Statement
import meta.statement as st
from meta.expression import Expression, typ_of_e
import meta.expression as exp

# constants regarding sketch
C.SK = enum(z=u"bit", self=u"self")

# global constants that should be placed at every sketch file
_const = u''

# among class declarations in the template
# exclude subclasses so that only the base class remains
# (will make a virtual struct representing all the classes in that hierarchy)
@takes(list_of(Clazz))
@returns(list_of(Clazz))
def rm_subs(clss):
  # { cname: Clazz(cname, ...), ... }
  decls = { cls.name: cls for cls in clss }

  # remove subclasses
  for cname in decls.keys():
    if util.is_collection(cname): continue
    cls = class_lookup(cname)
    if not cls.is_class: continue
    for sub in cls.subs:
      if sub.name in decls:
        logging.debug("{} < {}".format(sub.name, cname))
        del decls[sub.name]
    for sup in util.ffilter([cls.sup]):
      if sup in decls and cname in decls:
        logging.debug("{} < {}".format(cname, sup))
        del decls[cname]

  return decls.values()


# convert the given type name into a newer one
_ty = {} # { tname : new_tname }

@takes(dict_of(unicode, unicode))
@returns(nothing)
def add_ty_map(m):
  global _ty
  for key in m: _ty[key] = m[key]


@takes(unicode)
@returns(unicode)
def trans_ty(tname):
  _tname = util.sanitize_ty(tname.strip())
  array_regex = r"([^ \[\]]+)((\[\])+)"
  m = re.match(array_regex, _tname)

  global _ty
  r_ty = _tname
  # to avoid primitive types that Sketch doesn't support
  if _tname == C.J.z: r_ty = C.SK.z
  elif _tname in [C.J.b, C.J.s, C.J.j]: r_ty = C.J.i
  # TODO: parameterize len?
  elif _tname in [C.J.c+"[]"]: r_ty = u"{}[51]".format(C.J.c)
  elif _tname in [C.J.B, C.J.S, C.J.J, C.J.I]: r_ty = C.J.i
  # array bounds
  elif m:
    r_ty = trans_ty(m.group(1)) + \
        "[{}]".format(len(methods())) * len(re.findall(r"\[\]", m.group(2)))
  # use memoized type conversion
  elif _tname in _ty: r_ty = _ty[_tname]
  # convert Java collections into an appropriate struct name
  # Map<K,V> / List<T> / ... -> Map_K_V / List_T / ...
  elif util.is_collection(_tname):
    r_ty = '_'.join(util.of_collection(_tname))
    logging.debug("{} => {}".format(_tname, r_ty))
    _ty[_tname] = r_ty

  return r_ty


# check whether the given type is replaced due to class hierarchy
@takes(unicode)
@returns(bool)
def is_replaced(tname):
  return tname != trans_ty(tname)


# sanitize method name
# e.g., JComboBox(E[]) => JComboBox_JComboBox_E[] => JComboBox_JComboBox_Es
@takes(unicode)
@returns(unicode)
def sanitize_mname(mname):
  return mname.replace("[]",'s')


# convert the given method name into a new one
# considering parameterized types (e.g., collections) and inheritances
_mtds = {} # { cname_mname_... : new_mname }
@takes(unicode, unicode, list_of(unicode))
@returns(unicode)
def trans_mname(cname, mname, arg_typs=[]):
  global _mtds
  r_mtd = mname
  mid = u'_'.join([cname, mname] + arg_typs)
  # use memoized method name conversion
  if mid in _mtds:
    return _mtds[mid]
  # methods of Java collections
  elif util.is_collection(cname):
    _arg_typs = map(trans_ty, arg_typs)
    r_mtd = u'_'.join([mname, trans_ty(cname)] + _arg_typs)
  else:
    if is_replaced(cname):
      tr_name = trans_ty(cname)
      cls = class_lookup(tr_name)
    mtd = find_mtd_by_sig(cname, mname, arg_typs)
    if mtd: r_mtd = unicode(repr(mtd))
    else: r_mtd = '_'.join([mname, util.sanitize_ty(cname)])

  r_mtd = sanitize_mname(r_mtd)
  _mtds[mid] = r_mtd
  return r_mtd


# to avoid duplicate structs for collections
_collections = set([])

# Java collections -> C-style struct (along with basic functions)
@takes(Clazz)
@returns(unicode)
def col_to_struct(cls):
  buf = cStringIO.StringIO()
  cname = cls.name
  sname = trans_ty(cname)
  global _collections
  if sname in _collections:
    logging.debug("collection: {} (duplicated)".format(cname))
    return u''
  else:
    _collections.add(sname)
    logging.debug("collection: " + cname)

  buf.write("struct ${sname} {\n  int idx;\n")

  if C.J.MAP in cname:
    _, k, v = util.of_collection(cname)
    k = trans_ty(k)
    v = trans_ty(v)

    # Map<K,V> -> struct Map_K_V { int idx; K[S] key; V[S] val; }
    buf.write("  ${k}[S] key;\n  ${v}[S] val;\n}\n")

    # Map<K,V>.containsKey -> containsKey_Map_K_V
    buf.write("""
      bit {} (${{sname}} map, ${{k}} k) {{
        int i;
        for (i = 0; map.val[i] != null && i < S; i++) {{
          if (map.key[i] == k) return 1;
        }}
        return 0;
      }}
    """.format(trans_mname(cname, u"containsKey", [k])))

    # Map<K,V>.get -> get_Map_K_V
    buf.write("""
      ${{v}} {} (${{sname}} map, ${{k}} k) {{
        int i;
        for (i = 0; map.val[i] != null && i < S; i++) {{
          if (map.key[i] == k) return map.val[i];
        }}
        return null;
      }}
    """.format(trans_mname(cname, u"get", [k])))

    # Map<K,V>.put -> put_Map_K_V
    buf.write("""
      void {} (${{sname}} map, ${{k}} k, ${{v}} v) {{
        map.key[map.idx] = k;
        map.val[map.idx] = v;
        map.idx = (map.idx + 1) % S;
      }}
    """.format(trans_mname(cname, u"put", [k, v])))

    # Map<K,V>.clear -> clear_Map_K_V
    if util.is_class_name(k): default_k = "null"
    else: default_k = "0"
    buf.write("""
      void {} (${{sname}} map) {{
        map.idx = 0;
        for (int i = 0; i < S; i++) {{
          map.key[i] = {};
          map.val[i] = null;
        }}
      }}
    """.format(trans_mname(cname, u"clear", []), default_k))

  else:
    collection, t = util.of_collection(cname)
    t = trans_ty(t)

    if C.J.QUE in collection: buf.write("  int head;\n")
    # Collection<T> -> struct Collection_T { int idx; T[S] elts; }
    buf.write("  ${t}[S] elts;\n}\n")

    if C.J.STK in collection:
      # Stack<T>.push -> push_Stack_T
      buf.write("""
        ${{t}} {} (${{sname}} stk, ${{t}} elt) {{
          stk.elts[stk.idx] = elt;
          stk.idx = (stk.idx + 1) % S;
          return elt;
        }}
      """.format(trans_mname(cname, u"push", [t])))

      # Stack<T>.pop -> pop_Stack_T
      buf.write("""
        ${{t}} {} (${{sname}} stk) {{
          if (stk.idx == 0) return null;
          stk.idx = stk.idx - 1;
          ${{t}} top = stk.elts[stk.idx];
          stk.elts[stk.idx] = null;
          return top;
        }}
      """.format(trans_mname(cname, u"pop", [])))

    elif C.J.QUE in collection:
      # Queue<T>.add -> add_Queue_T
      buf.write("""
        bit {} (${{sname}} que, ${{t}} elt) {{
          que.elts[que.idx] = elt;
          que.idx = (que.idx + 1) % S;
          return true;
        }}
      """.format(trans_mname(cname, u"add", [t])))

      # Queue<T>.remove -> remove_Queue_T
      buf.write("""
        ${{t}} {} (${{sname}} que) {{
          if (que.head == que.idx) return null;
          ${{t}} top = que.elts[que.head];
          que.elts[que.head] = null;
          que.head = (que.head + 1) % S;
          return top;
        }}
      """.format(trans_mname(cname, u"remove", [])))

      # Queue<T>.isEmpty -> isEmpty_Queue_T
      buf.write("""
        bit {} (${{sname}} que) {{
          return que.head == que.idx;
        }}
      """.format(trans_mname(cname, u"isEmpty", [])))

    elif C.J.LST in collection:
      # List<T>.add -> add_List_T
      buf.write("""
        bit {} (${{sname}} lst, ${{t}} elt) {{
          lst.elts[lst.idx] = elt;
          lst.idx = (lst.idx + 1) % S;
          return true;
        }}
      """.format(trans_mname(cname, u"add", [t])))

      # List<T>.remove(T) -> remove_List_T_T
      buf.write("""
        bit {} (${{sname}} lst, ${{t}} elt) {{
          int i;
          for (i = 0; lst.elts[i] != null && i < S; i++) {{
            if (lst.elts[i] == elt) {{
              lst.elts[i] = null;
              return true;
            }}
          }}
          return false;
        }}
      """.format(trans_mname(cname, u"remove", [t])))

      # List<T>.remove(int) -> remove_List_T_int
      buf.write("""
        ${{t}} {} (${{sname}} lst, int index) {{
          ${{t}} res = null;
          if (0 <= index && index < lst.idx) {{
            res = lst.elts[index];
            lst.elts[index] = null;
            int i;
            for (i = index; lst.elts[i] != null && i < lst.idx; i++) {{
              lst.elts[i] = lst.elts[i+1];
            }}
            lst.idx = (lst.idx - 1) % S;
          }}
          return res;
        }}
      """.format(trans_mname(cname, u"remove", [C.J.i])))

      # List<T>.get -> get_List_T
      buf.write("""
        ${{t}} {} (${{sname}} lst, int index) {{
          ${{t}} res = null;
          if (0 <= index && index < lst.idx) {{
            res = lst.elts[index];
          }}
          return res;
        }}
      """.format(trans_mname(cname, u"get", [C.J.i])))

      # List<T>.isEmpty -> isEmpty_List_T
      buf.write("""
        bit {} (${{sname}} lst) {{
          return lst.idx == 0;
        }}
      """.format(trans_mname(cname, u"isEmpty", [])))

  return T(buf.getvalue()).safe_substitute(locals())


_flds = {} # { cname.fname : new_fname }
_s_flds = {} # { cname.fname : accessor }

# from the given base class,
# generate a virtual struct that encompasses all the class in the hierarchy
@takes(Clazz)
@returns(Clazz)
def to_v_struct(cls):
  cls_v = Clazz(name=cls.name)

  fld_ty = Field(clazz=cls_v, typ=C.J.i, name=u"__cid")
  cls_v.flds.append(fld_ty)

  global _ty, _flds, _s_flds
  @takes(dict_of(unicode, Field), Clazz)
  @returns(nothing)
  def per_cls(sup_flds, cls):

    # keep mappings from original subclasses to the representative
    # so that subclasses can refer to the representative
    # e.g., for C < B < A, { B : A, C : A }
    cname = util.sanitize_ty(cls.name)
    if cname != cls_v.name: # exclude the root of this family
      logging.debug("{} => {}".format(cname, cls_v.name))
      _ty[cname] = cls_v.name
      if cls.is_inner: # to handle inner class w/ outer class name
        logging.debug("{} => {}".format(repr(cls), cls_v.name))
        _ty[unicode(repr(cls))] = cls_v.name

    # if this class implements an interface which has constants,
    # then copy those constants
    for itf in cls.itfs:
      cls_i = class_lookup(itf)
      if not cls_i or not cls_i.flds: continue
      for fld in cls_i.flds:
        sup_flds[fld.name] = fld

    # also, keep mappings from original member fields to newer ones
    # so that usage of old fields can be replaced accordingly
    # e.g., for A.f1 and B.f2, { A.f1 : f1_A, B.f1 : f1_A, B.f2 : f2_B }
    for sup_fld in sup_flds.keys():
      fld = sup_flds[sup_fld]
      fname = unicode(repr(fld))
      fid = '.'.join([cname, sup_fld])
      logging.debug("{} => {}".format(fid, fname))
      if fld.is_static: _s_flds[fid] = fname
      else: _flds[fid] = fname # { ..., B.f1 : f1_A }

    cur_flds = cp.deepcopy(sup_flds) # { f1 : f1_A }
    @takes(Field)
    @returns(nothing)
    def cp_fld(fld):
      cur_flds[fld.name] = fld # { ..., f2 : f2_B }

      fname = unicode(repr(fld))
      fld_v = cp.deepcopy(fld)
      fld_v.clazz = cls_v
      fld_v.name = fname
      cls_v.flds.append(fld_v)

      def upd_flds(cname):
        fid = '.'.join([cname, fld.name])
        # if A.f1 exists and B redefines f1, then B.f1 : f1_A
        # except for enum, which can (re)define its own fields
        # e.g., SwingConstands.LEADING vs. GroupLayout.Alignment.LEADING
        if not cls.is_enum and (fid in _s_flds or fid in _flds): return
        logging.debug("{} => {}".format(fid, fname))
        if fld.is_static: _s_flds[fid] = fname
        else: _flds[fid] = fname # { ..., B.f2 : f2_B }

      upd_flds(cname)

    map(cp_fld, cls.flds)

    map(partial(per_cls, cur_flds), cls.subs)

  per_cls({}, cls)

  return cls_v


@takes(Field)
@returns(str)
def trans_fld(fld):
  buf = cStringIO.StringIO()
  buf.write(' '.join([trans_ty(fld.typ), fld.name]))
  if fld.is_static and fld.init and \
      not fld.init.has_call and not fld.init.has_str and not fld.is_aliasing:
    buf.write(" = " + trans_e(None, fld.init))
  buf.write(';')
  return buf.getvalue()


# Java class (along with subclasses) -> C-style struct
@takes(Clazz)
@returns(str)
def to_struct(cls):

  # make mappings from static fields to corresponding accessors
  def gen_s_flds_accessors(cls):
    s_flds = filter(op.attrgetter("is_static"), cls.flds)
    global _s_flds
    for fld in ifilterfalse(op.attrgetter("is_private"), s_flds):
      cname = fld.clazz.name
      fid = '.'.join([cname, fld.name])
      fname = unicode(repr(fld))
      logging.debug("{} => {}".format(fid, fname))
      _s_flds[fid] = fname

  cname = util.sanitize_ty(cls.name)
  global _ty
  # if this is an interface, merge this into another family of classes
  # as long as classes that implement this interface are in the same family
  if cls.is_itf:
    # interface may have static constants
    gen_s_flds_accessors(cls)
    subss = util.flatten_classes(cls.subs, "subs")
    bases = util.rm_dup(map(lambda sub: find_base(sub), subss))
    # filter out interfaces that extend other interfaces, e.g., Action
    base_clss, _ = util.partition(op.attrgetter("is_class"), bases)
    if not base_clss:
      logging.debug("no implementer of {}".format(cname))
    elif len(base_clss) > 1:
      logging.debug("ambiguous inheritance of {}: {}".format(cname, base_clss))
    else: # len(base_clss) == 1
      base = base_clss[0]
      base_name = base.name
      logging.debug("{} => {}".format(cname, base_name))
      _ty[cname] = base_name
      if cls.is_inner: # to handle inner interface w/ outer class name
        logging.debug("{} => {}".format(repr(cls), base_name))
        _ty[unicode(repr(cls))] = base_name

    return ''

  # if this is the base class having subclasses,
  # make a virtual struct first
  if cls.subs:
    cls = to_v_struct(cls)
    cname = cls.name

  # cls can be modified above, thus generate static fields accessors here
  gen_s_flds_accessors(cls)

  # for unique class numbering, add an identity mapping
  if cname not in _ty: _ty[cname] = cname

  buf = cStringIO.StringIO()
  buf.write("struct " + cname + " {\n  int hash;\n")

  # to avoid static fields, which will be bound to a class-representing package
  _, i_flds = util.partition(op.attrgetter("is_static"), cls.flds)
  buf.write('\n'.join(map(trans_fld, i_flds)))
  if len(i_flds) > 0: buf.write('\n')
  buf.write("}\n")

  return buf.getvalue()


# convert the given field name into a newer one
# only if the field belongs to a virtual representative struct
@takes(unicode, unicode, optional(bool))
@returns(unicode)
def trans_fname(cname, fname, is_static=False):
  global _flds, _s_flds
  r_fld = fname
  fid = '.'.join([cname, fname])
  if is_static:
    if fid in _s_flds: r_fld = _s_flds[fid]
  else:
    if fid in _flds: r_fld = _flds[fid]

  return r_fld


# collect method/field declarations in the given class and its inner classes
@takes(Clazz)
@returns(list_of((Method, Field)))
def collect_decls(cls, attr):
  clss = util.flatten_classes([cls], "inners")
  declss = map(op.attrgetter(attr), clss)
  return util.flatten(declss)


# sanitize id by removing package name
# e.g., javax.swing.SwingUtilities.invokeLater -> SwingUtilities.invokeLater
@takes(unicode)
@returns(unicode)
def sanitize_id(dot_id):
  pkg, cls, mtd = util.explode_mname(dot_id)
  if cls and util.is_class_name(cls) and class_lookup(cls):
    clazz = class_lookup(cls)
    if clazz.pkg and pkg and clazz.pkg != pkg: # to avoid u'' != None
      raise Exception("wrong package", pkg, clazz.pkg)
    return '.'.join([cls, mtd])

  return dot_id


@takes(optional(Method), Expression)
@returns(str)
def trans_e(mtd, e):
  curried = partial(trans_e, mtd)
  buf = cStringIO.StringIO()

  if e.kind == C.E.ID:
    if hasattr(e, "ty"): buf.write(trans_ty(e.ty) + ' ')
    fld = None
    if mtd and e.id not in mtd.param_vars:
      fld = find_fld(mtd.clazz.name, e.id)
    if fld: # fname -> self.new_fname (unless the field is static)
      new_fname = trans_fname(fld.clazz.name, e.id, fld.is_static)
      if fld.is_static:
        # access to the static field inside the same class
        if fld.clazz.name == mtd.clazz.name: buf.write(e.id)
        # o.w., e.g., static constant in an interface, call the accessor
        else: buf.write(new_fname + "()")
      else: buf.write('.'.join([C.SK.self, new_fname]))
    elif e.id in [C.J.THIS, C.J.SUP]: buf.write(C.SK.self)
    elif util.is_str(e.id): # constant string, such as "Hello, World"
      str_init = trans_mname(C.J.STR, C.J.STR, [u"char[]", C.J.i, C.J.i])
      s_hash = hash(e.id) % 256 # hash string value itself
      buf.write("{}(new Object(hash={}), {}, 0, {})".format(str_init, s_hash, e.id, len(e.id)))
    else: buf.write(e.id)

  elif e.kind == C.E.UOP:
    buf.write(' '.join([e.op, curried(e.e)]))

  elif e.kind == C.E.BOP:
    buf.write(' '.join([curried(e.le), e.op, curried(e.re)]))

  elif e.kind == C.E.DOT:
    # with package names, e.g., javax.swing.SwingUtilities
    if util.is_class_name(e.re.id) and class_lookup(e.re.id):
      buf.write(curried(e.re))
    elif e.re.id == C.J.THIS: # ClassName.this
      buf.write(C.SK.self)
    else:
      rcv_ty = typ_of_e(mtd, e.le)
      fld = find_fld(rcv_ty, e.re.id)
      new_fname = trans_fname(rcv_ty, e.re.id, fld.is_static)
      if fld.is_static:
        # access to the static field inside the same class
        if mtd and rcv_ty == mtd.clazz.name: buf.write(e.re.id)
        # o.w., e.g., static constant in an interface, call the accessor
        else: buf.write(new_fname + "()")
      else: buf.write('.'.join([curried(e.le), new_fname]))

  elif e.kind == C.E.IDX:
    buf.write(curried(e.e) + '[' + curried(e.idx) + ']')

  elif e.kind == C.E.NEW:
    if e.e.kind == C.E.CALL:
      ty = typ_of_e(mtd, e.e.f)
      cls = class_lookup(ty)
      if cls and cls.has_init:
        arg_typs = map(partial(typ_of_e, mtd), e.e.a)
        mname = trans_mname(cls.name, cls.name, arg_typs)
        obj = "alloc@log({})".format(cls.id)
        args = [obj] + map(unicode, map(curried, e.e.a))
        buf.write("{}({})".format(mname, ", ".join(args)))
      else: # collection or Object
        buf.write(C.J.NEW + ' ' + trans_ty(ty) + "()")
    else: # o.w., array initialization, e.g., new int[] { ... }
      buf.write(str(e.init))

  elif e.kind == C.E.CALL:
    arg_typs = map(partial(typ_of_e, mtd), e.a)
    if e.f.kind == C.E.DOT: # rcv.mid
      rcv_ty = typ_of_e(mtd, e.f.le)
      mname = e.f.re.id
      mtd_callee = find_mtd_by_sig(rcv_ty, mname, arg_typs)
      if mtd_callee and mtd_callee.is_static: rcv = None
      else: rcv = curried(e.f.le)
      mid = trans_mname(rcv_ty, mname, arg_typs)
    else: # mid
      mname = e.f.id
      # pre-defined meta information
      if mname in C.typ_arrays:
        mid = mname
        rcv = None
      elif mname == C.J.SUP and mtd.is_init: # super(...) inside <init>
        sup = class_lookup(mtd.clazz.sup)
        mid = trans_mname(sup.name, sup.name, arg_typs)
        rcv = C.SK.self
      else: # member methods
        mtd_callee = find_mtd_by_sig(mtd.clazz.name, mname, arg_typs)
        if mtd_callee and mtd_callee.is_static: rcv = None
        else: rcv = C.SK.self
        mid = trans_mname(mtd.clazz.name, mname, arg_typs)

    args = util.rm_none([rcv] + map(curried, e.a))
    buf.write(mid + '(' + ", ".join(args) + ')')

  elif e.kind == C.E.CAST:
    # since a family of classes is merged, simply ignore the casting
    buf.write(curried(e.e))

  else: buf.write(str(e))
  return buf.getvalue()


@takes(Method, Statement)
@returns(str)
def trans_s(mtd, s):
  curried_e = partial(trans_e, mtd)
  curried_s = partial(trans_s, mtd)
  buf = cStringIO.StringIO()

  if s.kind == C.S.IF:
    e = curried_e(s.e)
    t = '\n'.join(map(curried_s, s.t))
    f = '\n'.join(map(curried_s, s.f))
    buf.write("if (" + e + ") {\n" + t + "\n}")
    if f: buf.write("\nelse {\n" + f + "\n}")

  elif s.kind == C.S.WHILE:
    e = curried_e(s.e)
    b = '\n'.join(map(curried_s, s.b))
    buf.write("while (" + e + ") {\n" + b + "\n}")

  elif s.kind == C.S.REPEAT:
    e = curried_e(s.e)
    b = '\n'.join(map(curried_s, s.b))
    if e == "??": buf.write("minrepeat {\n" + b + "\n}")
    else: buf.write("repeat (" + e + ") {\n" + b + "\n}")

  elif s.kind == C.S.FOR:
    # assume "for" is used for List<T> and LinkedList<T> only
    col = mtd.vars[s.init.id]
    if not util.is_collection(col) or \
        util.of_collection(col)[0] not in [C.J.LST, C.J.LNK]:
      raise Exception("not iterable type", col)

    # if this is about observers, let sketch choose iteration direction
    is_obs = hasattr(class_lookup(util.of_collection(col)[1]), "obs")
    s_init = curried_e(s.init)

    if is_obs: init = "{{| 0 | {}.idx - 1 |}}".format(s_init)
    else: init = '0'
    buf.write("  int idx = {};".format(init))

    s_i_typ = trans_ty(s.i.ty)
    buf.write("""
      while (0 <= idx && idx < S && {s_init}.elts[idx] != null) {{
        {s_i_typ} {s.i.id} = {s_init}.elts[idx];
    """.format(**locals()))

    buf.write('\n'.join(map(curried_s, s.b)))

    if is_obs: upd = "{| idx (+ | -) 1 |}"
    else: upd = "idx + 1"
    buf.write("""
        idx = {};
      }}
    """.format(upd))

  elif s.kind == C.S.TRY:
    # NOTE: no idea how to handle catch blocks
    # at this point, just walk through try/finally blocks
    buf.write('\n'.join(map(curried_s, s.b + s.fs)))

  else: buf.write(s.__str__(curried_e))
  return buf.getvalue()


# Java member method -> C-style function
@takes(Method)
@returns(str)
def to_func(mtd):
  buf = cStringIO.StringIO()
  if C.mod.GN in mtd.mods: buf.write(C.mod.GN + ' ')
  elif C.mod.HN in mtd.mods: buf.write(C.mod.HN + ' ')
  ret_ty = trans_ty(mtd.typ)
  cname = unicode(repr(mtd.clazz))
  mname = mtd.name
  arg_typs = mtd.param_typs
  buf.write(ret_ty + ' ' + trans_mname(cname, mname, arg_typs) + '(')

  @takes(tuple_of(unicode))
  @returns(unicode)
  def trans_param( (ty, nm) ):
    return ' '.join([trans_ty(ty), nm])

  # for instance methods, add "this" pointer into parameters
  if mtd.is_static:
    params = mtd.params[:]
  else:
    self_ty = trans_ty(unicode(repr(mtd.clazz)))
    params = [ (self_ty, C.SK.self) ] + mtd.params[:]

  if len(params) > 0:
    buf.write(", ".join(map(trans_param, params)))
  buf.write(") {\n")

  clss = util.flatten_classes([mtd.clazz], "subs")
  mid = unicode(repr(mtd))
  m_ent = mid + "_ent()"
  m_ext = mid + "_ext()"

  is_void = C.J.v == mtd.typ
  if mtd.body:
    buf.write('\n'.join(map(partial(trans_s, mtd), mtd.body)))

  if mtd.is_init:
    buf.write("\nreturn {};".format(C.SK.self))

  buf.write("\n}\n")
  return buf.getvalue()


# generate type.sk
@takes(str, list_of(Clazz))
@returns(nothing)
def gen_type_sk(sk_dir, bases):
  buf = cStringIO.StringIO()
  buf.write("package type;\n")
  buf.write(_const)

  cols, decls = util.partition(lambda c: util.is_collection(c.name), bases)
  decls = filter(lambda c: not util.is_array(c.name), decls)
  itfs, clss = util.partition(op.attrgetter("is_itf"), decls)
  logging.debug("# interface(s): {}".format(len(itfs)))
  logging.debug("# class(es): {}".format(len(clss)))
  # convert interfaces first, then usual classes
  buf.write('\n'.join(util.ffilter(map(to_struct, itfs))))
  buf.write('\n'.join(util.ffilter(map(to_struct, clss))))

  # convert collections at last
  logging.debug("# collection(s): {}".format(len(cols)))
  buf.write('\n'.join(map(col_to_struct, cols)))

  # argument number of methods
  arg_num = map(lambda mtd: len(mtd.params), methods())
  buf.write("""
    #define _{0} {{ {1} }}
    int {0}(int id) {{
      return _{0}[id];
    }}
  """.format(C.typ.argNum, ", ".join(map(str, arg_num))))

  # argument types of methods
  def get_args_typ(mtd):
    def get_arg_typ(param): return str(class_lookup(param[0]).id)
    return '{' + ", ".join(map(get_arg_typ, mtd.params)) + '}'
  args_typ = map(get_args_typ, methods())
  buf.write("""
    #define _{0} {{ {1} }}
    int {0}(int id, int idx) {{
      return _{0}[id][idx];
    }}
  """.format(C.typ.argType, ", ".join(args_typ)))

  # return type of methods
  def get_ret_typ(mtd):
    cls = class_lookup(mtd.typ)
    if cls: return cls.id
    else: return -1
  ret_typ = map(get_ret_typ, methods())
  buf.write("""
    #define _{0} {{ {1} }}
    int {0}(int id) {{
      return _{0}[id];
    }}
  """.format(C.typ.retType, ", ".join(map(str, ret_typ))))

  # belonging class of methods
  belongs = map(lambda mtd: mtd.clazz.id, methods())
  buf.write("""
    #define _{0} {{ {1} }}
    int {0}(int id) {{
      return _{0}[id];
    }}
  """.format(C.typ.belongsTo, ", ".join(map(str, belongs))))

  subcls = \
      map(lambda cls_i: '{' + ", ".join( \
          map(lambda cls_j: str(cls_i <= cls_j).lower(), classes()) \
      ) + '}', classes())
  buf.write("""
    #define _{0} {{ {1} }}
    bit {0}(int i, int j) {{
      return _{0}[i][j];
    }}
  """.format(C.typ.subcls, ", ".join(subcls)))

  ## sub type relations
  #subcls = []
  #for cls_i in classes():
  #  row = []
  #  for cls_j in classes():
  #    row.append(int(cls_i <= cls_j))
  #  subcls.append(row)

  ## sub type relations in yale format 
  #_, IA, JA = util.yale_format(subcls)
  #li, lj = len(IA), len(JA)
  #si = ", ".join(map(str, IA))
  #sj = ", ".join(map(str, JA))
  #buf.write("""
  #  #define _iA {{ {si} }}
  #  #define _jA {{ {sj} }}
  #  int iA(int i) {{
  #    return _iA[i];
  #  }}
  #  int jA(int j) {{
  #    return _jA[j];
  #  }}
  #  bit subcls(int i, int j) {{
  #    int col_i = iA(i);
  #    int col_j = iA(i+1);
  #    for (int col = col_i; col < col_j; col++) {{
  #      if (j == jA(col)) return true;
  #    }}
  #    return false;
  #  }}
  #""".format(**locals()))

  with open(os.path.join(sk_dir, "type.sk"), 'w') as f:
    f.write(buf.getvalue())
    logging.info("encoding " + f.name)
  buf.close()


# generate cls.sk
@takes(str, Clazz)
@returns(optional(unicode))
def gen_cls_sk(sk_dir, cls):
  mtds = collect_decls(cls, "mtds")
  flds = collect_decls(cls, "flds")
  s_flds = filter(op.attrgetter("is_static"), flds)
  if cls.is_class:
    if not mtds and not s_flds: return None
  else: # cls.is_itf or cls.is_enum
    if not s_flds: return None

  cname = util.sanitize_ty(cls.name)

  buf = cStringIO.StringIO()
  buf.write("package {};\n".format(cname))
  buf.write(_const)

  # static fields
  buf.write('\n'.join(map(trans_fld, s_flds)))
  if len(s_flds) > 0: buf.write('\n')

  # migrating static fields' initialization to <clinit>
  for fld in ifilter(op.attrgetter("init"), s_flds):
    if not fld.init.has_call and not fld.init.has_str and not fld.is_aliasing: continue
    # retrieve (or declare) <clinit>
    clinit = fld.clazz.get_or_declare_clinit()
    if clinit not in mtds: mtds.append(clinit)
    # add assignment
    assign = st.gen_S_assign(exp.gen_E_id(fld.name), fld.init)
    clinit.body.append(assign)

  # accessors for static fields
  for fld in ifilterfalse(op.attrgetter("is_private"), s_flds):
    fname = fld.name
    accessor = trans_fname(fld.clazz.name, fname, True)
    buf.write("""
      {0} {1}() {{ return {2}; }}
    """.format(trans_ty(fld.typ), accessor, fname))

  # methods
  clinits, mtds = util.partition(lambda m: m.is_clinit, mtds)
  inits, mtds = util.partition(lambda m: m.is_init, mtds)
  # <init>/<clinit> should be dumped out in any case
  buf.write('\n'.join(map(to_func, clinits)))
  buf.write('\n'.join(map(to_func, inits)))
  for mtd in mtds:
    # interface won't have method bodies
    if mtd.clazz.is_itf: continue
    buf.write(to_func(mtd) + os.linesep)

  cls_sk = cname + ".sk"
  with open(os.path.join(sk_dir, cls_sk), 'w') as f:
    f.write(buf.getvalue())
    logging.info("encoding " + f.name)
    return cls_sk


# generate log.sk
@takes(str, Program)
@returns(nothing)
def gen_log_sk(sk_dir, pgr):
  buf = cStringIO.StringIO()
  buf.write("package log;\n")
  buf.write(_const)

  buf.write("""
    // distinct hash values for runtime objects
    int obj_cnt = 0;
    int nonce () {
      return obj_cnt++;
    }
  """)

  # factory of Object
  buf.write("""
    // factory of Object
    Object alloc(int ty) {{
      Object {0} = new Object(hash=nonce(), __cid=ty);
      return {0};
    }}
  """.format(C.SK.self))

  global _ty;
  _clss = []
  for ty in _ty.keys():
    if util.is_collection(ty): continue
    if util.is_array(ty): continue
    cls = class_lookup(ty)
    if not cls: continue # to avoid None definition
    # inner class may appear twice: w/ and w/o outer class name
    if cls not in _clss: _clss.append(cls)

  buf.write("\n// distinct class IDs\n")
  for cls in _clss:
    buf.write("int {cls!r} () {{ return {cls.id}; }}\n".format(**locals()))

  buf.write("\n// distinct method IDs\n")
  for cls in pgr.classes:
    mtds = collect_decls(cls, "mtds")
    if not mtds: continue

    for mtd in mtds:
      mname = sanitize_mname(unicode(repr(mtd)))
      buf.write("""
        int {mname}_ent () {{ return  {mtd.id}; }}
        int {mname}_ext () {{ return -{mtd.id}; }}
      """.format(**locals()))

  with open(os.path.join(sk_dir, "log.sk"), 'w') as f:
    f.write(buf.getvalue())
    logging.info("encoding " + f.name)
  buf.close()


# reset global variables
@takes(nothing)
@returns(nothing)
def reset():
  global _ty, _mtds, _flds, _s_flds
  global _collections
  _ty = {}
  _mtds = {}
  _flds = {}
  _s_flds = {}
  _collections = set([])


# translate the high-level program into low-level sketches
# using information at the samples
@takes(Program, str)
@returns(nothing)
def to_sk(pgr, sk_dir):
  # clean up result directory
  if os.path.isdir(sk_dir): util.clean_dir(sk_dir)
  else: os.makedirs(sk_dir)

  # reset global variables so that we can run this encoding phase per demo
  reset()

  # update global constants
  # TODO: conservative analysis of possible length of collections
  # TODO: counting .add() calls or something?
  magic_S = 5

  global _const
  _const = u"""
    int S = {}; // length of arrays for Java collections
  """.format(magic_S)

  # type.sk
  logging.info("building class hierarchy")
  pgr.consist()
  # merge all classes and interfaces, except for primitive types
  clss, _ = util.partition(lambda c: util.is_class_name(c.name), classes())
  bases = rm_subs(clss)
  gen_type_sk(sk_dir, bases)

  # cls.sk
  cls_sks = []
  for cls in pgr.classes:
    # skip the collections, which will be encoded at type.sk
    if repr(cls).split('_')[0] in C.collections: continue
    cls_sk = gen_cls_sk(sk_dir, cls)
    if cls_sk: cls_sks.append(cls_sk)

  # log.sk
  gen_log_sk(sk_dir, pgr)

  # main.sk that imports all the other sketch files
  buf = cStringIO.StringIO()

  # --bnd-unroll-amnt: the unroll amount for loops
  unroll_amnt = None # use a default value if not set
  unroll_amnt = magic_S # TODO: other criteria?
  if unroll_amnt:
    buf.write("pragma options \"--bnd-unroll-amnt {}\";\n".format(unroll_amnt))

  # --bnd-inline-amnt: bounds inlining to n levels of recursion
  inline_amnt = None # use a default value if not set
  # setting it 1 means there is no recursion
  if inline_amnt:
    buf.write("pragma options \"--bnd-inline-amnt {}\";\n".format(inline_amnt))
    buf.write("pragma options \"--bnd-bound-mode CALLSITE\";\n")

  sks = ["log.sk", "type.sk"] + cls_sks
  for sk in sks:
    buf.write("include \"{}\";\n".format(sk))

  # TODO: make harness (if not exists)

  with open(os.path.join(sk_dir, "main.sk"), 'w') as f:
    f.write(buf.getvalue())
    logging.info("encoding " + f.name)
  buf.close()

