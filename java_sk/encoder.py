import os
import util
import cStringIO
import math
import copy as cp
import logging
from itertools import ifilterfalse

from . import builtins

from .translator import Translator

from ast.utils import utils
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.constructordeclaration import ConstructorDeclaration
from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

class Encoder(object):
    def __init__(self, program):
        # more globals to check out.
        self._prg = program
        self._prg.symtab.update(builtins)
        self._sk_dir = ''

        self._harness = None
        self._bases = []
        
        # populate global dict of types, classes and their ids
        self._clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self._prg)
        self._CLASS_NUMS = {u'Object':1}
        i = 2
        for c in self._clss:
            if c.name not in self._CLASS_NUMS.keys():
                self._CLASS_NUMS[c.name] = i
                i = i + 1
                self._CLASS_NUMS[u'int'] = i
                self._CLASS_NUMS[u'double'] = i+1

        self._mtds = utils.extract_nodes([MethodDeclaration], self._prg)
        self._cons = utils.extract_nodes([ConstructorDeclaration], self._prg)
        self._MTD_NUMS = {}
        i = 0
        for m in self._mtds+self._cons:
            if m.name not in self._MTD_NUMS.keys():
                self._MTD_NUMS[m] = i
                i = i + 1
                self._primitives = ['int', 'void', 'double', 'byte', 'short', 'long']
                self._tltr = Translator(cnums=self._CLASS_NUMS, mnums=self._MTD_NUMS)

    def find_main(self):
        mtds = []
        for c in self.clss:
            mtds = utils.extract_nodes([MethodDeclaration, ConstructorDeclaration], c)
            mtds = filter(lambda m: td.isStatic(m) and m.name == u'main', mtds)
            lenn = len(mtds)
            if lenn > 1:
                raise Exception("multiple main()s", mtds)
                return mtds[0] if lenn == 1 else None

    def find_harness(self):
        # TODO: these can also be specified with annotations -- we don't support those yet
        mtds = filter(td.isHarness, self.mtds)
        self.harness = mtds[0] if mtds else None
        return self.harness
      
    def main_cls(self):
        # get the main method and pull it's corresponding class out of the gsymtab.
        main = self.find_main()
        main = self.prg.gsymtab[main.atr] if main else None
        harness = self.find_harness()
        harness = self.prg.gsymtab[harness.atr] if harness else None
        if main: return main
        elif harness: return harness
        else: raise Exception("No main(), @Harness, or harness found")

    def to_sk(self):
        # clean up result directory
        if os.path.isdir(self.sk_dir): util.clean_dir(self.sk_dir)
        else: os.makedirs(self.sk_dir)

        # consist builds up some class hierarchies which happens in main.py
        # prg.consist()
        # type.sk
        logging.info('generating Object.sk')
        self.gen_object_sk()
        
        logging.info('generating meta.sk')
        self.gen_meta_sk()
        
        # cls.sk
        logging.info('generating cls.sk')
        cls_sks = []
        clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self.prg)
        for cls in clss:
            cls_sk = self.gen_cls_sk(cls)
            if cls_sk: cls_sks.append(cls_sk)

        logging.info('generating main.sk')
        self.gen_main_sk(cls_sks)

    def gen_main_sk(self, cls_sks):
        # main.sk that imports all the other sketch files
        buf = cStringIO.StringIO()
      
        # --bnd-cbits: the number of bits for integer holes
        bits = max(5, int(math.ceil(math.log(len(self.mtds), 2))))
        buf.write("pragma options \"--bnd-cbits {}\";\n".format(bits))
        
        # --bnd-unroll-amnt: the unroll amount for loops
        unroll_amnt = None # use a default value if not set
        unroll_amnt = 35
        if unroll_amnt:
            buf.write("pragma options \"--bnd-unroll-amnt {}\";\n".format(35))
        
        # --bnd-inline-amnt: bounds inlining to n levels of recursion
        inline_amnt = None # use a default value if not set
        # setting it 1 means there is no recursion
        if inline_amnt:
            buf.write("pragma options \"--bnd-inline-amnt {}\";\n".format(inline_amnt))
            buf.write("pragma options \"--bnd-bound-mode CALLSITE\";\n")

        sks = ['meta.sk', 'Object.sk'] + cls_sks
        for sk in sks: buf.write("include \"{}\";\n".format(sk))

        with open(os.path.join(self.sk_dir, "main.sk"), 'w') as f:
            f.write(util.get_and_close(buf))
            
    def gen_meta_sk(self):
        buf = cStringIO.StringIO()
        buf.write("package meta;\n\n")
        buf.write("// distinct class IDs\n")
        for k,v in self.CLASS_NUMS.items():
            if k not in self.primitives:
                buf.write("int {k}() {{ return {v}; }}\n".format(**locals()))
        with open(os.path.join(self.sk_dir, "meta.sk"), 'w') as f:
            f.write(util.get_and_close(buf))

    def gen_object_sk(self):
        buf = cStringIO.StringIO()
        buf.write("package Object;\n\n")

        self.bases = util.rm_subs(self.clss)
        buf.write('\n'.join(filter(None, map(self.to_struct, self.bases))))
        with open(os.path.join(self.sk_dir, "Object.sk"), 'w') as f:
            f.write(util.get_and_close(buf))

    def gen_cls_sk(self, cls):
        mtds = utils.extract_nodes([MethodDeclaration], cls)
        cons = utils.extract_nodes([ConstructorDeclaration], cls)
        flds = utils.extract_nodes([FieldDeclaration], cls)
        s_flds = filter(td.isStatic, flds)

        if cls in self.bases: return None
        
        cname = cls.sanitize_ty(cls.name)
        buf = cStringIO.StringIO()
        buf.write("package {};\n\n".format(cname))

        for fld in ifilterfalse(td.isPrivate, s_flds):
            buf.write(self.tltr.trans_fld(fld))
            for v in fld.variables:
                typ = self.tltr.trans_ty(fld.typee)
                buf.write("{0} {1}_g() {{ return {1}; }}\n".format(typ, v.name))
                buf.write("void {1}_s({0} {1}_s) {{ {1} = {1}_s; }}\n".format(typ, v.name))
                buf.write('\n')

        if cls not in self.bases and cls.name != self.harness.parentNode.name and \
           not filter(lambda c: len(c.parameters) == 0, cons):
            buf.write("Object {0}_Object(Object self) {{\n"
                      "    return self;\n"
                      "}}\n\n".format(str(cls)))
                        
        for m in mtds + cons:
            if m.parentNode.interface: continue
            buf.write(self.to_func(m) + os.linesep)

        cls_sk = cname + ".sk"
        with open(os.path.join(self.sk_dir, cls_sk), 'w') as f:
            f.write(util.get_and_close(buf))
        return cls_sk

    def to_func(self, mtd):
        buf = cStringIO.StringIO()
        buf.write(self.tltr.trans(mtd))
        return util.get_and_close(buf)

    # only called on base classes. This seems to just be Object?
    def to_struct(self, cls):
        cname = cls.sanitize_ty(cls.name)
        if not cls.extendsList: cls = self.to_v_struct(cls)
              
        buf = cStringIO.StringIO()
        buf.write("struct " + cname + " {\n  int hash;\n  ")
              
        # to avoid static fields, which will be bound to a class-representing package
        i_flds = filter(lambda f: not td.isStatic(f), filter(lambda m: type(m) == FieldDeclaration, cls.members))
        buf.write('  '.join(map(self.tltr.trans_fld, i_flds)))
        buf.write("}\n")
        return util.get_and_close(buf)

    # from the given base class,
    # generate a virtual struct that encompasses all the class in the hierarchy
    def to_v_struct(self, cls):
        cls_d = {u'name':cls.name}
        cls_v = ClassOrInterfaceDeclaration(cls_d)
        # add __cid field
        fld_d = {u'variables':
                 {u'@e': [{u'@t': u'VariableDeclarator', u'id': {u'name': u'__cid'}}]},
                 u'@t': u'FieldDeclaration', u'type':
                 {u'@t': u'PrimitiveType', u'type':
                  {u'nameOfBoxedType': u'Integer', u'name': u'Int'}}}
        cls_v.members.append(FieldDeclaration(fld_d))
        cls_v.childrenNodes.append(FieldDeclaration(fld_d))
        def per_cls(cls):
            cname = cls.sanitize_ty(cls.name)
            if cname != cls_v.name: self.tltr.ty[cls.name] = cls_v.name
            flds = filter(lambda m: type(m) == FieldDeclaration, cls.members)
            def cp_fld(fld):
                for v in fld.variables:
                    fname = util.repr_fld(v, fld)
                    fld_v = cp.deepcopy(fld)
                    fld_v.variables = [cp.deepcopy(v)]
                    fld_v.variables[0].name = fname
                    fld_v.parentNode = cls_v
                    cls_v.members.append(fld_v)
                    cls_v.childrenNodes.append(fld_v)
                    fid = '.'.join([cname, v.name])
                    self.tltr.flds[fid] = fname # { ..., B.f2 : f2_B }
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
    def clss(self): return self._clss
    @clss.setter
    def clss(self, v): self._clss = v
    
    @property
    def mtds(self): return self._mtds
    @mtds.setter
    def mtds(self, v): self._mtds = v

    @property
    def harness(self): return self._harness
    @harness.setter
    def harness(self, v): self._harness = v

    @property
    def bases(self): return self._bases
    @bases.setter
    def bases(self, v): self._bases = v
    
    @property
    def primitives(self): return self._primitives
    @primitives.setter
    def primitives(self, v): self._primitives = v
    
    @property
    def CLASS_NUMS(self): return self._CLASS_NUMS
    @CLASS_NUMS.setter
    def CLASS_NUMS(self, v): self._CLASS_NUMS = v
    
    @property
    def MTD_NUMS(self): return self._MTD_NUMS
    @MTD_NUMS.setter
    def MTD_NUMS(self, v): self._MTD_NUMS = v
