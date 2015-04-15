import lib.const as C
from lib.enum import enum

from .. import util

C.mod = enum(PR=u"private", PB=u"public", \
    AB=u"abstract", ST=u"static", FN=u"final", \
    GN=u"generator", HN=u"harness")
C.PBST = [C.mod.PB, C.mod.ST]
C.PRST = [C.mod.PR, C.mod.ST]
C.sk_mod = [C.mod.GN, C.mod.HN]

# snapshot of meta-class # Field

# to assign unique id to an instance
__fid = -1
# an array of all the instnaces whose id is equal to index being inserted
# i.e., Field.flds(fid).id == fid
__flds = []

def field_nonce():
  global __fid
  __fid = __fid + 1
  return __fid

def fields():
  global __flds
  return __flds

def fields_reset(flds=[]):
  global __fid, __flds
  if flds:
    __fid = len(flds)
    __flds = flds
  else:
    __fid = -1
    __flds = []

def register_field(fld):
  global __flds
  __flds.append(fld)

# snapshot of meta-class # Method

__mid = -1
__mtds = []

def method_nonce():
  global __mid
  __mid = __mid + 1
  return __mid

def methods():
  global __mtds
  return __mtds

def methods_reset(mtds=[]):
  global __mid, __mtds
  if mtds:
    __mid = len(mtds)
    __mtds = mtds
  else:
    __mid = -1
    __mtds = []

def register_method(mtd):
  global __mtds
  __mtds.append(mtd)

# snapshot of meta-class # Clazz

__cid = -1
__clss = []

def class_nonce():
  global __cid
  __cid = __cid + 1
  return __cid

def classes():
  global __clss
  return __clss

def classes_reset(clss=[]):
  global __cid, __clss
  if clss:
    __cid = len(clss)
    __clss = clss
  else:
    __cid = -1
    __clss = []

def register_class(cls):
  global __clss
  __clss.append(cls)

def class_lookup(cname):
  _cname = util.sanitize_ty(unicode(cname))
  global __clss
  for c in __clss:
    cls_r = repr(c)
    # normal case
    if c.name == cname: return c
    if c.is_inner:
      # full name of inner class, e.g., Demo$CancelAction
      if _cname == cls_r: return c
      # inner class w/o outer class name, e.g., Align
      if cname in cls_r.split('_'): return c
  return None

