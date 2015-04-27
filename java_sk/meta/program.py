#!/usr/bin/env python

import cStringIO
import logging
import logging.config
import operator as op
import os
import sys

from antlr3.tree import CommonTree as AST

from lib.typecheck import *
import lib.const as C
import lib.visit as v

from .. import util
from ..anno import parse_anno

from . import fields_reset, methods_reset, classes_reset, fields, methods, classes, class_lookup
import statement as st
from field import Field
from method import Method
from clazz import Clazz, parse_class, find_base


class Program(v.BaseNode):

  def __init__(self, ast):
    # reset ids and lists of meta-classes: Field, Method, and Clazz

    fields_reset()
    methods_reset()
    classes_reset()
    self._frozen = False

    # class declarations in this template
    self._classes = [] # [ Clazz... ]

    # primitive classes
    cls_obj = Clazz(pkg=u"java.lang", name=C.J.OBJ)
    cls_obj.sup = None # Object is the root
    self._classes.append(cls_obj)

    annos = []
    pkg = None
    mods = []
    for _ast in ast.getChildren():
      tag = _ast.getText()
      if tag in [C.T.CLS, C.T.ITF, C.T.ENUM]:
        clazz = parse_class(_ast)
        clazz.annos = annos
        if pkg:
          for cls in util.flatten_classes([clazz], "inners"): cls.pkg = pkg
        clazz.mods = mods
        self._classes.append(clazz)

        annos = []
        pkg = None
        mods = []

      elif tag == C.T.ANNO:
        annos.append(parse_anno(_ast))
      elif tag == C.T.PKG:
        p_node = util.mk_v_node_w_children(_ast.getChildren())
        pkg = util.implode_id(p_node)
      else: # modifiers
        mods.append(tag)
    ## parsing done
    ## post manipulations go below

    logging.debug("# class(es): {}".format(len(classes())))
    logging.debug("# method(s): {}".format(len(methods())))
    logging.debug("# field(s): {}".format(len(fields())))

    self.consist()

  # keep snapshots of instances of meta-classes
  def freeze(self):
    self._flds = fields()
    self._mtds = methods()
    self._clss = classes()

  # restore snapshots of instances of meta-classes
  def unfreeze(self):
    fields_reset(self._flds)
    methods_reset(self._mtds)
    classes_reset(self._clss)

  @property
  def classes(self):
    return self._classes

  @classes.setter
  def classes(self, v):
    self._classes = v
    
  def add_classes(self, v):
    self._classes.extend(v)
  
  def __str__(self):
    return '\n'.join(map(str, self._classes))

  def accept(self, visitor):
    visitor.visit(self)
    clss = util.flatten_classes(self._classes, "inners")
    map(op.methodcaller("accept", visitor), clss)

  # to make the template type-consistent
  #   collect all the types in the template
  #   build class hierarchy
  #   discard interfaces without implementers
  #   discard methods that refer to undefined types
  def consist(self):
    clss = util.flatten_classes(self._classes, "inners")

    # collect *all* types in the template
    # including inners as well as what appear at field/method declarations
    # (since we don't care about accessability, just flatten inner classes)
  
    # for easier(?) membership test
    # { cls!r: Clazz(cname, ...), ... }
    decls = { repr(cls): cls for cls in clss }
    def is_defined(tname):
      _tname = util.sanitize_ty(tname)
      for cls_r in decls.keys():
        if decls[cls_r].is_inner:
          if _tname == cls_r: return True
          if _tname in cls_r.split('_'): return True
        else:
          if tname == cls_r: return True
      return False

    def add_decl(tname):
      if is_defined(tname): return
      logging.debug("adding virtual declaration {}".format(tname))
      cls = Clazz(name=tname)
      # to avoid weird subtyping, e.g., int < Object
      if tname in C.primitives: cls.sup = None
      decls[repr(cls)] = cls
      # add declarations in nested generics or arrays
      if util.is_collection(tname):
        map(add_decl, util.of_collection(tname)[1:])
      elif util.is_array(tname):
        add_decl(util.componentType(tname))

    # finding types that occur at field/method declarations
    for cls in clss:
      for fld in cls.flds:
        if not is_defined(fld.typ): add_decl(fld.typ)
      for mtd in cls.mtds:
        for (ty, nm) in mtd.params:
          if not is_defined(ty): add_decl(ty)

    # build class hierarchy: fill Clazz.subs
    for cls in clss:
      if not cls.sup and not cls.itfs: continue
      sups = map(util.sanitize_ty, cls.itfs)
      if cls.sup: sups.append(util.sanitize_ty(cls.sup))
      if not sups: continue
      for sup in clss:
        if sup == cls: continue
        if sup.name in sups or repr(sup) in sups:
          if cls not in sup.subs: sup.subs.append(cls)


  # invoke Clazz.mtds_w_anno for all classes
  @takes("Program", callable)
  @returns(list_of(Method))
  def mtds_w_anno(self, cmp_anno):
    mtdss = map(lambda cls: cls.mtds_w_anno(cmp_anno), self._classes)
    return util.ffilter(util.flatten(mtdss))

  # invoke Clazz.mtds_w_mod for all classes
  @takes("Program", unicode)
  @returns(list_of(Method))
  def mtds_w_mod(self, mod):
    mtdss = map(lambda cls: cls.mtds_w_mod(mod), self._classes)
    return util.ffilter(util.flatten(mtdss))

  # find methods with @Harness
  # if called with a specific name, will returns the exact method
  @takes("Program", optional(str))
  @returns( (list_of(Method), Method) )
  def harness(self, name=None):
    if name:
      h_finder = lambda anno: anno.by_attr({"name": C.A.HARNESS, "f": name})
      mtds = self.mtds_w_anno(h_finder)
      if mtds and len(mtds) == 1: return mtds[0]
      _mtds = self.mtds_w_mod(C.mod.HN)
      mtds = filter(lambda mtd: mtd.name == name, _mtds)
      if mtds and len(mtds) == 1: return mtds[0]
      raise Exception("can't find @Harness or harness", name)

    else:
      h_finder = lambda anno: anno.by_name(C.A.HARNESS)
      mtds = self.mtds_w_anno(h_finder) + self.mtds_w_mod(C.mod.HN)
      return util.rm_dup(mtds)

  # find main()
  @property
  def main(self):
    mtds = []
    # assume *main* is not defined in inner classes
    for cls in self._classes:
      for mtd in cls.mtds:
        if C.mod.ST in mtd.mods and mtd.name == C.J.MAIN:
          mtds.append(mtd)
    n = len(mtds)
    if n > 1:
      raise Exception("multiple main()s", mtds)
    elif 1 == n: return mtds[0]
    else: return None

  # find the class to which main() belongs
  @property
  def main_cls(self):
    main = self.main
    harness = self.harness()
    if main: return main.clazz
    # assume @Harness methods are defined at the same class
    elif harness: return harness[0].clazz
    else: raise Exception("None of main() and @Harness is found")

  # add main() that invokes @Harness methods
  @takes("Program")
  @returns(nothing)
  def add_main(self):
    main_cls = self.main_cls
    if any(main_cls.mtd_by_name(u"main")): return
    params = [ (u"String[]", u"args") ]
    main = Method(clazz=main_cls, mods=C.PBST, name=u"main", params=params)
    def to_call(mtd): return mtd.name + "();"
    body = '\n'.join(map(to_call, self.harness()))
    main.body = st.to_statements(main, body)
    main_cls.mtds.append(main)

  # find class of certain kind, e.g., Activity
  @takes("Program", unicode)
  @returns(list_of(Clazz))
  def find_cls_kind(self, kind):
    cls_kind = class_lookup(kind)
    if cls_kind: pred = lambda cls: cls < cls_kind
    else: pred = lambda cls: kind in cls.name
    return filter(pred, self._classes)


