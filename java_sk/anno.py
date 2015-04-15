import cStringIO

from antlr3.tree import CommonTree as AST

from lib.typecheck import *
import lib.const as C
from lib.enum import enum

import util

C.A = enum(OVERRIDE="Override", SUPWARN="SuppressWarnings", \
  HARNESS="Harness")

class Anno(object):

  def __init__(self, **kwargs):
    for key in kwargs:
      setattr(self, key, kwargs[key])

  def __str__(self):
    buf = cStringIO.StringIO()
    buf.write('@' + self.name)

    attrs = [var for var in vars(self) if "name" not in var]
    if attrs:
      def var_to_str(var, print_var_too=True):
        s_attr = str(getattr(self, var)).replace('[','{').replace(']','}')
        if print_var_too: return var+"="+s_attr
        else: return s_attr

      buf.write('(')
      if len(attrs) == 1: buf.write(var_to_str(attrs[0], False))
      else: buf.write(", ".join(map(var_to_str, attrs)))
      buf.write(')')

    return buf.getvalue()

  def __repr__(self):
    return self.__str__()

  # find the designated annotation by attributes
  @takes("Anno", dict_of(str, str))
  @returns(bool)
  def by_attr(self, attrs):
    for k, v in attrs.iteritems():
      if not hasattr(self, k) or getattr(self, k) != v: return False
    return True

  # find the designated annotation by name
  @takes("Anno", str)
  @returns(bool)
  def by_name(self, name):
    return self.by_attr({"name": name})


# (ANNOTATION (NAME Id) (ELEMS (Val | (= Id Val)+))?)
@takes(AST)
@returns(Anno)
def parse_anno(node):
  _anno = Anno(name = node.getChild(0).getChild(0).getText())

  ##
  ## Java annotations
  ##
  if _anno.name == C.A.OVERRIDE: pass
  elif _anno.name == C.A.SUPWARN: pass

  # (A... (NAME Harness) (ELEMS "what"))
  elif _anno.name == C.A.HARNESS:
    what = node.getChild(1).getChild(0).getText().strip('"')
    setattr(_anno, "f", what)

  else: raise Exception("unhandled @annotation", node.toStringTree())

  return _anno

