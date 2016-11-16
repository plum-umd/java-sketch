import os
import shutil
from itertools import ifilter, ifilterfalse

from ast.utils import utils
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

"""
regarding paths and files
"""

# clean all the contents in the designated path, excluding that path
def clean_dir(path):
  for root, dirs, files in os.walk(path):
    for f in files:
      try: os.unlink(os.path.join(root, f))
      except OSError: pass # maybe .swp file
    for d in dirs:
      shutil.rmtree(os.path.join(root, d))

def add_object(ast):
  clss = utils.extract_nodes([ClassOrInterfaceDeclaration], ast)
  obj = ClassOrInterfaceDeclaration({u'name':u'Object',u'parentNode':{u'@r':ast.ati},u'atr':ast.ati,u'@i':0})
  def obj_subs(n):
    if not n.extendsList:
      n.extendsList = [obj]
  map(obj_subs, clss)
  ast.types.append(obj)

def rm_subs(clss):
  return filter(lambda c: not c.extendsList, clss)

def sanitize_mname(mname):
  return mname.replace("[]",'s')

def repr_fld(var, fld):
  return u"{}_{}".format(var.name, fld.sanitize_ty(fld.parentNode.name))

def repr_cls(cls):
  return cls.sanitize_ty(cls.name)

# ~ List.partition in OCaml
# divide the given list into two lists:
# one satisfying the conditoin and the other not satisfying the condition
# e.g., \x . x > 0, [1, -2, -3, 4] -> [1, 4], [-2, -3]
def partition(pred, lst):
  return list(ifilter(pred, lst)), list(ifilterfalse(pred, lst))

# get the contets of buf, close it, return contents
def get_and_close(buf):
  v = buf.getvalue()
  buf.close()
  return v

# flatten class declarations or hierarchy
# "inners": class A { class Inner { class InnerMost }} -> [A, Inner, InnerMost]
# "subs": ActA, ActB, ... < Act < Cxt -> [Cxt, Act, ActA, ActB, ...]
def flatten_classes(cls):
  lst = [cls]
  def flatten(c):
    for s in c.subClasses:
      lst.append(s)
      flatten(s)
  flatten(cls)
  return lst
