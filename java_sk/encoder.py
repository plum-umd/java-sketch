import os
import util
import cStringIO
import copy as cp
from functools import partial

from . import TYPES as T
from ast.utils import utils
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

# global constants that should be placed at every sketch file
# Can I get rid of this? Don't care for global vars
_const = u''
_flds = {} # { cname.fname : new_fname }
_s_flds = {} # { cname.fname : accessor }
_ty = {} # { tname : new_tname }

# more globals to check out.
magic_S = 7
_const = u"""
int S = {}; // length of arrays for Java collections
""".format(magic_S)

CLASS_NUMS = {u'Object':0,u'void':-1}
    
def find_main(prg):
  clss = []
  utils.extract_nodes(clss, ClassOrInterfaceDeclaration, prg)

  mtds = []
  for c in clss:
    utils.extract_nodes(mtds, MethodDeclaration, c)
    mtds = filter(lambda m: td.isStatic(m) and m.name == u'main', mtds)
  lenn = len(mtds)
  if lenn > 1:
    raise Exception("multiple main()s", mtds)
  return mtds[0] if lenn == 1 else None

def find_harness(prg):
  # TODO: these can also be specified with annotations -- we don't support those yet
  mtds = []
  utils.extract_nodes(mtds, MethodDeclaration, prg)
  mtds = filter(lambda m: td.isHarness(m), mtds)
  return mtds[0] if mtds else None

def main_cls(prg):
  # get the main method and pull it's corresponding class out of the symtab.
  main = find_main(prg)
  main = prg.symtab[main.atr] if main else None
  harness = find_harness(prg)
  harness = prg.symtab[harness.atr] if harness else None
  if main:
    return main
  elif harness:
    return harness
  else: raise Exception("None of main() and @Harness is found")

def to_sk(prg, sk_dir):
  # clean up result directory
  if os.path.isdir(sk_dir): util.clean_dir(sk_dir)
  else: os.makedirs(sk_dir)

  # consist here -- skipping b/c it looks like mostly inheritance stuff
  # which i don't care about yet
  # pgr.consist()
  gen_type_sk(sk_dir, prg)

def gen_type_sk(sk_dir, prg):
  buf = cStringIO.StringIO()
  buf.write("package type;\n")
  buf.write(_const)

  # populate global dict of types, classes and their ids
  clss = []
  utils.extract_nodes(clss, ClassOrInterfaceDeclaration, prg)

  # bases is just Object?
  i = 1
  for c in clss:
    if c.name not in CLASS_NUMS.keys():
      CLASS_NUMS[c.name] = i
      i = i + 1
  CLASS_NUMS[u'int'] = i

  bases = util.rm_subs(clss)
  buf.write('\n'.join(filter(None, map(to_struct, bases))))

  mtds = []
  utils.extract_nodes(mtds, MethodDeclaration, prg)
  
  # argument number of methods
  arg_num = map(lambda m: str(len(m.parameters)), mtds)
  buf.write("""
    #define _{0} {{ {1} }}
    int {0}(int id) {{
      return _{0}[id];
    }}
  """.format('argNum', ", ".join(arg_num)))

  # argument types of methods
  arg_typs = []
  for m in mtds:
    arg_typs.append('{'+', '.join(map(lambda p: str(CLASS_NUMS[p.typee.name]), m.parameters)) +'}')
  buf.write("""
    #define _{0} {{ {1} }}
    int {0}(int id, int idx) {{
      return _{0}[id][idx];
    }}
  """.format('argType', ", ".join(arg_typs)))

  # return type of methods
  ret_typs = map(lambda r: str(CLASS_NUMS[r.typee.name]), mtds)
  buf.write("""
    #define _{0} {{ {1} }}
    int {0}(int id) {{
      return _{0}[id];
    }}
  """.format('retType', ", ".join(ret_typs)))

  # belonging class of methods
  belongs_to = map(lambda mtd: CLASS_NUMS[mtd.parentNode.name], mtds)
  buf.write("""
    #define _{0} {{ {1} }}
    int {0}(int id) {{
      return _{0}[id];
    }}
  """.format(u'belongsTo', ", ".join(map(str, belongs_to))))

  # I have no idea why this is necesary...
  # rearrange the classes
  int_cls = ClassOrInterfaceDeclaration({u'name':u'int'})
  obj_cls, clss = util.partition(lambda x: x.name == u'Object', clss)
  obj_cls = obj_cls[0]
  obj_cls.subClasses.append(int_cls)
  clss = [obj_cls] + clss
  clss.append(int_cls)
  clss.append(int_cls)
  clss.append(obj_cls)
  subcls = \
      map(lambda cls_i: '{' + ", ".join( \
          map(lambda cls_j: str(utils.is_subclass(cls_i, cls_j)).lower(), clss) \
      ) + '}', clss)
  buf.write("""
    #define _{0} {{ {1} }}
    bit {0}(int i, int j) {{
      return _{0}[i][j];
    }}
  """.format(u'subcls', ", ".join(subcls)))
  print buf.getvalue()
  with open(os.path.join(sk_dir, "type.sk"), 'w') as f:
    f.write(buf.getvalue())
    # logging.info("encoding " + f.name)
  buf.close()

