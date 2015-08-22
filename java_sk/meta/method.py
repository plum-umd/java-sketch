import cStringIO
import logging
import operator as op

from antlr3.tree import CommonTree as AST

from lib.typecheck import *
import lib.const as C
import lib.visit as v

from .. import util

from . import method_nonce, register_method, class_lookup
import statement as st

class Method(v.BaseNode):

  def __init__(self, **kwargs):
    self._id = method_nonce()

    self._clazz = kwargs.get("clazz", None) # for Java-to-C translation
    self._annos = kwargs.get("annos", [])
    self._mods = kwargs.get("mods", [])
    self._typ = kwargs.get("typ", C.J.v)
    self._name = kwargs.get("name", None)
    # to keep the order of parameters, can't be {}
    self._params = kwargs.get("params", [])
    self._throws = kwargs.get("throws", [])
    # updated while parsing the body
    self._locals = { \
        C.J.N: C.J.OBJ, \
        C.J.THIS: self._clazz.name, \
        C.J.SUP: self._clazz.sup \
    }
    self._body = []

    register_method(self)

  @property
  def id(self):
    return self._id

  @property
  def clazz(self):
    return self._clazz

  @clazz.setter
  def clazz(self, v):
    self._clazz = v

  @property
  def annos(self):
    return self._annos

  @property
  def mods(self):
    return self._mods

  @property
  def is_static(self):
    return C.mod.ST in self._mods

  @property
  def is_abstract(self):
    return C.mod.AB in self._mods

  @property
  def typ(self):
    return self._typ

  @typ.setter
  def typ(self, v):
    self._typ = v

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, v):
    self._name = v

  @property
  def is_init(self):
    return util.is_class_name(self._name) and self._name == self._typ

  @property
  def is_clinit(self):
    return self._name == C.J.CLINIT

  @property
  def params(self):
    return self._params

  @property
  def param_typs(self):
    typs, _ = util.split(self._params)
    return typs

  @property
  def param_vars(self):
    _, args = util.split(self._params)
    return args

  @property
  def signature(self):
    params = ", ".join(self.param_typs)
    return "{} {}.{}({})".format(self._typ, self._clazz.name, self._name, params)

  @property
  def locals(self):
    return self._locals

  @locals.setter
  def locals(self, v):
    self._locals = v

  @property
  def vars(self):
    d_flds = { fld.name: fld.typ for fld in self._clazz.flds }
    d_params = { nm: ty for (ty, nm) in self._params }
    # the order of merging is important
    # in this way, variables declared later overwrite fields and parameters
    d_merged = dict(d_flds, **d_params)
    return dict(d_merged, **self._locals)

  @property
  def body(self):
    return self._body

  @body.setter
  def body(self, v):
    self._body = v

  @property
  def has_return(self):
    return util.exists(op.attrgetter("has_return"), self.body)

  def __repr__(self):
    mname, cname = self._name, repr(self._clazz)
    params = map(util.sanitize_ty, self.param_typs)
    return u'_'.join([mname, cname] + params)

  def __str__(self, s_printer=str):
    buf = cStringIO.StringIO()
    if self._mods:
      buf.write(' '.join(list(set(self._mods) - set(C.sk_mod))) + ' ')
    # <clinit> won't have type signature
    if self._name != C.J.CLINIT:
      # not to print constructor (i.e., class name) twice
      if self._typ != self._name: buf.write(self._typ + ' ')
      buf.write(self._name + " (")
      def str_param( (ty, nm) ): return ' '.join([ty, nm])
      buf.write(", ".join(map(str_param, self._params)))
      buf.write(')')
      if self._throws:
        buf.write(" {} {}".format(C.T.THROWS, ", ".join(self._throws)))
    # interfaces and abstract methods won't have method body
    if self._clazz.is_itf or self.is_abstract: buf.write(';')
    else:
      buf.write(" {\n")
      buf.write('\n'.join(map(s_printer, self._body)))
      buf.write("\n}\n")
    return buf.getvalue()

  def __eq__(self, other):
    return repr(self) == repr(other)

  def is_supercall(self, other):
    if self._name != other.name: return False
    if len(self._params) != len(other.params): return False
    if not (self._clazz <= other.clazz): return False
    args = sig_match(other.params, self._params)
    for (_, nm), arg in zip(self._params, args):
      if nm != arg: return False
    return True

  def accept(self, visitor):
    visitor.visit(self)
    f = op.methodcaller("accept", visitor)
    self._body = util.flatten(map(f, self._body))

  def jsonify(self):
    m = {}
    if self._mods: m["mods"] = self._mods
    m["type"] = self._typ
    m["name"] = self._name
    if self._params:
      m["params"] = [ {"type": ty, "name": nm} for (ty, nm) in self._params ]
    return m


