import cStringIO
import logging
import operator as op

from antlr3.tree import CommonTree as AST

from lib.typecheck import *
import lib.const as C
import lib.visit as v

from .. import util

from . import field_nonce, register_field
import expression as exp
import clazz

class Field(v.BaseNode):

  def __init__(self, **kwargs):
    self._id = field_nonce()

    self._clazz = kwargs.get("clazz", None) # for Java-to-C translation
    self._annos = kwargs.get("annos", [])
    self._mods = kwargs.get("mods", [])
    self._typ = kwargs.get("typ", None)
    self._name = kwargs.get("name", None)
    self._init = kwargs.get("init", None)

    register_field(self)

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
  def is_private(self):
    return C.mod.PR in self._mods

  @property
  def is_static(self):
    return C.mod.ST in self._mods

  @property
  def is_final(self):
    return C.mod.FN in self._mods

  @property
  def is_aliasing(self):
    if not self._init: return False
    if not self.is_static or not self.is_final: return False
    fld_a = None
    if self._init.kind == C.E.DOT:
      rcv_ty = exp.typ_of_e(None, self._init.le)
      fld_a = clazz.find_fld(rcv_ty, self._init.re.id)
    elif self._init.kind == C.E.ID:
      fld_a = clazz.find_fld(self._clazz.name, self._init.id)
    return fld_a != None

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
  def init(self):
   return self._init

  @init.setter
  def init(self, v):
    self._init = v

  def __repr__(self):
    return u"{}_{}".format(self._name, util.sanitize_ty(self._clazz.name))

  def __str__(self):
    buf = cStringIO.StringIO()
    if self._mods: buf.write(' '.join(self._mods) + ' ')
    buf.write(' '.join([self._typ, self._name]))
    if self._init: buf.write(" = " + str(self._init))
    buf.write(';')
    return buf.getvalue()

  def __eq__(self, other):
    return repr(self) == repr(other)

  def accept(self, visitor):
    visitor.visit(self)
    if self._init: self._init = self._init.accept(visitor)

  def jsonify(self):
    m = {}
    if self._mods: m["mods"] = self._mods
    m["type"] = self._typ
    m["name"] = self._name
    return m


# (DECL (ANNOTATION ...)* modifier* ((FIELD|METHOD) ...))
# (FIELD (TYPE Id) (NAME Id (= (E... ))?))
@takes("Clazz", AST, list_of("Anno"), list_of(unicode))
@returns(nothing)
def parse(cls, node, annos, mods):
  _node = node.getChildren()[-1]

  typ = util.implode_id(_node.getChild(0))
  name = _node.getChild(1)
  fid = name.getChild(0).getText()
  if name.getChildCount() > 1:
    init = exp.parse_e(name.getChild(1).getChild(0), cls)
  else: init = None
  fld = Field(clazz=cls, annos=annos, mods=mods, typ=typ, name=fid, init=init)
  cls.flds.append(fld)

