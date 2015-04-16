import re
import copy as cp
import cStringIO
from itertools import ifilter, ifilterfalse
import logging
import operator as op

from antlr3.tree import CommonTree as AST

from lib.typecheck import *
import lib.const as C
import lib.visit as v

from .. import util
from ..anno import parse_anno

from . import class_nonce, register_class, class_lookup
import expression as exp
import statement as st
import field
import method

class Clazz(v.BaseNode):

  def __init__(self, **kwargs):
    self._id = class_nonce()

    # annotation
    self._annos = kwargs.get("annos", []) # list_of(Anno)
    # package
    self._pkg = kwargs.get("pkg", None)
    # modifiers
    self._mods = kwargs.get("mods", []) # list_of(unicode)
    # class, interface, or enum
    self._kind = kwargs.get("kind", C.T.CLS)
    # identifier
    self._name = kwargs.get("name", None)
    # superclass
    default_sup = None if self._kind == C.T.ITF else C.J.OBJ
    self._sup = kwargs.get("sup", default_sup)
    # to hold class hierarchy info:
    #   subclasses that extend this class
    #   classes that implement this interface
    self._subs = kwargs.get("subs", []) # list_of(Clazz)
    # implementing interfaces
    self._itfs = kwargs.get("itfs", []) # list_of(unicode)
    # fields
    self._flds = kwargs.get("flds", []) # list_of(Field)
    # methods
    self._mtds = kwargs.get("mtds", []) # list_of(Method)
    # inner classes
    self._inners = kwargs.get("inners", []) # list_of(Clazz)
    # outer class
    self._outer = kwargs.get("outer", None)

    register_class(self)

  @property
  def id(self):
    return self._id

  @property
  def annos(self):
    return self._annos

  @annos.setter
  def annos(self, v):
    self._annos = v

  @property
  def pkg(self):
    return self._pkg

  @pkg.setter
  def pkg(self, v):
    self._pkg = v

  @property
  def mods(self):
    return self._mods

  @mods.setter
  def mods(self, v):
    self._mods = v

  @property
  def is_abstract(self):
    return C.mod.AB in self._mods

  @property
  def kind(self):
    return self._kind

  @property
  def is_class(self):
    return self._kind == C.T.CLS

  @property
  def is_itf(self):
    return self._kind == C.T.ITF

  @property
  def is_enum(self):
    return self._kind == C.T.ENUM

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, v):
    self._name = v

  @property
  def sup(self):
    return self._sup

  @sup.setter
  def sup(self, v):
    self._sup = v

  @property
  def subs(self):
    return self._subs

  @subs.setter
  def subs(self, v):
    self._subs = v

  @property
  def itfs(self):
    return self._itfs

  @itfs.setter
  def itfs(self, v):
    self_.itfs = v

  @property
  def sups(self):
    return util.ffilter([self._sup] + self._itfs)

  @property
  def flds(self):
    return self._flds

  @property
  def fldS(self):
    flds = []
    if self._sup: flds.extend(class_lookup(self._sup).fldS)
    flds.extend(self._flds)
    return flds

  @property
  def mutable_flds(self):
    _, flds = util.partition(op.attrgetter("is_final"), self.flds)
    return flds

  @property
  def mutable_fldS(self):
    _, flds = util.partition(op.attrgetter("is_final"), self.fldS)
    return flds

  @flds.setter
  def flds(self, v):
    self._flds = v
  
  def add_fld(self, fld):
    if fld in self._flds: return False
    else:
      self._flds.append(fld)
      return True
    
  def add_flds(self, v):
    self._flds.extend(v)

  @property
  def mtds(self):
    return self._mtds

  @mtds.setter
  def mtds(self, v):
    self._mtds = v
  
  def add_mtd(self, mtd):
    if mtd in self._mtds: return False
    else:
      self._mtds.append(mtd)
      return True

  def add_mtds(self, v):
    self._mtds.extend(v)

  @property
  def param_typs(self):
    params = map(op.attrgetter("param_typs"), self._mtds)
    return util.rm_dup(util.flatten(params))

  @property
  def inners(self):
    return self._inners

  @inners.setter
  def inners(self, v):
    self._inners = v

  @property
  def outer(self):
    return self._outer

  @outer.setter
  def outer(self, v):
    self._outer = v

  @property
  def is_inner(self):
    return self._outer != None

  @property
  def is_anony(self):
    return None != re.match(r"\S+\$\d+", self._name)

  @property
  def JVM_notation(self):
    cname = self._name
    if self._outer: cname = u'$'.join([self._outer.name, self._name])
    full_name = u'.'.join(util.ffilter([self._pkg, cname]))
    return util.toJVM(full_name)

  def __repr__(self):
    cname = self._name
    if self._outer: cname = u'.'.join([self._outer.name, self._name])
    return util.sanitize_ty(cname)

  def __str__(self, s_printer=None):
    buf = cStringIO.StringIO()
    if self._mods: buf.write(' '.join(self._mods) + ' ')
    buf.write(self._kind + ' ' + self._name)
    if self._sup and self._sup != C.J.OBJ:
      buf.write(' ' + C.T.EXT + ' ' + self._sup)
    if self._itfs:
      buf.write(' ' + C.T.IMP + ' ' + ", ".join(self._itfs))
    buf.write(" {\n")

    if self._kind == C.T.ENUM:
      enum_constants = map(op.attrgetter("name"), self._flds)
      buf.write(",\n".join(map(str, enum_constants)))
    else:
      buf.write('\n'.join(map(str, self._flds)) + '\n')

    m_printer = str
    if s_printer: m_printer = lambda mtd: mtd.__str__(partial(s_printer, mtd))
    clinit, mtds = util.partition(op.attrgetter("is_clinit"), self._mtds)
    if self._kind != C.T.ENUM:
      buf.write('\n'.join(map(m_printer, mtds)) + '\n')

    buf.write('\n'.join(map(str, self._inners)))
    buf.write("\n}\n")
    return buf.getvalue()

  def __eq__(self, other):
    # reflective: c == c
    return repr(self) == repr(other)

  def __lt__(self, other):
    # topmost: c < Object
    if other.name in C.J.OBJ: return True 
    # pre-defined, e.g., primitives
    if self._name in C.primitives and other.name in C.primitives:
      s_id = C.primitives.index(self._name)
      o_id = C.primitives.index(other.name)
      if s_id < o_id: return True

    # superclass: c (extends | implements) d
    if self._sup and self._sup == other.name: return True
    if other.name in self._itfs: return True

    # transitive: c < x and x <= d
    def check_sup(sname):
      sup = class_lookup(sname)
      return sup and sup <= other
    return util.exists(check_sup, util.ffilter([self._sup] + self._itfs))

  def __le__(self, other):
    return self == other or self < other

  def subtype(self, other):
    return self <= other

  def accept(self, visitor):
    visitor.visit(self)
    f = op.methodcaller("accept", visitor)
    map(f, self._flds)
    map(f, self._mtds)

  # gather methods that have the given annotation
  @takes("Clazz", callable)
  @returns(list_of("Method"))
  def mtds_w_anno(self, cmp_anno):
    def anno_filter(mtd):
      return util.exists(cmp_anno, mtd.annos)
    return filter(anno_filter, self._mtds)

  @takes("Clazz", callable, optional(callable), optional(anything))
  def in_hierarchy(self, pred, calc=None, default=None):
    if pred(self):
      if calc: return calc(self)
      else: return self

    if self._sup:
      sup = class_lookup(self._sup)
      if sup: return sup.in_hierarchy(pred, calc, default)

    return default

  # find the field by name
  @takes("Clazz", unicode)
  @returns(optional("Field"))
  def fld_by_name(self, fname):
    def match(fld): return fld.name == fname
    def finder(cls): return util.exists(match, cls.flds)
    def getter(cls): return util.find(match, cls.flds)
    return self.in_hierarchy(finder, getter)

  # find the field by type
  @takes("Clazz", unicode)
  @returns(optional("Field"))
  def fld_by_typ(self, tname):
    def match(fld): return fld.typ == tname
    def finder(cls): return util.exists(match, cls.flds)
    def getter(cls): return util.find(match, cls.flds)
    return self.in_hierarchy(finder, getter)

  # find the method by name
  @takes("Clazz", unicode)
  @returns(list_of("Method"))
  def mtd_by_name(self, mname):
    def match(mtd): return mtd.name == mname
    def finder(cls): return util.exists(match, cls.mtds)
    def getter(cls): return filter(match, cls.mtds)
    return self.in_hierarchy(finder, getter, [])

  # find the method by signature
  @takes("Clazz", unicode, list_of(unicode))
  @returns(optional("Method"))
  def mtd_by_sig(self, mname, sig=[]):
    def match(mtd):
      def subtype_cmp(formal_params, actual_params):
        for f_param, a_param in zip(formal_params, actual_params):
          # actual argument might be null whose type is regarded as Object
          if util.is_class_name(f_param) and a_param == C.J.OBJ: continue

          # ignore undefined types
          cls_f, cls_a = class_lookup(f_param), class_lookup(a_param)
          if not cls_f or not cls_a: return False

          # actual argument is a subtype of formal parameter
          if cls_a <= cls_f: continue

          return False

        # end of for loop; means, all parameters are compatible
        return True

      return mtd.name == mname and len(mtd.param_typs) == len(sig) and \
          subtype_cmp(mtd.param_typs, sig)

    def finder(cls): return util.exists(match, cls.mtds)
    def getter(cls): return util.find(match, cls.mtds)
    return self.in_hierarchy(finder, getter)

  @property
  def inits(self):
    return self.mtd_by_name(self._name)

  @property
  def has_init(self):
    return any(self.inits)

  @takes("Clazz")
  @returns("Method")
  def add_default_init(self):
    init = method.Method(clazz=self, mods=[C.mod.PB], typ=self._name, name=self._name)
    if self._sup and self._sup != C.J.OBJ:
      init.body = st.to_statements(init, u"super();")
    self._mtds.append(init)
    return init

  # add a default-ish, field-initializing constructor
  @takes("Clazz")
  @returns(optional("Method"))
  def add_fld_init(self):
    if not self.mutable_flds: return None
    i_flds = list(enumerate(self.mutable_flds))
    params = map(lambda (i, fld): (fld.typ, u"p{}".format(i)), i_flds)
    init = method.Method(clazz=self, mods=[C.mod.PB], typ=self._name, name=self._name, params=params)
    def init_fld((i, fld)): return fld.name + u" = p{};".format(i)
    body = '\n'.join(map(init_fld, i_flds))
    init.body = st.to_statements(init, body)
    self._mtds.append(init)
    return init

  @staticmethod
  def is_instantiable(tname):
    if tname in C.J.STR: return False
    if not util.is_class_name(tname): return False
    if util.is_array(tname): return False
    # if an existing Clazz, it should be neither an interface nor an enum
    cls = class_lookup(tname)
    return not cls or (not cls.is_itf and not cls.is_abstract and not cls.is_enum)

  # generate a statement that instantiates the given type
  @staticmethod
  def call_init(tname, params=[]):
    args = []
    try:
      cls = class_lookup(tname)
      inits = cls.mtd_by_name(tname) # AttributeError if cls is NoneType
      for init in inits:
        _args = method.sig_match(init.params, params)
        # try to find best matched one
        if len(args) <= len(_args): args = _args
    except (AttributeError, IndexError): pass
    f = exp.gen_E_id(tname)
    args = map(exp.to_expression, args)
    return exp.gen_E_new(exp.gen_E_call(f, args)), args

  # a wrapper of call_init, considering interface implementers
  @staticmethod
  def call_init_if_instantiable(tname, params=[]):
    if Clazz.is_instantiable(tname):
      init_e, _ = Clazz.call_init(tname, params)
      return init_e
    else:
      cls = class_lookup(tname)
      if cls and (cls.is_itf or cls.is_abstract): # try to find implementers
        subss = util.flatten_classes(cls.subs, "subs")
        init_e, args = None, []
        for impl in ifilterfalse(lambda c: c.is_itf or c.is_abstract, subss):
          _e, _args = Clazz.call_init(impl.name, params)
          # try to find best matched one
          if len(args) <= len(_args): init_e, args = _e, _args
        return init_e
    return None

  # declare <clinit> if not exists
  @takes("Clazz")
  @returns("Method")
  def get_or_declare_clinit(self):
    if hasattr(self, C.J.CLINIT): return getattr(self, C.J.CLINIT)
    clinit = method.Method(clazz=self, mods=[C.mod.ST], name=C.J.CLINIT)
    self._mtds.append(clinit)
    setattr(self, C.J.CLINIT, clinit)
    return clinit

  # add static initializer for the given static field
  @takes("Clazz", "Field", list_of("Statement"))
  @returns(nothing)
  def clinit_fld(self, fld, init_ss=[]):
    clinit = self.get_or_declare_clinit()

    # make initializing statements 
    if not init_ss and not fld.is_final:
      call = Clazz.call_init_if_instantiable(fld.typ)
      if call: init_ss = [st.gen_S_assign(exp.gen_E_id(fld.name), call)]

    # update the method body
    if init_ss:
      self.clinit.body.extend(init_ss[:])

  # add initializer for the given instance field
  @takes("Clazz", "Field", list_of("Statement"))
  @returns(nothing)
  def init_fld(self, fld, init_ss=[]):
    # declare <init> if not exists
    inits = self.mtd_by_name(self._name)
    if not inits: inits = [self.add_default_init()]

    # make initializing statements
    if not init_ss and not fld.is_final:
      call = Clazz.call_init_if_instantiable(fld.typ)
      if call: init_ss = [st.gen_S_assign(exp.gen_E_id(fld.name), call)]

    # update the method body
    if init_ss:
      for init in inits: init.body.extend(init_ss[:])


