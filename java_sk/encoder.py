import os
import util
import cStringIO
import math
import copy as cp
import logging

from . import builtins
from .translator import Translator

from ast.utils import utils

from ast.body.fielddeclaration import FieldDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.constructordeclaration import ConstructorDeclaration
from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

from ast.expr.generatorexpr import GeneratorExpr

from ast.type.referencetype import ReferenceType

class Encoder(object):
    def __init__(self, program, out_dir):
        # more globals to check out.
        self._prg = program
        self._prg.symtab.update(builtins)
        self._out_dir = out_dir
        self._sk_dir = ''
        self._mcls = None
        self._bases = []

        # populate global dict of types, classes and their ids
        self._clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self._prg)
        self._CLASS_NUMS = {u'Object':1}
        i = 2
        for c in self._clss:
            if str(c) not in self._CLASS_NUMS.keys():
                self._CLASS_NUMS[str(c)] = i
                i = i + 1
                self._CLASS_NUMS[u'int'] = i
                self._CLASS_NUMS[u'double'] = i+1

        self._mtds = utils.extract_nodes([MethodDeclaration], self._prg)
        self._cons = utils.extract_nodes([ConstructorDeclaration], self._prg)
        self._MTD_NUMS = {}
        i = 0
        for m in self._mtds+self._cons:
            if str(m) not in self._MTD_NUMS.keys():
                self._MTD_NUMS[m] = i
                i = i + 1

        # finds main/harness and populates some book keeping stuff
        self.main_cls()
        # create a translator object, this will do the JSketch -> Sketch
        self._tltr = Translator(cnums=self._CLASS_NUMS, mnums=self._MTD_NUMS, sk_dir=self.sk_dir)

    def find_main(self):
        mtds = []
        for c in self.clss:
            m = utils.extract_nodes([MethodDeclaration], c)
            mtds.extend(filter(lambda m: m.name == u'main', m))
            # do we care if main is static?
            # mtds.extend(filter(lambda m: td.isStatic(m) and m.name == u'main', m))
        lenn = len(mtds)
        if lenn > 1:
            raise Exception("multiple main()s", map(lambda m: str(utils.get_coid(m)), mtds))
        return mtds[0] if lenn == 1 else None

    def find_harness(self):
        # TODO: these can also be specified with annotations -- we don't support those yet
        mtds = filter(td.isHarness, self.mtds)
        return mtds[0] if mtds else None

    def main_cls(self):
        # get the main method and pull it's corresponding class out of the gsymtab.
        main = self.find_main()
        main = self.prg.gsymtab[main.atr] if main else None
        harness = self.find_harness()
        harness = self.prg.gsymtab[harness.atr] if harness else None
        if not main and not harness:
            raise Exception("No main(), @Harness, or harness found, None")

        self.mcls = main if main else harness
        self.demo_name = str(self.mcls)
        self.sk_dir = os.path.join(self.out_dir, '_'.join(["sk", self.demo_name]))

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

        logging.info('writing struct Object')
        self.print_obj_struct()

        logging.info('generating array.sk')
        self.gen_array_sk()

    def gen_array_sk(self):
        types = [u'bit', u'char', u'int', u'float', u'double', u'Object',]
        array_struct = 'struct Array_{0} {{\n  int length;\n  {0}[length] A;\n}}\n\n'
        with open(os.path.join(self.sk_dir, "array.sk"), 'w') as f:
            f.write("package array;\n\n")
            for t in types:
                f.write(array_struct.format(t))

    def print_obj_struct(self):
        buf = cStringIO.StringIO()

        # pretty print
        i_flds = filter(lambda m: type(m) == FieldDeclaration, self.tltr.obj_struct.members)
        flds = map(self.tltr.trans_fld, i_flds)
        lens = map(lambda f: len(f[0]), flds)
        m = max(lens) + 1
        buf.write("struct " + str(self.tltr.obj_struct) + " {\n")
        for f in flds:
            buf.write('  {} {}{}{};\n'.format(f[0],' '*(m-len(f[0])), f[1], f[2]))
        buf.write("}\n")
        with open(os.path.join(self.sk_dir, "Object.sk"), 'a') as f:
            f.write(util.get_and_close(buf))

    def gen_main_sk(self, cls_sks):
        # main.sk that imports all the other sketch files
        buf = cStringIO.StringIO()

        # --bnd-cbits: the number of bits for integer holes
        bits = max(5, int(math.ceil(math.log(len(self.mtds), 2))))
        buf.write('pragma options "--bnd-cbits {}";\n'.format(bits))

        # --bnd-unroll-amnt: the unroll amount for loops
        unroll_amnt = 35
        if unroll_amnt:
            buf.write('pragma options "--bnd-unroll-amnt {}";\n'.format(35))

        # --bnd-inline-amnt: bounds inlining to n levels of recursion
        inline_amnt = None # use a default value if not set
        # setting it 1 means there is no recursion
        if inline_amnt:
            buf.write('pragma options "--bnd-inline-amnt {}";\n'.format(inline_amnt))
            buf.write('pragma options "--bnd-bound-mode CALLSITE";\n')

        buf.write('pragma options "--fe-fpencoding AS_FIXPOINT";\n')

        sks = ['meta.sk', 'Object.sk', 'array.sk'] + cls_sks
        for sk in sks: buf.write("include \"{}\";\n".format(sk))

        with open(os.path.join(self.sk_dir, "main.sk"), 'w') as f:
            f.write(util.get_and_close(buf))

    def gen_meta_sk(self):
        buf = cStringIO.StringIO()
        buf.write("package meta;\n\n")

        buf.write("// distinct class IDs\n")
        items = sorted(self.CLASS_NUMS.items())
        lens = map(lambda i: len(i[0]), items)
        m = max(lens)
        for k,v in items:
            if k not in utils.narrow:
                buf.write("int {k}() {s} {{ return {v}; }}\n".format(k=k, v=v, s=' '*(m-len(k))))
        buf.write('\n// Uninterpreted functions\n')
        with open(os.path.join(self.sk_dir, "meta.sk"), 'w') as f:
            f.write(util.get_and_close(buf))

    def gen_object_sk(self):
        buf = cStringIO.StringIO()
        buf.write("package Object;\n\n")

        self.bases = util.rm_subs(self.clss)
        filter(None, map(self.to_struct, self.bases))
        buf.write('Object Object_Object(Object self){\n return self;\n}\n\n')
        with open(os.path.join(self.sk_dir, "Object.sk"), 'w') as f:
            f.write(util.get_and_close(buf))

    def gen_cls_sk(self, cls):
        # if cls in self.bases: return None

        mtds = utils.extract_nodes([MethodDeclaration], cls, recurse=False)
        cons = utils.extract_nodes([ConstructorDeclaration], cls, recurse=False)
        flds = utils.extract_nodes([FieldDeclaration], cls, recurse=False)
        s_flds = filter(td.isStatic, flds)

        cname = str(cls)
        buf = cStringIO.StringIO()
        buf.write("package {};\n\n".format(cname))

        for fld in s_flds:
            f = self.tltr.trans_fld(fld)
            buf.write('{} {}{};\n'.format(f[0], f[1], f[2]))
            if cls == self.mcls and fld.variable.init and type(fld.variable.init) == GeneratorExpr: continue
            typ = self.tltr.trans_ty(fld.typee)
            if isinstance(fld.typee, ReferenceType) and fld.typee.arrayCount > 0:
                typ = 'Array_{}'.format(typ)
            buf.write("{0} {1}_g() {{ return {1}; }}\n".format(typ, fld.name))
            buf.write("void {1}_s({0} {1}_s) {{ {1} = {1}_s; }}\n".format(typ, fld.name))
            buf.write('\n')

        etypes = cls.enclosing_types()
        if etypes: buf.write('Object self{};\n\n'.format(len(etypes)-1))
        # not a base class, not the harness class, and doesn't override the base constructor
        # if cls not in self.bases and str(cls) != str(self.mcls) and \
        if str(cls) != str(self.mcls) and \
           not filter(lambda c: len(c.parameters) == 0, cons):
            # these represent this$N (inner classes)
            if etypes:
                i = len(etypes)-1
                init = 'self{0} = self_{0};'.format(i)
                buf.write("Object {0}_{0}_{1}(Object self, Object self_{2}) {{\n"
                          "    {3}\n"
                          "    return self;\n"
                          "}}\n\n".format(str(cls), str(etypes[-1]), i, init))
            else:
                buf.write("Object {0}_{0}(Object self) {{\n"
                          "    return self;\n"
                          "}}\n\n".format(str(cls)))

        for m in cons + mtds:
            if hasattr(m, 'interface') and m.parentNode.interface: continue
            buf.write(self.to_func(m) + os.linesep)

        cls_sk = cname + ".sk"
        with open(os.path.join(self.sk_dir, cls_sk), 'w') as f:
            f.write(util.get_and_close(buf))
        return cls_sk

    def to_func(self, mtd):
        buf = cStringIO.StringIO()
        buf.write(self.tltr.trans(mtd))
        if self.tltr.post_mtds:
            buf.write(self.tltr.post_mtds)
            self.tltr.post_mtds = ''
        return util.get_and_close(buf)

    # only called on base classes. This seems to just be Object?
    def to_struct(self, cls):
        if not cls.extendsList: self.tltr.obj_struct = self.to_v_struct(cls)
 
    # from the given base class,
    # generate a virtual struct that encompasses all the class in the hierarchy
    def to_v_struct(self, cls):
        cls_d = {u'name':str(cls)}
        cls_v = ClassOrInterfaceDeclaration(cls_d)
        # add __cid field
        fld_d = {u'variables':
                 {u'@e': [{u'@t': u'VariableDeclarator', u'id': {u'name': u'__cid'}}]},
                 u'@t': u'FieldDeclaration', u'type':
                 {u'@t': u'PrimitiveType', u'type':
                  {u'nameOfBoxedType': u'Integer', u'name': u'Int'}}}
        fd = FieldDeclaration(fld_d)
        cls_v.members.append(fd)
        cls_v.childrenNodes.append(fd)
        def per_cls(cls):
            cname = str(cls)
            if cname != str(cls_v): self.tltr.ty[str(cls)] = str(cls_v)
            flds = filter(lambda m: type(m) == FieldDeclaration, cls.members)
            def cp_fld(fld):
                # fld_v = cp.deepcopy(fld)
                fld_v = cp.copy(fld)
                # fld_v.variable = cp.copy(fld.variable)
                fld_v.parentNode = cls
                cls_v.members.append(fld_v)
                cls_v.childrenNodes.append(fld_v)
            map(cp_fld, filter(lambda f: not td.isStatic(f), flds))
        map(per_cls, utils.all_subClasses(cls))
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
    def bases(self): return self._bases
    @bases.setter
    def bases(self, v): self._bases = v

    @property
    def out_dir(self): return self._out_dir
    @out_dir.setter
    def out_dir(self, v): self._out_dir = v

    @property
    def sk_dir(self): return self._sk_dir
    @sk_dir.setter
    def sk_dir(self, v): self._sk_dir = v

    @property
    def CLASS_NUMS(self): return self._CLASS_NUMS
    @CLASS_NUMS.setter
    def CLASS_NUMS(self, v): self._CLASS_NUMS = v

    @property
    def MTD_NUMS(self): return self._MTD_NUMS
    @MTD_NUMS.setter
    def MTD_NUMS(self, v): self._MTD_NUMS = v
