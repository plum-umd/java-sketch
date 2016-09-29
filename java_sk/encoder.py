import os
import util
import cStringIO
import copy as cp

from visit.translator import Translator

from ast.utils import utils
from ast.body.parameter import Parameter
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.constructordeclaration import ConstructorDeclaration
from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

class Encoder(object):
  def __init__(self, program):
    # more globals to check out.
    magic_S = 7
    self._const = u"int S = {}; // length of arrays for Java collections\n".format(magic_S)
    self._tltr = Translator()
    self._prg = program
    self._sk_dir = ''

  def find_main(self):
    clss = []
    clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self.prg)
  
    mtds = []
    for c in clss:
      mtds = utils.extract_nodes([MethodDeclaration, ConstructorDeclaration], c)
      mtds = filter(lambda m: td.isStatic(m) and m.name == u'main', mtds)
      lenn = len(mtds)
      if lenn > 1:
        raise Exception("multiple main()s", mtds)
      return mtds[0] if lenn == 1 else None

  def find_harness(self):
    # TODO: these can also be specified with annotations -- we don't support those yet
    mtds = []
    mtds = utils.extract_nodes([MethodDeclaration, ConstructorDeclaration], self.prg)
    mtds = filter(td.isHarness, mtds)
    return mtds[0] if mtds else None

  def main_cls(self):
    # get the main method and pull it's corresponding class out of the symtab.
    main = self.find_main()
    main = self.prg.symtab[main.atr] if main else None
    harness = self.find_harness()
    harness = self.prg.symtab[harness.atr] if harness else None
    if main:
      return main
    elif harness:
      return harness
    else: raise Exception("No main(), @Harness, or harness found")

  def to_sk(self):
    # clean up result directory
    if os.path.isdir(self.sk_dir): util.clean_dir(self.sk_dir)
    else: os.makedirs(self.sk_dir)

    # type.sk
    # consist builds up some class hierarchies which I think we can do differently
    # pgr.consist()
    self.gen_type_sk()

    # cls.sk
    cl_sks = []
    clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self.prg)
    for cls in clss:
      cls_sk = self.gen_cls_sk(cls)
      if cls_sk: cl_sks.append(cls_sk)

  def gen_cls_sk(self, cls):
    mtds = utils.extract_nodes([MethodDeclaration, ConstructorDeclaration], cls)
    flds = utils.extract_nodes([FieldDeclaration], cls)
    s_flds = filter(td.isStatic, flds)

    if not cls.interface and not mtds and not s_flds: return None
    # else: return None # interface or enum...not supported

    cname = util.sanitize_ty(cls.name)
    buf = cStringIO.StringIO()
    buf.write("package {};\n".format(cname))
    buf.write(self.const)

    buf.write('\n'.join(map(self.tltr.trans_fld, s_flds)))
    if s_flds: buf.write('\n')

    # init and clinit stuff being ignored here
    for m in mtds:
      if m.parentNode.interface: continue
      buf.write(self.to_func(m) + os.linesep)

    cls_sk = cname + ".sk"
    with open(os.path.join(self.sk_dir, cls_sk), 'w') as f:
      f.write(util.get_and_close(buf))
      return cls_sk

  def to_func(self, mtd):
    buf = cStringIO.StringIO()
    # if td.isGenerator(mtd): buf.write(C.mod.GN + ' ') # dont have generators yet
    if td.isHarness(mtd): buf.write(u'harness' + ' ')
    ret_ty = self.tltr.trans_ty(mtd.typee.name)
    buf.write(ret_ty + ' ' + self.tltr.trans_mname(mtd) + '(')

    if td.isStatic(mtd): params = mtd.parameters
    else:
      self_ty = self.tltr.trans_ty(util.repr_cls(mtd.parentNode))
      params = [Parameter({u'id':{u'name':u'self'},u'type':{u'@t':u'Type',u'name':self_ty}})] + mtd.parameters

    buf.write(', '.join(map(lambda p: self.tltr.trans_params((p.typee.name, p.name)), params)))
    buf.write(') {\n')
    self.tltr.mtd = mtd
    body = self.tltr.trans_stmt(mtd.body)
    buf.write(body)
    buf.write('\n}\n')
    return util.get_and_close(buf)

  def gen_type_sk(self):
    CLASS_NUMS = {u'Object':0,u'void':-1}

    buf = cStringIO.StringIO()
    buf.write("package type;\n")
    buf.write(self._const)

    # populate global dict of types, classes and their ids
    clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self.prg)

    i = 1
    for c in clss:
      if c.name not in CLASS_NUMS.keys():
        CLASS_NUMS[c.name] = i
      i = i + 1
    CLASS_NUMS[u'int'] = i

    # bases is just Object?
    bases = util.rm_subs(clss)
    buf.write('\n'.join(filter(None, map(self.to_struct, bases))))

    mtds = utils.extract_nodes([MethodDeclaration, ConstructorDeclaration], self.prg)
  
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
    subcls = map(lambda cls_i: '{' + ", ".join(
      map(lambda cls_j: str(utils.is_subclass(cls_i, cls_j)).lower(),
          clss)) + '}',
                 clss)
    buf.write("""
#define _{0} {{ {1} }}
bit {0}(int i, int j) {{
  return _{0}[i][j];
}}
  """.format(u'subcls', ", ".join(subcls)))
    with open(os.path.join(self.sk_dir, "type.sk"), 'w') as f:
      f.write(buf.getvalue())
      # logging.info("encoding " + f.name)
    buf.close()

  # only called on base classes. This seems to just be Object?  
  def to_struct(self, cls):
    # this is a bit hacky, but it's the only way to access this from inside gen_s
    flds = [utils.extract_nodes([FieldDeclaration], cls)]

    # make mappings from static fields to corresponding accessors
    def gen_s_flds_accessors(cls):
      # when this is called update the list of fields for cls
      flds[0] = utils.extract_nodes([FieldDeclaration], cls)
      # s_flds = filter(lambda f: td.isStatic(f) and not td.isPrivate(f), flds)
      # global _s_flds
      # for fld in s_flds:
      #   cname = cls.name
      #   fid = '.'.join([cname, fld.name])
      #   fname = utils.repr_fld(fld)
      #   _s_flds[fid] = fname
    cname = util.sanitize_ty(cls.name)

    # if cls.is_itf: # deal with iterfaces later

    if not cls.extendsList: cls = self.to_v_struct(cls)
    gen_s_flds_accessors(cls)
    
    # for unique class numbering, add an identity mapping
    # if cname not in _ty: _ty[cname] = cname
  
    buf = cStringIO.StringIO()
    buf.write("struct " + cname + " {\n  int hash;\n  ")
  
    # to avoid static fields, which will be bound to a class-representing package
    i_flds = filter(lambda f: not td.isStatic(f), flds[0])
    buf.write('\n  '.join(map(self.tltr.trans_fld, i_flds)))
    if i_flds: buf.write('\n')
    buf.write("}\n")
    return util.get_and_close(buf)

  def to_v_struct(self, cls):
    cls_d = {u'name':cls.name}
    cls_v = ClassOrInterfaceDeclaration(cls_d)
    fld_d = {u'variables':
             {u'@e': [{u'@t': u'VariableDeclarator', u'id': {u'name': u'__cid'}}]},
             u'@t': u'FieldDeclaration', u'type':
             {u'@t': u'PrimitiveType', u'type':
              {u'nameOfBoxedType': u'Integer', u'name': u'Int'}}}
    cls_v.childrenNodes.append(FieldDeclaration(fld_d))

    def per_cls(cls):
      if util.sanitize_ty(cls.name) != cls_v.name:
        self.tltr.ty[cls.name] = cls_v.name
      flds = []
      flds = utils.extract_nodes([FieldDeclaration], cls)
      def cp_fld(fld):
        fname = util.repr_fld(fld)
        fld_v = cp.deepcopy(fld)
        fld_v.parentNode = cls_v
        fld_v.name = fname
        cls_v.members.append(fld_v)
        cls_v.childrenNodes.append(fld_v)
      map(cp_fld, flds)
      map(per_cls, cls.subClasses)
    per_cls(cls)

    return cls_v

  @property
  def prg(self): return self._prg
  @prg.setter
  def prg(self, v): self._prg = v

  @property
  def tltr(self): return self._tltr
  @tltr.setter
  def tltr(self, v): self._tltr = v

  @property
  def const(self): return self._const
  @const.setter
  def const(self, v): self._const = v