# find the field by the given class and field name
@takes(unicode, unicode, optional(list_of(unicode)))
@returns(optional("Field"))
def find_fld(cname, fname, visited=[]):
  cls = class_lookup(cname)
  if not cls: return None

  # try the current and super class
  fld = cls.fld_by_name(fname)
  if fld: return fld

  # try the outer class if exists
  if cls.outer:
    fld = cls.outer.fld_by_name(fname)
    if fld: return fld

  # search constants in interfaces
  for iname in cls.itfs:
    itf = class_lookup(iname)
    if not itf: continue
    fld = itf.fld_by_name(fname)
    if fld: return fld

  return None


@takes(unicode, callable)
@returns(list_of("Method"))
def __find_mtd(cname, f):
  cls = class_lookup(cname)
  if not cls: return []

  # try to concretize a call to interface
  if (cls.is_itf or cls.is_abstract) and cls.subs:
    for sub in cls.subs:
      mtds = __find_mtd(sub.name, f)
      if mtds: return mtds

  # try the current class and super classes in the hierarchy
  if cls.is_class:
    mtds = f(cls)
    if mtds: return mtds

  # try the outer class if exists
  if cls.outer:
    mtds = f(cls.outer)
    if mtds: return mtds

  return []


# find the method by the given class name and method name
@takes(unicode, unicode)
@returns(list_of("Method"))
def find_mtds_by_name(cname, mname):
  f = lambda cls: cls.mtd_by_name(mname)
  return __find_mtd(cname, f)