"""
To import lib.*, run as follows:
  pasket $ python -m java_sk.meta.program
"""
if __name__ == "__main__":
  from optparse import OptionParser
  usage = "usage: python -m java_sk.meta.program (input.java | input_folder)+ [option]*"
  parser = OptionParser(usage=usage)
  parser.add_option("--hierarchy",
    action="store_true", dest="hierarchy", default=False,
    help="print inheritance hierarchy")
  parser.add_option("--method",
    action="store_true", dest="method", default=False,
    help="print declared methods in the template")

  (opt, argv) = parser.parse_args()

  if len(argv) < 1:
    parser.error("incorrect number of arguments")

  pwd = os.path.dirname(__file__)
  src_dir = os.path.join(pwd, "..")
  root_dir = os.path.join(src_dir, "..")
  sys.path.append(root_dir)

  ## logging configuration
  logging.config.fileConfig(os.path.join(src_dir, "logging.conf"))
  logging.getLogger().setLevel(logging.DEBUG)

  pgr_files = []
  for arg in argv:
    pgr_files.extend(util.get_files_from_path(arg, "java"))

  ast = util.toAST(pgr_files)
  pgr = Program(ast)

  if opt.hierarchy:

    def toStringTree(cls, depth=0):
      buf = cStringIO.StringIO()
      buf.write("%*s" % (depth, ""))
      if cls.is_class: buf.write("[c] ")
      elif cls.is_itf: buf.write("[i] ")
      elif cls.is_enum: buf.write("[e] ")
      buf.write(repr(cls))
      if cls.itfs: buf.write(" : " + ", ".join(map(str, cls.itfs)))
      buf.write('\n')
      for sub in cls.subs:
        buf.write(toStringTree(sub, depth+4))
      for inner in cls.inners:
        buf.write(toStringTree(inner, depth+2))
      return buf.getvalue()

    pgr.consist()
    bases = util.rm_dup(map(find_base, classes()))
    for cls in bases:
      print toStringTree(cls, 0)

  if opt.method:
    for mtd in methods():
      print mtd.signature

  if not sum([opt.hierarchy, opt.method]):
    print str(pgr)