# only called on base classes. This seems to just be Object?  
def to_struct(cls):
    # make mappings from static fields to corresponding accessors
    flds = []
    def gen_s_flds_accessors(cls):
      # when this is called update the list of fields for cls
      utils.extract_nodes(flds, FieldDeclaration, cls)
      # s_flds = filter(lambda f: td.isStatic(f) and not td.isPrivate(f), flds)
      # global _s_flds
      # for fld in s_flds:
      #   cname = cls.name
      #   fid = '.'.join([cname, fld.name])
      #   fname = utils.repr_fld(fld)
      #   _s_flds[fid] = fname
    cname = util.sanitize_ty(cls.name)
    # global _ty

    # if cls.is_itf: # deal with iterfaces later
    #   gen_s_flds_accessors(cls)
        # ...
        # return ''

    if not cls.extendsList:
      cls = to_v_struct(cls)
    gen_s_flds_accessors(cls)

    # for unique class numbering, add an identity mapping
    # if cname not in _ty: _ty[cname] = cname

    buf = cStringIO.StringIO()
    buf.write("struct " + cname + " {\n  int hash;\n  ")

    # to avoid static fields, which will be bound to a class-representing package
    i_flds = filter(lambda f: not td.isStatic(f), flds)
    buf.write('\n  '.join(map(trans_fld, i_flds)))
    if i_flds: buf.write('\n')
    buf.write("}\n")
    
    return buf.getvalue()

def to_v_struct(cls):
  cls_d = {u'name':cls.name}
  cls_v = ClassOrInterfaceDeclaration(cls_d)
  fld_d = {u'variables':
           {u'@e': [{u'@t': u'VariableDeclarator', u'id': {u'name': u'__cid'}}]},
          u'@t': u'FieldDeclaration', u'type':
           {u'@t': u'PrimitiveType', u'type':
            {u'nameOfBoxedType': u'Integer', u'name': u'Int'}}}
  cls_v.childrenNodes.append(FieldDeclaration(fld_d))

  # global _ty, _flds, _s_flds
  def per_cls(sup_flds, cls):
    # keep mappings from original subclasses to the representative
    # so that subclasses can refer to the representative
    # e.g., for C < B < A, { B : A, C : A }
    cname = util.sanitize_ty(cls.name)
    if cname != cls_v.name: # exclude the root of this family
      _ty[cname] = cls_v.name
      # if cls.is_inner: # to handle inner class w/ outer class name
      #   _ty[unicode(repr(cls))] = cls_v.name
    # for itf in cls.itfs: # interface stuff, don't care yet
    #   pass
    # for sup_fld in sup_flds.keys():
    #   fld = sup_flds[sup_fld]
    #   fname = util.repr_fld(fld)
    #   fid = '.'.join([cname, sup_fld])
    #   if td.isStatic(fld): _s_flds[fid] = fname
    #   else: _flds[fid] = fname

    cur_flds = cp.deepcopy(sup_flds)
    def cp_fld(fld):
      cur_flds[fld.name] = fld

      fname = util.repr_fld(fld)
      fld_v = cp.deepcopy(fld)
      fld_v.parentNode = cls_v
      fld_v.name = fname
      cls_v.members.append(fld_v)
      cls_v.childrenNodes.append(fld_v)

      # def upd_flds(cname):
      #   fid = '.'.join([cname, fld.name])
      #   # if A.f1 exists and B redefines f1, then B.f1 : f1_A
      #   # except for enum, which can (re)define its own fields
      #   # e.g., SwingConstands.LEADING vs. GroupLayout.Alignment.LEADING
      #   # if not cls.is_enum and (fid in _s_flds or fid in _flds): return
      #   if td.isStatic(fld): _s_flds[fid] = fname
      #   else: _flds[fid] = fname # { ..., B.f2 : f2_B }

      # upd_flds(cname)
    flds = []
    utils.extract_nodes(flds, FieldDeclaration, cls)
    map(cp_fld, flds)
    map(partial(per_cls, cur_flds), cls.subClasses)

  per_cls({}, cls)

  return cls_v

def trans_fld(fld):
  buf = cStringIO.StringIO()
  buf.write(' '.join([trans_ty(fld.typee.name), fld.name]))
  # let's ignore initialised fields
  # if fld.is_static and fld.init and \
  #     not fld.init.has_call and not fld.init.has_str and not fld.is_aliasing:
    # buf.write(" = " + trans_e(None, fld.init))
  buf.write(';')
  return buf.getvalue()

def trans_ty(tname):
  # ignoring a lot of 'advanced' type stuff
  _tname = util.sanitize_ty(tname.strip())
  
  global _ty
  r_ty = _tname
  if _tname in [T[u'BYTE'], T[u'SHORT'], T[u'LONG'], T[u'OBYTE'], T[u'OSHORT'], \
                T[u'OLONG'], T[u'OINT']]: r_ty = T[u'INT']
  return r_ty