# find the method by the given class name, method name, and parameter types
@takes(unicode, unicode, list_of(unicode))
@returns(optional("Method"))
def find_mtd_by_sig(cname, mname, sig):
  f = lambda cls: util.ffilter([cls.mtd_by_sig(mname, sig)])
  mtds = __find_mtd(cname, f)
  if 1 == len(mtds): return mtds[0]
  else: return None


# find the base class of the family in which the given class is involved
@takes(Clazz)
@returns(Clazz)
def find_base(cls):
  if cls.sup:
    sup = class_lookup(cls.sup)
    if sup: return find_base(sup)
  return cls


# merge the given classes into one flat class
# class A { ty1 fld1; }
# class B { ty2 fld2; }
#  => class AB { int kind; ty1 fld1; ty2 fld2; }
# A x; x.fld1 => AB x; x.fld1
@takes(unicode, list_of(Clazz))
@returns(Clazz)
def merge_flat(cname, clss):
  cls_m = Clazz(name=cname)
  kind = field.Field(clazz=cls_m, typ=C.J.i, name=u"kind")
  cls_m.flds.append(kind)
  def cp_fld(fld):
    fld_m = cp.deepcopy(fld)
    fld_m.clazz = cls_m
    cls_m.flds.append(fld_m)
  flds = util.flatten(map(op.attrgetter("flds"), clss))
  map(cp_fld, flds)
  return cls_m


