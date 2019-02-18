from __future__ import print_function

from __future__ import absolute_import
try:
    import cStringIO
except: # so sue me.
    import io as cStringIO
import math
import os
import copy as cp
import logging

from . import util

from functools import partial

from . import builtins
# from .translator import TranslatorWrap, TranslatorNoWrap
from .translator import Translator

from ast.utils import utils

from ast.body.fielddeclaration import FieldDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.parameter import Parameter
from ast.body.constructordeclaration import ConstructorDeclaration
from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.xform import Xform
from ast.body.axiomdeclaration import AxiomDeclaration
from ast.body.variabledeclarator import VariableDeclarator
from ast.body.axiomparameter import AxiomParameter

from ast.stmt.returnstmt import ReturnStmt

from ast.expr.generatorexpr import GeneratorExpr
from ast.expr.methodcallexpr import MethodCallExpr
from ast.expr.literalexpr import LiteralExpr
from ast.expr.nameexpr import NameExpr
from ast.expr.conditionalexpr import ConditionalExpr
from ast.expr.binaryexpr import BinaryExpr

from ast.type.referencetype import ReferenceType
from ast.type.primitivetype import PrimitiveType
from ast.type.classorinterfacetype import ClassOrInterfaceType

class Encoder(object):
    def __init__(self, program, out_dir, fs):
        # more globals to check out.
        self._prg = program
        self._prg.symtab.update(builtins)
        self._out_dir = out_dir
        self._fs = fs
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

        clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self.prg)
        # is_ax_cls = [c._axiom for c in clss]
        is_ax_cls = True if len([c for c in clss if c.box]) > 0 else False
        ax_clss = [c for c in clss if c.axiom]
        
        self.is_ax_cls = is_ax_cls
        self.ax_clss = ax_clss
        
        # create a translator object, this will do the JSketch -> Sketch
        self._tltr = Translator(cnums=self._CLASS_NUMS, mnums=self._MTD_NUMS, sk_dir=self._sk_dir, fs=self._fs, is_ax_cls=is_ax_cls, ax_clss=ax_clss)
        
        # if is_ax_cls:
        #     # create a translator object, this will do the JSketch -> Sketch
        #     self._tltr = TranslatorWrap(cnums=self._CLASS_NUMS, mnums=self._MTD_NUMS, sk_dir=self._sk_dir, fs=self._fs)
        # else:
        #     # create a translator object, this will do the JSketch -> Sketch
        #     self._tltr = TranslatorNoWrap(cnums=self._CLASS_NUMS, mnums=self._MTD_NUMS, sk_dir=self._sk_dir, fs=self._fs)

    def find_main(self):
        mtds = []
        for c in self.clss:
            m = utils.extract_nodes([MethodDeclaration], c)
            mtds.extend([m for m in m if m.name == u'main'])
            # do we care if main is static?
            # mtds.extend(filter(lambda m: td.isStatic(m) and m.name == u'main', m))
        lenn = len(mtds)
        if lenn > 1:
            raise Exception("multiple main()s", [str(utils.get_coid(m)) for m in mtds])
        return mtds[0] if lenn == 1 else None

    def find_harness(self):
        # TODO: these can also be specified with annotations -- we don't support those yet
        mtds = [m for m in self.mtds if td.isHarness(m)]
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

        clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self.prg)
        is_ax_cls = any([c._axiom for c in clss])
        
        # consist builds up some class hierarchies which happens in main.py
        # prg.consist()
        # type.sk
        logging.info('generating Object.sk')
        self.gen_object_sk(is_ax_cls)

        logging.info('generating meta.sk')
        self.gen_meta_sk(is_ax_cls)

        # cls.sk
        logging.info('generating cls.sk')
        cls_sks = []
        for cls in clss:
            cls_sk = self.gen_cls_sk(cls, is_ax_cls)
            if cls_sk: cls_sks.append(cls_sk)

        logging.info('generating main.sk')
        self.gen_main_sk(cls_sks)

        logging.info('writing struct Object')
        # self.print_obj_struct(is_ax_cls)
        self.print_obj_struct(self.is_ax_cls)

        logging.info('generating array.sk')
        # self.gen_array_sk(is_ax_cls)
        self.gen_array_sk(self.is_ax_cls)

    def gen_array_sk(self, is_ax_cls):
        types = [u'bit', u'char', u'int', u'float', u'double', u'Object',]
        array_struct = 'struct Array_{0} {{\n  int length;\n  {0}[length] A;\n}}\n\n'
        array_wrapper = ''
        if is_ax_cls:
            array_struct = 'struct Array_{0} {{\n  Object length;\n  {0}[length._int] A;\n}}\n\n'
            array_wrapper = 'Object Wrap_Array_{0}(Array_{0} arr) {{\n  return new Object(__cid=Array(), _array_{1}=arr); \n}}\n\n'
        with open(os.path.join(self.sk_dir, "array.sk"), 'w') as f:
            f.write("package array;\n\n")
            for t in types:
                f.write(array_struct.format(t))
            if is_ax_cls:
                for t in types:
                    f.write(array_wrapper.format(t, t.lower())) 

    def print_obj_struct(self, is_ax_cls):
        buf = cStringIO.StringIO()

        if self.tltr.obj_struct:            
            # pretty print
            i_flds = [m for m in self.tltr.obj_struct.members if type(m) == FieldDeclaration]
            flds = [self.tltr.trans_fld(m) for m in i_flds]
            lens = [len(f[0]) for f in flds]
            m = max(lens) + 1
            buf.write("struct " + str(self.tltr.obj_struct) + " {\n")
            if is_ax_cls:
                for i in range(0, len(flds)):
                    f = flds[i]
                    typ = f[0]
                    if isinstance(i_flds[i].typee, PrimitiveType) and not(f[1] == '__cid' or f[1] == '_int' or f[1] == '_bit' or f[1] == '_double' or f[1] == '_float' or f[1] == '_char'):
                        typ = u'Object'
                    buf.write('  {} {}{}{};\n'.format(typ,' '*(m-len(typ)), f[1], f[2]))
            else:
                for i in range(0, len(flds)):                
                # for f in flds:
                    f = flds[i]
                    typ = f[0]
                    i_f = i_flds[i]
                    if isinstance(i_f.typee, ReferenceType):
                        if isinstance(i_f.typee.typee, ClassOrInterfaceType):
                            clss = utils.extract_nodes([ClassOrInterfaceDeclaration], self.prg)
                            clss = [a.name for a in [c for c in clss if c._axiom]]
                            
                            if i_f.typee.typee.name in clss:
                                typ = u'Object'
                                
                    buf.write('  {} {}{}{};\n'.format(typ,' '*(m-len(typ)), f[1], f[2]))
            buf.write("}\n")
        else:
            if is_ax_cls:
                buf.write("struct Object {\n")
                buf.write("  int __cid;\n")
                buf.write("  Array_bit _array_bit;\n")            
                buf.write("  Array_char _array_char;\n")
                buf.write("  Array_int _array_int;\n")
                buf.write("  Array_float _array_float;\n")
                buf.write("  Array_double _array_double;\n")
                buf.write("  Array_Object _array_object;\n")
                buf.write("  int _int;\n")
                buf.write("  bit _bit;\n")
                buf.write("  double _double;\n")
                buf.write("  char _char;\n")
                buf.write("  float _float;\n")            
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

    def gen_meta_sk(self, is_ax_cls):
        buf = cStringIO.StringIO()
        buf.write("package meta;\n\n")

        buf.write("// distinct class IDs\n")
        items = sorted(self.CLASS_NUMS.items())
        lens = [len(i[0]) for i in items]
        m = max(lens)
        for k,v in items:
            if k not in utils.narrow:
                buf.write("int {k}() {s} {{ return {v}; }}\n".format(k=k, v=v, s=' '*(m-len(k))))

        if is_ax_cls:
            buf.write("int {k}(){s}{{ return {v}; }}\n".format(k="Array", v="-1", s=' '*(m-len(k))))        
            buf.write("int {k}(){s} {{ return {v}; }}\n".format(k="_int", v="-2", s=' '*(m-len(k))))        
            buf.write("int {k}(){s}{{ return {v}; }}\n".format(k="_char", v="-3", s=' '*(m-len(k))))        
            buf.write("int {k}(){s} {{ return {v}; }}\n".format(k="_bit", v="-4", s=' '*(m-len(k))))        
            buf.write("int {k}(){s}{{ return {v}; }}\n".format(k="_float", v="-5", s=' '*(m-len(k)-1)))        
            buf.write("int {k}(){s}{{ return {v}; }}\n".format(k="_double", v="-6", s=' '*(m-len(k)-2)))        
            
        buf.write('\n// Uninterpreted functions\n')
        with open(os.path.join(self.sk_dir, "meta.sk"), 'w') as f:
            f.write(util.get_and_close(buf))

    def gen_object_sk(self, is_ax_cls):
        buf = cStringIO.StringIO()
        buf.write("package Object;\n\n")

        self.bases = util.rm_subs(self.clss)
        for b in self.bases:
            self.to_struct(is_ax_cls, b)
        buf.write('Object Object_Object(Object self){\n return self;\n}\n\n')
        with open(os.path.join(self.sk_dir, "Object.sk"), 'w') as f:
            f.write(util.get_and_close(buf))

    def gen_cls_sk(self, cls, is_ax_cls):
        if cls.axiom:
            if is_ax_cls:
                return self.gen_axiom_cls_sk(cls, self.is_ax_cls)
            
        mtds = utils.extract_nodes([MethodDeclaration], cls, recurse=False)
        cons = utils.extract_nodes([ConstructorDeclaration], cls, recurse=False)
        flds = utils.extract_nodes([FieldDeclaration], cls, recurse=False)
        s_flds = [f for f in flds if td.isStatic(f)]

        cname = str(cls)
        buf = cStringIO.StringIO()
        buf.write("package {};\n\n".format(cname))

        for fld in s_flds:
            f = self.tltr.trans_fld(fld)
            typ = f[0]
            if self.is_ax_cls:
                typ = u'Object'
            buf.write('{} {}{};\n'.format(typ, f[1], f[2]))
            if cls == self.mcls and fld.variable.init and type(fld.variable.init) == GeneratorExpr: continue
            if not is_ax_cls:
                typ = self.tltr.trans_ty(fld.typee)
                if isinstance(fld.typee, ReferenceType) and fld.typee.arrayCount > 0:
                    if is_ax_cls:
                        typ = 'Object'
                    else:
                        typ = 'Array_{}'.format(typ)
            buf.write("{0} {1}_g() {{ return {1}; }}\n".format(typ, fld.name))
            buf.write("void {1}_s({0} {1}_s) {{ {1} = {1}_s; }}\n".format(typ, fld.name))
            buf.write('\n')

        etypes = cls.enclosing_types()
        if etypes: buf.write('Object self{};\n\n'.format(len(etypes)-1))
        # not a base class, not the harness class, and doesn't override the base constructor
        # if cls not in self.bases and str(cls) != str(self.mcls) and \
        if not [c for c in cons if len(c.parameters) == 0]:
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

    def gen_axiom_cls_sk(self, cls, is_ax_cls):
        cname = str(cls)

        ax_mtds = utils.extract_nodes([AxiomDeclaration], cls, recurse=False)

        def gen_adt_constructor(mtd):
            name = mtd.name
            mtd_param_typs = mtd.param_typs()            
            # if mtd.constructor:
            #     name += u'_Object'
            for t in mtd_param_typs:
                typ = self.tltr.trans_ty(t)
                if typ == u'Object' or str(t) == u'byte': typ = str(t)
                # if typ in map(str, cls.typeParameters):
                #     typ = u'Object'
                name += '_'+typ
                # if mtd.constructor:
                #     name += '_'+typ
            name = name.capitalize()
            c = '    {}{} {{ '.format(name, ' '*(max_len+1-len(mtd.name)))
            if not mtd.default and not mtd.constructor:
                c += '{} self'.format(cls.name)
                if not mtd.parameters:
                    c += '; '
            if mtd.parameters and not mtd.constructor: c += '; '
            for p,t,n in zip(mtd.parameters, mtd.param_typs(), mtd.param_names()):
                typ = u'Object'
                if not is_ax_cls:
                    typ = self.tltr.trans_ty(t)
                    if isinstance(t, ReferenceType) and t.arrayCount > 0:
                        typ = "Array_"+typ
                    if isinstance(t, ReferenceType) and isinstance(t.typee, ClassOrInterfaceType) and str(t.typee) in [c.name for c in self.ax_clss] and not self.is_ax_cls:
                        typ = u'Object'
                        
                # if p.typee.name in p.symtab:
                #     typ_cls = p.symtab[p.typee.name]
                #     if isinstance(typ_cls, ClassOrInterfaceDeclaration) and typ_cls.axiom:
                #         typ = u'Object'

                c += '{} {}; '.format(typ, n)
            c += '}\n'
            return c
        # Generates Object Wrapper Functions for ADT Constructors
        def gen_obj_constructor(mtd):
            mtd_param_typs = mtd.param_typs()
            name = mtd.name
            mtd_name2 = mtd.name
            if mtd.constructor:
                name += u'_Object'
            for t in mtd_param_typs:
                typ = self.tltr.trans_ty(t)
                if typ == u'Object' or str(t) == u'byte': typ = str(t)
                # if typ in map(str, cls.typeParameters):
                #     typ = u'Object'
                mtd_name2 += '_'+typ
                if mtd.constructor:
                    name += '_'+typ
            ptyps = []
            ptyps_name = []
            for t in mtd_param_typs:
                if isinstance(t, ReferenceType) and isinstance(t.typee, ClassOrInterfaceType) and str(t.typee) in [c.name for c in self.ax_clss] and not self.is_ax_cls:
                    typ = u'Object'
                else:
                    typ = self.tltr.trans_ty(t)
                ptyps.append(typ)
                if typ == u'Object' or str(t) == u'byte': typ = str(t)
                ptyps_name.append(typ)
            pnms = [str(p) for p in mtd.param_names()]
            # (ptyps, pnms) = (map(lambda t: self.tltr.trans_ty(t), mtd.param_typs()), map(str, mtd.param_names()))
            # ptyps_name = cp.deepcopy(ptyps)
            if is_ax_cls:
                for i in range(0, len(ptyps)):
                    ptyps[i] = u'Object'
            #     ptyp = ptyps[i]
            #     p = mtd.parameters[i]
            #     if p.typee.name in p.symtab:
            #         typ_cls = p.symtab[p.typee.name]
            #         if isinstance(typ_cls, ClassOrInterfaceDeclaration) and typ_cls.axiom:
            #             ptyps[i] = u'Object'
            if not is_ax_cls:
                for i in range(0,len(ptyps)):
                    if isinstance(mtd_param_typs[i], ReferenceType):
                        if mtd_param_typs[i].arrayCount > 0:
                            ptyps[i] = "Array_"+ptyps[i]
            params = ', '.join([' '.join(p) for p in zip(ptyps, pnms)])
            c = 'Object '
            if (not is_ax_cls and mtd_name2.split('_')[0] in [x.name for x in ax_mtds]) and not mtd.boxedRet:
                # c = str(mtd.typee) + u' '
                c = self.tltr.trans_ty(mtd.typee) + u' '
            if isinstance(mtd.typee, ReferenceType) and mtd.typee.arrayCount > 0 and (not is_ax_cls and not mtd.boxedRet and not mtd.is_bang):
                c = u'Array_'+self.tltr.trans_ty(mtd.typee) + u' '
                
            if name == cname.lower():
                mtd_name = cname + "_" + cname
            elif len(name) > 6 and name[len(name)-6:] == "_Empty" and name[0:len(name)-6] == cname.lower():
                mtd_name = cname + "_" + cname                
            else:
                mtd_name = name #str(name.lower())
            typ_params = '_'.join(ptyps_name)
            if not mtd.default and not mtd.constructor:
                mtd_name += '_Object'
                if mtd.parameters:
                    mtd_name += '_{}'.format(typ_params)

            c += '{}'.format(mtd_name)
            c += '('
            if not mtd.default:
                if not mtd.constructor:
                    c += 'Object self'
                    if mtd.parameters: c += ', '
                c += '{}) {{\n    '.format(params)
            else:
                c += ') {\n    '
            if mtd_name2.split('_')[0] not in [x.name for x in ax_mtds]:
                # THERE MUST BE A BETTER WAY TO DETECT BANG TYPE METHODS
                if mtd_name2.split('_')[0].endswith('b'):
                    c += 'self._{0}=new {1}('.format(cls.name.lower(), mtd_name2.capitalize())
                    if not mtd.default and not mtd.constructor:
                        c += 'self=self._{}'.format(cls.name.lower())
                    for i in range(0, len(pnms)):
                        n = pnms[i]
                        if i == 0 and mtd.constructor:
                            c += '{0}={0}'.format(n)
                        else:
                            c += ', {0}={0}'.format(n)
                    c += ');\n'
                    c +='return self;\n}\n\n'
                else:
                    c += 'return new Object(__cid={}(), _{}=new {}('.format(cls.name, cls.name.lower(), mtd_name2.capitalize())
                    if not mtd.default and not mtd.constructor:
                        c += 'self=self._{}'.format(cls.name.lower())
                    for i in range(0, len(pnms)):
                        n = pnms[i]
                        if i == 0 and mtd.constructor:
                            c += '{0}={0}'.format(n)
                        else:
                            c += ', {0}={0}'.format(n)
                    c += '));\n}\n\n'
            else:
                mname = mtd_name2.split('_')[0]
                ptypes = '_'.join(mtd_name2.split('_')[1:])
                c += 'return xform_{}_{}'.format(mname, cls.name)
                if ptypes != '':
                    c +='_{}'.format(ptypes)
                # c += '(self._{}'.format(cls.name.lower())
                c += '(self'
                if not is_ax_cls and not mtd.boxedRet:
                    c += u'._'+str(cls).lower()
                if pnms != []:
                    c += ', {}'.format(','.join(pnms))
                c += ');\n}\n\n'
                
            return c

        buf = cStringIO.StringIO()
        buf.write("package {};\n\n".format(cname))

        # Creates list of adt "functions" (i.e. constructors from top of java file)
        #   including bang functions
        mtds = utils.extract_nodes([MethodDeclaration], cls, recurse=False)
        adt_mtds = [m for m in mtds if m.adt]
        non_adt_mtds = [m for m in mtds if not m.adt]

        # Write all non axiom / adt functions to file (like static functions)
        for m in non_adt_mtds:
            buf.write(self.to_func(m) + os.linesep)        
        
        # add bang functions for non-pure methods
        for (m,i) in zip(adt_mtds, xrange(len(adt_mtds))):
            if not m.pure:
                if not m.constructor:
                    mtd = cp.copy(m)
                    mtd.name = m.name + 'b'
                    mtd.pure = True
                    mtd.is_bang = True
                    adt_mtds.insert(i+1, mtd)
                # else:
                #     m.name += 'b'
                #     m.pure = False

        # add default constructor if one isn't provided
        #   i.e. user didn't write constructor at top of Java file
        # default = filter(lambda m: cname == m.name, adt_mtds)
        default = None
        if not default:
            default_name = cname.lower();
            if cname == cname.lower().capitalize():
                default_name += "_Empty"
            m = MethodDeclaration({u'@t':u'MethodDeclaration', u'name':default_name,
                                   u'type':{u'@t':u'ClassOrInterfaceType',u'name':u'Object',},},)
            # set this to pure so we don't generate a bang constructor and default...
            # so we know it's default
            m.pure = True
            m.default = True
            m.add_parent_post(cls)
            adt_mtds = [m] + adt_mtds                                

        # I like to format
        max_len = max([len(m.name) for m in adt_mtds])
        
        # Create ADT constructors for all methods and wraps them in ADT struct
        #  Also create a dictionary for object constructors for symbol table reference
        cons = [gen_obj_constructor(m) for m in adt_mtds]
        adt_cons = [gen_adt_constructor(m) for m in adt_mtds]
        adt = 'adt {} {{\n{}}}\n\n{}'.format(cname, ''.join(adt_cons), ''.join(cons))
        buf.write(adt)

        # updates n's symbol table to include parents symbol table items
        def cpy_sym(n, *args):
            if n.parentNode: n.symtab = dict(n.parentNode.symtab.items() +
                                             n.symtab.items())
        
        # Iterates through ADT constructors
        #   Creates a dictionary of xforms using constructor names
        #   Keys are the xform name (of the form "xform_"+adt_name)
        #   Values are MethodDeclarations with lots of ugly looking formatting 
        xforms = {}
        for a in adt_mtds:
            xnm = u'xform_{}'.format(a.name_no_nested(False))
            x = Xform.gen_xform(a.get_coid(), xnm, adt_mtds,
                                [{u'@t':u'Parameter',
                                  u'type':{u'@t':u'ClassOrInterfaceType',u'name':cname,},
                                  u'id':{u'name':u'selff',},},], is_ax_cls, a)

            # _self = Parameter({u'id':{u'name':u'selff'},
            #                        u'type':{u'@t':u'ClassOrInterfaceType', u'name':cname}},)
            _self = Parameter({u'id':{u'name':u'selff'},
                                   u'type':{u'@t': u'ReferenceType', u'type': {u'@t':u'ClassOrInterfaceType', u'name':cname},},},)
            x.childrenNodes.append(_self)
            x.parameters = [_self] + [cp.copy(p) for p in a.parameters]
                
            x.adtName = str(a)
            x.add_parent_post(cls, True)
            x.boxedRet = a.boxedRet
            xforms[xnm] = x

        # Applies cpy_sym to all children of this class and all children of those
        #    Updates symbol table of each of these children to include parent's
        #    symbol table
        for c in cls.childrenNodes:
           utils.walk(cpy_sym, c)
            
        # # create xform dispatch method
        # #    i.e. calls the right xform depending on type of ADT
        # dispatch = Xform.gen_xform(cls, u'xform', adt_mtds,
        #                            [{u'@t':u'Parameter',
        #                              u'type':{u'@t':u'ClassOrInterfaceType',u'name':cname},
        #                              u'id':{u'name':u'self',},},],)
        # dispatch.add_parent_post(cls)

        # # Builds up return and body of dispatch function
        # for a in adt_mtds:
        #     xnm = 'xform_{}'.format(a.name_no_nested(False))
        #     xf = xforms[xnm]
        #     ret = ReturnStmt({u'expr':{u'@t':u'MethodCallExpr',
        #                                u'name':xnm,u'type':{u'@t':u'ClassOrInterfaceType',
        #                                                     u'name':'Object',},
        #                                u'args':[],},},)

        #     for p in xf.parameters:
        #         if p.idd.name == 'self' and a.constructor:
        #             v = LiteralExpr({u'name':u'{}'.format(p.idd.name),},)
        #         else:
        #             if not a.default:
        #                 v = LiteralExpr({u'name':u'self.{}'.format(p.idd.name),},)
        #             else:
        #                 v = LiteralExpr({u'name':u'{}'.format(p.idd.name),},)
        #         v.typee = p.typee
        #         ret.expr.childrenNodes.append(v)
        #         ret.expr.args.append(v)
                
        #     body = dispatch.get_xform()
        #     # body.add_body([a.name.capitalize()], [ret], adt_mtds)
        #     body.add_body([a.name_no_nested(False).capitalize()], [ret], adt_mtds)

        # Writes dispatch function
        # buf.write(self.tltr.trans(dispatch))

        # Gets all the axiom declarations 
        ax_mtds = utils.extract_nodes([AxiomDeclaration], cls, recurse=False)

        # for a in adt_mtds:
        #     print("HERE22: "+str(a.name_no_nested(False)))

        # def set_param_names(self, xparams, params, mtd, xf, depth):
        #     for (xp, ap) in zip(xparams, params):
        #         name = mtd.name
        #         if name == u'selff': name = u'self'
        #         old_name = '#'+ap.name+"_axparam#"
        #         if not old_name in xf.symtab: 
        #             xf.symtab[old_name] = ((name+u'_')*(depth-1))+name+u'.'+xp.name

        # def set_param_names2(self, param, xparam, depth, cls):            
        #     if param.method and param.method.parameters:
        #         name_with_args = param.method.name
        #         if len(param.method.parameters) > 0:
        #             nested_params = param.method.parameters
        #             # Checking for constructor w/ no args
        #             if name_with_args != cls.name:
        #                 nested_params = nested_params[1:]
        #             for param2 in nested_params:
        #                 t = param2.typee
        #                 typ = self.tltr.trans_ty(t)
        #                 if typ == u'Object' or str(t) == u'byte': typ = str(t)
        #                 name_with_args += '_'+typ
        #         if name_with_args == cls.name and len(param.method.parameters) == 0:
        #             name_with_args += '_Empty'

        #         xf = filter(lambda m: name_with_args.startswith(m.name), adt_mtds)[0]
        #             params2 = param.method.parameters[1:]
        #             if xf2.constructor:
        #                 params2 = param.method.parameters
        #             for (xp, ap) in zip(xf2.parameters, params2):
        #                 name = xparam.name
        #                 if name == 'selff': name = u'self'
        #             if not xf2.constructor:
        #                 ap_name = param.method.parameters[0].name
        #                 name = u'self' #ap_name
        #                 xf.symtab['#'+ap_name+"_axparam#"] = ((name+u'_')*(depth-1))+name+u'.self'
        #             param = param.method.parameters[0]
        #             depth += 1
                
        def set_param_names(a, xf, adt_mtds, depth, xf_sym, name, xnames):
            xf_params = xf.parameters
            if len(xf_params) == len(a.parameters)-1:
                first_param = LiteralExpr({u'name':u'selff',},)
                xf_params = [first_param]+xf_params
            for (param, xparam) in zip(a.parameters, xf_params):
                if not param.method or not param.method.parameters:
                    if name == 'selff': name = u'self'
                    old_name = '#'+param.name+"_axparam#"
                    if not old_name in xf_sym.symtab:
                        xname = xparam.name
                        if xname == u'selff': xname = u'self'
                        if depth != 0:
                            if depth == 1 and name == u'self':
                                xname = name+u'.'+xname
                            else:
                                if name == u'self':
                                    xname = ((name+u'_')*(depth-1))+name+u'.'+xname
                                else:
                                    xname = ((name+u'_')*(depth))+name+u'.'+xname
                                    
                                poss_names = [n for n in xnames if len(n.split('_')) == depth+1]
                                if len(poss_names) > 0:
                                    new_xname = poss_names[0].split('.')[0]
                                    xname = new_xname+u'.'+xname.split('.')[-1]
                        xf_sym.symtab[old_name] = xname
                        xnames.append(xname)
                else:
                    xf2 = [m for m in adt_mtds if param.method.name == m.name.split('_')[0]][0]
                    if depth == 0:
                        set_param_names(param.method, xf2, adt_mtds, depth+1, xf_sym, xparam.name, xnames)
                    else:
                        if xparam.name != u'selff':
                            xnames.append(xparam.name+(u'_'+xparam.name)*(depth+1))
                        set_param_names(param.method, xf2, adt_mtds, depth+1, xf_sym, name, xnames)

        for a in ax_mtds:
            a.name = a.name_no_nested(False, [])            
            xnm = 'xform_{}'.format(a.name)
            xf = xforms[xnm]
            xf.name = 'xform_{}'.format(a.name)
            
            set_param_names(a, xf, adt_mtds, 0, xf, u'self', [])            
            # index = 0
            # for (param,xparam) in zip(a.parameters, xf.parameters):
            #     xf2 = []
            #     # if param.method:
            #     #     if param.method.parameters:
            #     depth = 1 if index == 0 else 2
            #     index += 1
            #     while param.method and param.method.parameters:
            #         name_with_args = param.method.name
            #         # name_with_args += '_Object_Object'
            #         if len(param.method.parameters) > 0:
            #             params2 = param.method.parameters
            #             if name_with_args != cls.name:
            #                 params2 = params2[1:]
            #             for param2 in params2:
            #                 # name_with_args += '_'+str(param2.typee)
            #                 t = param2.typee
            #                 typ = self.tltr.trans_ty(t)
            #                 if typ == u'Object' or str(t) == u'byte': typ = str(t)
            #                 name_with_args += '_'+typ
            #         if name_with_args == cls.name and len(param.method.parameters) == 0:
            #             name_with_args += '_Empty'
            #         # xf2 = filter(lambda m: m.name == name_with_args, adt_mtds)
            #         xf2 = filter(lambda m: name_with_args.startswith(m.name), adt_mtds)
            #         xf2 = xf2[0]
            #         params2 = param.method.parameters[1:]
            #         if xf2.constructor:
            #             params2 = param.method.parameters
            #         for (xp, ap) in zip(xf2.parameters, params2):
            #             name = xparam.name
            #             if name == 'selff': name = u'self'
            #             old_name = '#'+ap.name+"_axparam#"
            #             if not old_name in xf.symtab: 
            #                 xf.symtab[old_name] = ((name+u'_')*(depth-1))+name+u'.'+xp.name
            #         if not xf2.constructor:
            #             ap_name = param.method.parameters[0].name
            #             name = u'self' #ap_name
            #             xf.symtab['#'+ap_name+"_axparam#"] = ((name+u'_')*(depth-1))+name+u'.self'
            #         param = param.method.parameters[0]
            #         depth += 1
                
        # populate individual xforms with axioms
        #   
        for a in ax_mtds:
            xnm = 'xform_{}'.format(a.name)
            xf = xforms[xnm]
            xf.name = 'xform_{}'.format(a.name)
                
            # rename xf parameters to correspond to axiom declaration, not adt
            #    (i.e. parameters representing xforms must access their fields through
            #    correct names, some parameters must be renamed
            for (xp,ap) in zip(xf.parameters, a.parameters):
                # Filters out first argument (i.e. the bang ADT structure)
                if ap.idd:
                    xp_name = xp.name if xp.name != u'selff' else u'self'
                    # xp.name = ap.name
                    # ap.name = xp.name
                    a.symtab[ap.name].name = xp_name

            # add a symbol table items to xf
            #   this will give it access to the argument names of a
            #   then updates xf children with 
            xf.symtab = dict(a.symtab.items() + xf.symtab.items())
            for c in xf.childrenNodes:
                utils.walk(cpy_sym, c)

            # NOT SURE WHY THIS IS NEEDED
            #    without this it isn't able to resolve the string type of the
            #    function. not sure why...
            a.symtab = dict(xf.symtab.items() + a.symtab.items())
            for c in a.childrenNodes:
                utils.walk(cpy_sym, c)

            # returns empty switch statement to be filled by axioms declarations
            #   of the axiom "a"
            body = xf.get_xform()

            if any([p.method for p in a.parameters]):
                # iterate through body of axiom declarations of a, translate
                #    them to appropriate IRs (i.e. JSON dicts)
                a.body.stmts = self.tltr.trans_xform(a.name, body, a.body.stmts)
                            
            casess = []

            for i in range(0, len(a.parameters)):
                # Find the right instance for which case this should be in the
                #    resulting switch statement
                decs = utils.extract_nodes([AxiomDeclaration], a.parameters[i])

                # decs = filter(lambda m: m.adt and m.name_no_nested() == a.parameters[i].name_no_nested(), adt_mtds)
                                
                # cases = map(lambda d: d.name_no_nested().capitalize(), decs)
                
                decs2 = [m for m in adt_mtds if m.name.split('_')[0] == a.parameters[i].name and a.parameters[i].name == cls.name]
                
                # Add the empty constructor to the declarations if needed
                if not a.parameters[0].method:
                    decs.append(adt_mtds[0])
                    
                cases = []
                    
                if a.parameters[i].method and len(decs2) > 0:
                    for d in decs2:
                        # params = a.parameters[i].method.parameters
                        # name = a.parameters[i].method.name
                        # for p in params:
                        #     name += '_'+self.tltr.trans_ty(p.typee).lower()
                        name = a.parameters[i].method.name_no_nested(d.constructor, adt_mtds).capitalize()
                        # cases.append(name)
                        cases.append((name, i))
                else:
                    for d in decs:
                        if isinstance(d, AxiomDeclaration):
                            # cases.append(d.name_no_nested(False, adt_mtds).capitalize())
                            cases.append((d.name_no_nested(False, adt_mtds).capitalize(), i))
                        else:
                            # cases.append(d.name_no_nested(False).capitalize())
                            cases.append((d.name_no_nested(False).capitalize(), i))
                    # cases = map(lambda d: d.name_no_nested(False, adt_mtds).capitalize(), decs)
                    
                casess.append(cases)
                
            # add cases to body
            if any([p.method for p in a.parameters]):
                body.add_body_nested(casess, a.body.stmts, adt_mtds, xf.parameters, cls, a, self.is_ax_cls)
            else:
                body.create_normal_body(a.body)

        for v in xforms.values():
            buf.write(self.tltr.trans(v))        
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

    def to_struct(self, is_ax_cls, cls):
        if not cls.extendsList: self.tltr.obj_struct = self.to_v_struct(cls, is_ax_cls)
 
    # from the given base class,
    # generate a virtual struct that encompasses all the class in the hierarchy
    def to_v_struct(self, cls, is_ax_cls):
        cls_d = {u'name':str(cls)}
        cls_v = ClassOrInterfaceDeclaration(cls_d)
        # add __cid field
        fd = FieldDeclaration(
            {u'variables':{u'@e': [{u'@t': u'VariableDeclarator',
                                    u'id': {u'name': u'__cid',},},],},
             u'type':{u'@t': u'PrimitiveType', u'type':
                      {u'nameOfBoxedType': u'Integer', u'name': u'Int',},},},)
        cls_v.members.append(fd)
        cls_v.childrenNodes.append(fd)
        def per_cls(cls):
            cname = str(cls)
            if cname != str(cls_v):
                self.tltr.ty[str(cls)] = str(cls_v) if not cls.axiom else str(cls)  
            flds = [m for m in cls.members if type(m) == FieldDeclaration]
            def cp_fld(fld):
                fld_v = cp.copy(fld)
                fld_v.parentNode = cls
                cls_v.members.append(fld_v)
                cls_v.childrenNodes.append(fld_v)
            for f in flds:
                if not td.isStatic(f):
                    cp_fld(f)
        for c in utils.all_subClasses(cls):
            per_cls(c)

        # add ADT fields
        axiom_clss = [c for c in utils.all_subClasses(cls) if c.axiom]
        for a in axiom_clss:
            fd = FieldDeclaration(
                {u'variables':{u'@e': [{u'@t': u'VariableDeclarator',
                                        u'id': {u'name': '_{}'.format(str(a).lower()),},},],},
                 u'type':{u'@t': u'ClassOrInterfaceType', u'name':str(a),},},)

            cls_v.members.append(fd)
            cls_v.childrenNodes.append(fd)

        wrappers = self.gen_arr_wrappers()

        for w in wrappers:
            cls_v.members.append(w)
            cls_v.childrenNodes.append(w)

        return cls_v

    def gen_arr_wrappers(self):
        arrs = ['Array_bit', 'Array_char', 'Array_int', 'Array_float', 'Array_double', 'Array_Object', 'Primitive_bit', 'Primitive_char', 'Primitive_int', 'Primitivie_float', 'Primitive_double']

        primToBox = {
            u'int':u'Integer',
            u'bit':u'Boolean',
            u'float':u'Float',
            u'double':u'Double',
            u'char':u'Character'
        }

        wrappers = []
        
        for a in arrs:
            parts = a.split('_')
            typ = parts[1]
            if parts[0] == 'Array':
                if not (typ == 'Object'):
                    fd = FieldDeclaration(
                        {u'variables':{u'@e': [{u'@t': u'VariableDeclarator',
                                                u'id': {u'name': '_{}'.format(str(a).lower()),},},],},
                         u'type':{u'@t': u'ReferenceType', u'type':
                                  {u'@t': u'PrimitiveType', u'type':
                                   {u'nameOfBoxedType': primToBox[typ], u'name': typ.capitalize(),},},
                                  u'arrayCount':str(1),},},)
                else:
                    fd = FieldDeclaration(
                        {u'variables':{u'@e': [{u'@t': u'VariableDeclarator',
                                                u'id': {u'name': '_{}'.format(str(a).lower()),},},],},
                         u'type':{u'@t': u'ReferenceType', u'type':
                                  {u'@t': u'ClassOrInterfaceType', u'name':str(a),},
                                  u'arrayCount':str(1),},},)
            else:
                fd = FieldDeclaration(
                    {u'variables':{u'@e': [{u'@t': u'VariableDeclarator',
                                            u'id': {u'name': '_{}'.format(str(typ).lower()),},},],},
                     u'type':{u'@t': u'ReferenceType', u'type':
                              {u'@t': u'PrimitiveType', u'type':
                               {u'nameOfBoxedType': primToBox[typ], u'name': typ.capitalize(),},},},},)

            wrappers.append(fd)
                
        return wrappers
                
    
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
    def fs(self): return self._fs
    @fs.setter
    def fs(self, v): self._fs = v

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