@takes(list_of(tuple_of(unicode)), list_of(tuple_of(unicode)))
@returns(list_of(unicode))
def param_match(params1, params2):
  r = []
  cp_params = params2[:]
  for (ty_formal, nm_formal) in params1:
    # setting default argument
    if util.is_class_name(ty_formal):
      if ty_formal == C.J.STR: arg = u"\"\""
      else: arg = C.J.N
    elif ty_formal == C.J.z: arg = u"false"
    else: arg = u'0' # NOTE: perhaps buggy
    cls_formal = class_lookup(ty_formal)
    def candidate_by_ty( (ty_actual, _) ):
      cls_actual = class_lookup(ty_actual)
      return cls_actual <= cls_formal
    def candidate_by_nm( (_, nm_actual) ):
      return nm_actual in nm_formal
    candidates_ty = filter(candidate_by_ty, cp_params)
    if candidates_ty:
      if util.exists(candidate_by_nm, candidates_ty):
        ty_actual, nm_actual = util.find(candidate_by_nm, candidates_ty)
      else: ty_actual, nm_actual = candidates_ty[0]
      cp_params.remove( (ty_actual, nm_actual) )
      arg = nm_actual
    r.append(arg)
  return r


# pick type-matched arguments (if possible)
# e.g., sig_match([(C,x),(D,y),(C,z)], [(int,a),(C,b),(C,c)]) = [b,"null",c]
# if there exist multiple instances of a certain type,
# name-matched or left-most one will be chosen.
@takes(list_of(tuple_of(unicode)), list_of(tuple_of(unicode)))
@returns(list_of(unicode))
def sig_match(sig, params):
  return param_match(sig, params)


# find type-matched formal parameters (if possible)
# e.g., find_formals([(C,x),(D,y),(C,z)], [C, D]) = [x, y]
# similarly, the left-most one will be chosen, if there are multiple choices
@takes(list_of(tuple_of(unicode)), list_of(unicode))
@returns(list_of(unicode))
def find_formals(sig, typs):
  # bogus_params = [(C, '0'), (D, '1')]
  bogus_params = [ (ty, unicode(i)) for i, ty in enumerate(typs) ]
  # args_idx = ['0', '1']
  args_idx = param_match(sig, bogus_params)
  # matched = [(C, x), (D, y)]
  matched = [ sig[int(i)] for i in args_idx if i != C.J.N ]
  # return [x, y]
  return [ nm for _, nm in matched ]


# an expression to call the given static method
@takes(Method, list_of(tuple_of(unicode)))
@returns(unicode)
def call_stt(mtd, params):
  args = sig_match(mtd.params, params)
  return u"{}.{}({})".format(mtd.clazz.name, mtd.name, ", ".join(args))


# (DECL (ANNOTATION ...)* modifier* ((FIELD|METHOD) ...))
# (METHOD (TYPE Id) (NAME Id) (PARAMS (Id Id)+)? (THROWS Id+)? Body)
@takes("Clazz", AST, list_of("Anno"), list_of(unicode))
@returns(nothing)
def parse(cls, node, annos, mods):
  _node = node.getChildren()[-1]

  typ = util.implode_id(_node.getChild(0))
  name = _node.getChild(1).getChild(0).getText()
  b_idx = 2
  params = []
  if _node.getChild(b_idx).getText() == C.T.PARA:
    __params = _node.getChild(b_idx).getChildren()
    s_params = map(op.methodcaller("getText"), __params)
    ty = u''
    for p in s_params:
      if p in ['.', '[', ']', '<', '>', '?']: ty += p
      elif ty.endswith('.'): ty += p
      elif not ty: ty = p
      else:
        params.append( (ty, p) )
        ty = u''
    b_idx = b_idx + 1

  throws = []
  if _node.getChild(b_idx).getText() == C.T.THROWS:
    _throws = util.mk_v_node_w_children(_node.getChild(b_idx).getChildren())
    throws = util.implode_id(_throws).split(',')
    b_idx = b_idx + 1

  mtd = Method(clazz=cls, annos=annos, mods=mods, typ=typ, name=name, params=params, throws=throws)
  mtd.body = st.parse(mtd, _node.getChildren()[b_idx:])
  cls.mtds.append(mtd)