# merge the given classes into a layered class
# class A { ty1 fld1; }
# class B { ty2 fld2; }
#  => class AB { int kind; A a; B b; }
# A x; x.fld1 => AB x; x.a.fld1
@takes(unicode, list_of(Clazz))
@returns(Clazz)
def merge_layer(cname, clss):
  cls_m = Clazz(name=cname)
  kind = field.Field(clazz=cls_m, typ=C.J.i, name=u"kind")
  cls_m.flds.append(kind)
  def layered(cls):
    fld_l = field.Field(clazz=cls_m, typ=cls.name, name=cls.name.lower())
    cls_m.flds.append(fld_l)
  map(layered, clss)
  return cls_m


# anonymous class name
@takes(Clazz)
@returns(unicode)
def anony_name(cls):
  return u"{}${}".format(cls.name, len(cls.inners)+1)


# (DECL (ANNOTATION ...)* modifier* ((FIELD|METHOD) ...))
@takes(Clazz, AST)
@returns(nothing)
def parse_decl(cls, node):
  annos = []
  def anno_filter(node):
    return node.getText() == C.T.ANNO
  for _node in ifilter(anno_filter, node.getChildren()):
    _anno = parse_anno(_node)
    annos.append(_anno)

  tags = map(op.methodcaller("getText"), node.getChildren())
  def mod_filter(tag):
    return tag not in [C.T.ANNO, C.T.CLS, C.T.ITF, C.T.ENUM, C.T.FLD, C.T.MTD]
  mods = filter(mod_filter, tags)

  _node = node.getChildren()[-1]
  f_or_m = _node.getText()

  # (FIELD (TYPE Id) (NAME Id (= (E... ))?))
  if f_or_m == C.T.FLD: field.parse(cls, node, annos, mods)
  # (METHOD (TYPE Id) (NAME Id) (PARAMS (Id Id)+)? (THROWS Id+)? Body)
  elif f_or_m == C.T.MTD: method.parse(cls, node, annos, mods)
  # inner class or interface
  else:
    inner = parse_class(_node)
    inner.annos = annos
    inner.mods = mods
    inner.outer = cls
    cls.inners.append(inner)


# ((class|interface) (NAME Id) ... '{' (DECL ...)* '}')*
@takes(AST)
@returns(Clazz)
def parse_class(node):
  _kind = node.getText()
  if _kind == C.T.ENUM: return parse_enum(node)

  cls = Clazz(kind=_kind)
  flds = []
  mtds = []
  inners = []
  for _node in node.getChildren():
    n_ty = _node.getText()
    # (NAME Id)
    if n_ty == C.T.NAME: cls.name = _node.getChild(0).getText()
    # (extends Id)?
    elif n_ty == C.T.EXT: cls.sup = util.implode_id(_node)
    # (implements Id+)?
    elif n_ty == C.T.IMP:
      for itf in util.implode_id(_node).split(','):
        cls.itfs.append(itf)

    elif n_ty == C.T.DECL:
      parse_decl(cls, _node)

  return cls


# (enum (NAME Id) c (, c)*)
@takes(AST)
@returns(Clazz)
def parse_enum(node):
  _kind = node.getText()
  cls = Clazz(kind=_kind)
  cls.name = node.getChild(0).getChild(0).getText()
  _nodes = node.getChildren()[1:] # exclude name
  constants = util.implode_id(util.mk_v_node_w_children(_nodes)).split(',')
  for c in constants:
    # define representative field
    fld = field.Field(clazz=cls, mods=C.PBST, typ=cls.name, name=c)
    cls.add_fld(fld)
    # initialize it in <clinit>
    f = exp.gen_E_id(cls.name)
    init_e = exp.gen_E_new(exp.gen_E_call(f, []))
    init_s = st.gen_S_assign(exp.gen_E_id(c), init_e)
    cls.clinit_fld(fld, [init_s])
  return cls

