#!/usr/bin/env python
import cStringIO
import itertools

from . import util

import visit as v

from ast import Operators as op
from ast import AssignOperators as assignop

from ast.utils import utils
from ast.node import Node

from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.constructordeclaration import ConstructorDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.parameter import Parameter
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.variabledeclarator import VariableDeclarator
from ast.body.variabledeclaratorid import VariableDeclaratorId

from ast.stmt.blockstmt import BlockStmt
from ast.stmt.returnstmt import ReturnStmt
from ast.stmt.ifstmt import IfStmt
from ast.stmt.forstmt import ForStmt
from ast.stmt.minrepeatstmt import MinrepeatStmt
from ast.stmt.emptystmt import EmptyStmt
from ast.stmt.expressionstmt import ExpressionStmt
from ast.stmt.assertstmt import AssertStmt
from ast.stmt.assumestmt import AssumeStmt
from ast.stmt.switchstmt import SwitchStmt
from ast.stmt.switchentrystmt import SwitchEntryStmt
from ast.stmt.explicitconstructorinvocationstmt import ExplicitConstructorInvocationStmt

from ast.expr.variabledeclarationexpr import VariableDeclarationExpr
from ast.expr.unaryexpr import UnaryExpr
from ast.expr.binaryexpr import BinaryExpr
from ast.expr.nameexpr import NameExpr
from ast.expr.assignexpr import AssignExpr
from ast.expr.integerliteralexpr import IntegerLiteralExpr
from ast.expr.methodcallexpr import MethodCallExpr
from ast.expr.generatorexpr import GeneratorExpr
from ast.expr.objectcreationexpr import ObjectCreationExpr
from ast.expr.fieldaccessexpr import FieldAccessExpr
from ast.expr.arraycreationexpr import ArrayCreationExpr
from ast.expr.arrayinitializerexpr import ArrayInitializerExpr
from ast.expr.arrayaccessexpr import ArrayAccessExpr
from ast.expr.enclosedexpr import EnclosedExpr
from ast.expr.conditionalexpr import ConditionalExpr
from ast.expr.thisexpr import ThisExpr
from ast.expr.superexpr import SuperExpr
from ast.expr.castexpr import CastExpr
from ast.expr.booleanliteralexpr import BooleanLiteralExpr

from ast.type.primitivetype import PrimitiveType
from ast.type.voidtype import VoidType
from ast.type.referencetype import ReferenceType
from ast.type.classorinterfacetype import ClassOrInterfaceType

class Translator(object):
    SELF = NameExpr({u'@t':u'NameExpr',u'name':u'self'})
    _cid = {u'@t': u'AssignExpr', u'op': {u'name': u'assign'},
            u'target': {u'name': u'__cid', u'@t': u'NameExpr'},
            u'value': {u'value': u'', u'@t': u'IntegerLiteralExpr'}}
    ARRAY_SIZE = 50
    def __init__(self, **kwargs):
        # convert the given type name into a newer one
        self._ty = {}     # { tname : new_tname }
        self._flds = {}   # { cname.fname : new_fname }
        self._cnums = kwargs.get('cnums')
        self._mnums = kwargs.get('mnums')

        from . import JAVA_TYPES
        from . import SKETCH_TYPES
        self._JT = JAVA_TYPES
        self._ST = SKETCH_TYPES

        self._buf = None
        self._mtd = None
        self._cls = None

        # array bounds will be set to this if not specified
        self._num_mtds = 0

        # for pretty printing
        self._indentation = kwargs.get('indentation', "    ")
        self._level = kwargs.get('level', 0)
        self._indented = kwargs.get('indented', False)

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """

    @v.when(Node)
    def visit(self, n):
        print 'unimplemented node:', n
        # if isinstance(n, Type): print 'un:', n
        # map(lambda x: x.accept(self), n.childrenNodes)

    # body
    @v.when(ConstructorDeclaration)
    def visit(self, n):
        p = Parameter({u'id':{u'name':u'self'},
                       u'type':{u'@t':u'ClassOrInterfaceType',u'name':u'Object'}})
        n.parameters = [p] + n.parameters

        self.printt('Object {}'.format(str(n)))
        self.printt('(')
        self.printSepList(n.parameters)
        self.printt(')')

        for i in xrange(n.arrayCount): self.printt('[]')
        if n.throws:
            self.printt(' throws ')
            self.printCommaList(n.throws)
            
        if not n.body: self.printt(';')
        else:
            n.body.stmts = n.body.stmts + [u'return self;']
            n.body.accept(self)
        self.printLn()

    @v.when(MethodDeclaration)
    def visit(self, n):
        if td.isHarness(n):
            self.printt('harness ')
            n.body.stmts = [u'Object self = new Object(__cid=0);'] + n.body.stmts
        n.typee.accept(self)
        self.printt(' ')
        self.printt(str(n))
        self.printt('(')

        if not td.isStatic(n) and not td.isHarness(n):
            ty = self.trans_ty(str(n.parentNode), didrepr=True)
            self.printt('{} self'.format(ty))
            if n.parameters: self.printt(', ')
        self.printSepList(n.parameters)
        self.printt(')')

        for i in xrange(n.arrayCount): self.printt('[]')
        if n.throws:
            self.printt(' throws ')
            self.printCommaList(n.throws)
            
        if not n.body: self.printt(';')
        else:
            self.printt(' ')
            n.body.accept(self)
        self.printLn()

    @v.when(Parameter)
    def visit(self, n):
        self.buf.write(' '.join([self.trans_ty(n.typee), n.name]))

    @v.when(VariableDeclarator)
    def visit(self, n):
        n.idd.accept(self)
        if n.init:
            self.printt(' = ')
            n.init.accept(self)

    @v.when(VariableDeclaratorId)
    def visit(self, n):
        self.printt(n.name)

    # stmt
    @v.when(BlockStmt)
    def visit(self, n):
        self.printLn('{')
        if n.stmts:
            self.indent()
            for s in n.stmts:
                if type(s) == str or type(s) == unicode:
                    self.printLn(s)
                else:
                    s.accept(self)
                    self.printLn()
            self.unindent()
        self.printt('}')

    @v.when(ReturnStmt)
    def visit(self, n):
        self.printt('return')
        if n.expr:
            self.printt(' ')
            n.expr.accept(self)
        self.printt(';')

    @v.when(IfStmt)
    def visit(self, n):
        self.printt('if (')
        n.condition.accept(self)
        thenBlock = isinstance(n.thenStmt, BlockStmt)
        self.printt(') ')
        if not thenBlock: self.indent()
        n.thenStmt.accept(self)
        if not thenBlock: self.unindent()
        if n.elseStmt:
            self.printLn()
            elseIf = isinstance(n.elseStmt, IfStmt)
            elseBlock = isinstance(n.elseStmt, BlockStmt)
            if elseIf or elseBlock: self.printt('else ')
            else:
                self.printLn('else')
                self.indent()
            n.elseStmt.accept(self)
            if not (elseIf or elseBlock): self.unindent()
                
    @v.when(ForStmt)
    def visit(self, n):
        self.printt('for (')
        if n.init: self.printSepList(n.init)
        self.printt('; ')
        if n.compare: n.compare.accept(self)
        self.printt('; ')
        if n.update: self.printSepList(n.update)
        self.printt(') ')
        n.body.accept(self)

    @v.when(MinrepeatStmt)
    def visit(self, n):
        self.printt('minrepeat ')
        n.body.accept(self)
        
    @v.when(ExpressionStmt)
    def visit(self, n):
        n.expr.accept(self)
        if type(n.expr) != MethodCallExpr: self.printt(';')

    @v.when(AssertStmt)
    def visit(self, n):
        self.printt("assert ")
        n.check.accept(self)
        if n.msg:
            self.printt(" : ")
            n.msg.accept(self)
        self.printt(";")

    @v.when(AssumeStmt)
    def visit(self, n):
        self.printt("assume ")
        n.expr.accept(self)
        self.printt(";")

    @v.when(SwitchStmt)
    def visit(self, n):
        for e in xrange(len(n.entries)):
            self.printt('if (') if e == 0 else self.printt('else if (')
            n.selector.accept(self)
            self.printt(' == ')
            n.entries[e].label.accept(self)
            self.printLn(') {')
            self.indent()
            for s in n.entries[e].stmts: s.accept(self)
            self.unindent()
            self.printLn()
            self.printLn('}')
        
    @v.when(SwitchEntryStmt)
    def visit(self, n):
        pass
        
    @v.when(ExplicitConstructorInvocationStmt)
    def visit(self, n):
        if n.isThis:
            self.printt('self')
        else:
            if n.expr:
                n.expr.accept(self)
                self.printt('.')
            cls = utils.get_coid(n)
            sups = cls.supers()
            if not sups: exit('Calling super with  with no super class: {}'.format(cls.name))
            def ty(a):
                return a.typee.name if type(a) != NameExpr else n.symtab[a.name].typee.name
            arg_typs = '_'.join([u'Object'] + map(ty, n.args))
            self.printt('_'.join([sups[0].name, arg_typs]))
            self.printt('@{}'.format(sups[0].name))
        self.printt(u'(self')
        if n.args: self.printt(', ')
        self.printSepList(n.args)
        self.printt(');')

    @v.when(EmptyStmt)
    def visit(self, n): pass

    # expr
    @v.when(NameExpr)
    def visit(self, n):
        nd = n.symtab.get(n.name, None)
        if type(nd) == FieldDeclaration:
            new_fname = self.trans_fname(nd, nd.variables[0].name)
            if td.isStatic(nd): self.printt(nd.variables[0].name)
            else: self.printt('.'.join([u'self', new_fname]))
        else: self.printt(n.name)
            
    @v.when(VariableDeclarationExpr)
    def visit(self, n):
        n.typee.accept(self)
        self.printt(' ')
        self.printSepList(n.varss)

    @v.when(AssignExpr)
    def visit(self, n):
        n.target.accept(self)
        if type(n.target) == FieldAccessExpr and type(n.target.scope) != ThisExpr and \
           td.isStatic(self.find_fld(n.target)):
            return
        self.printt(' ')
        self.printt(assignop[n.op.upper()])
        self.printt(' ')
        n.value.accept(self)

    @v.when(FieldAccessExpr)
    def visit(self, n):
        fld = self.find_fld(n)
        def fld_access():
            n.scope.accept(self)
            new_fname = self.trans_fname(fld, n.field.name)
            self.printt('.{}'.format(new_fname))
        if td.isStatic(fld):
            if n.scope.name == utils.get_coid(n).name:
                self.printt(fld.variables[0].name)
            elif type(n.parentNode) == AssignExpr and n == n.parentNode.target:
                self.printt('{}_s@{}('.format(fld.variables[0].name, fld.parentNode.name))
                n.parentNode.value.accept(self)
                self.printt(')')
            else:
                self.printt('{}_g@{}()'.format(fld.variables[0].name, fld.parentNode.name))
        else:
            fld_access()

    @v.when(UnaryExpr)
    def visit(self, n):
        self.printt(UnaryExpr.PRE_OPS.get(n.op, ''))
        n.expr.accept(self)
        self.printt(UnaryExpr.POST_OPS.get(n.op, ''))

    @v.when(BinaryExpr)
    def visit(self, n):
        n.left.accept(self)
        self.printt(' ')
        self.printt(op[n.op.upper()])
        self.printt(' ')
        n.right.accept(self)

    @v.when(ObjectCreationExpr)
    def visit(self, n):
        if n.scope:
            n.getScope.accept(self)
            self.printt(".")
        if n.args:
            typs = []
            for a in n.args:
                if type(a) == FieldAccessExpr:
                    tname = self.find_fld(a).typee.name
                elif not a.typee:
                    tname = n.symtab[a.name].typee.name
                else:
                    tname = a.typee.name
                typs.append(tname)
                    
            self.printt('_'.join([n.typee.name] + [u'Object'] + typs))
        else:
            self.printt('{}_Object'.format(n.typee.name))
        self.printt('((new Object(__cid={}()))'.format(n.typee.name))
        if n.args: self.printt(', ')
        self.printSepList(n.args)
        self.printt(')')
        
    @v.when(ArrayCreationExpr)
    def visit(self, n):
        for c in xrange(n.arrayCount):
            n.initializer.accept(self)

    @v.when(ArrayInitializerExpr)
    def visit(self, n):
        self.printt('{')
        self.printSepList(n.values)
        self.printt('}')

    @v.when(ArrayAccessExpr)
    def visit(self, n):
        n.nameExpr.accept(self)
        self.printt('[')
        n.index.accept(self)
        self.printt(']')

    @v.when(MethodCallExpr)
    def visit(self, n):
        rcv_ty = self.scope_to_cls(n) if n.scope else utils.get_coid(n)
        mdec = self.mdec_from_callexpr(rcv_ty, n)
        self.trans_call(rcv_ty, mdec, n)

    @v.when(EnclosedExpr)
    def visit(self, n):
        self.printt('(')
        if n.inner: n.inner.accept(self)
        self.printt(')')

    @v.when(GeneratorExpr)
    def visit(self, n):
        if n.isHole: self.printt('??')
        else:
            self.printt('{| ')
            self.printSepList(n.exprs, ' | ')
            self.printt(' |}')

    @v.when(ConditionalExpr)
    def visit(self, n):
        n.condition.accept(self)
        self.printt(' ? ')
        n.thenExpr.accept(self)
        self.printt(' : ')
        n.elseExpr.accept(self)

    @v.when(ThisExpr)
    def visit(self, n):
        if n.classExpr:
            n.classExpr.accept(self)
            self.printt('.')
        self.printt('self')

    @v.when(SuperExpr)
    def visit(self, n):
        if n.classExpr:
            n.classExpr.accept(self)
            self.printt('.')
        self.printt('super')

    @v.when(CastExpr)
    def visit(self, n):
        n.expr.accept(self)

    @v.when(BooleanLiteralExpr)
    def visit(self, n):
        self.printt(n.value)

    # type
    @v.when(ClassOrInterfaceType)
    def visit(self, n):
        self.printt(self.trans_ty(n))

    @v.when(IntegerLiteralExpr)
    def visit(self, n):
        self.printt(n.value)

    @v.when(PrimitiveType)
    def visit(self, n):
        self.printt(n.name)

    @v.when(VoidType)
    def visit(self, n):
        self.printt(n.name)

    @v.when(ReferenceType)
    def visit(self, n):
        n.typee.accept(self)
        for i in xrange(n.arrayCount):
            self.printt('[')
            if n.values:
                n.values[i].accept(self)
            else:
                self.printt(str(self.num_mtds))
            self.printt(']')

    def trans(self, s):
        self.buf = cStringIO.StringIO()
        s.accept(self)
        return util.get_and_close(self.buf)
    
    def trans_ty(self, typ, didrepr=False):
        # self.JT => JAVA_TYPES, self.ST => SKETCH_TYPES
        # ignoring a lot of 'advanced' type stuff
        _tname = typ if didrepr else typ.sanitize_ty(typ.name.strip())
        r_ty = _tname
        if typ and type(typ) == ReferenceType:
            if typ.name in self.ty: r_ty = self.ty[typ.name]
            if typ.values: r_ty += ''.join(["[{}]".format(v.name) for v in typ.values])
            else: r_ty += ''.join(['[{}]'.format(self.ARRAY_SIZE) for i in xrange(typ.arrayCount)])
        # we've already rewritten this type
        elif _tname in self.ty: r_ty = self.ty[_tname]
        # this type is a Sketch type
        elif _tname in self.ST: r_ty = self.ST[_tname]
        # type translates to Sketch int
        elif _tname in [self.JT[u'byte'], self.JT[u'short'], self.JT[u'long'],
                        self.JT[u'Byte'], self.JT[u'Short'], self.JT[u'Long'],
                        self.JT[u'Int']]: r_ty = self.JT[u'int']
        return r_ty

    def trans_fname(self, fld, nm):
        fid = '.'.join([utils.get_coid(fld).name, nm])
        r_fld = self.flds[fid]
        return r_fld

    def trans_fld(self, fld):
        buf = cStringIO.StringIO()
        for var in fld.variables:
            init = ''
            if var.init:
                init = ' = '
                init += self.trans(var.init)
            buf.write('{} {}{};\n'.format(self.trans_ty(fld.typee), var.name, init))
        # ignored initialised fields
        return util.get_and_close(buf)

    def trans_params(self, (ty, nm)):
        return ' '.join([self.trans_ty(ty), nm])

    def scope_to_cls(self, n):
        if type(n) == CastExpr:
            return n.symtab[n.typee.name]
        if type(n.scope) == EnclosedExpr:
            return self.scope_to_cls(n.scope.inner)
        if type(n.scope) == ThisExpr: return utils.get_coid(n.scope)
        s_tab = n.scope.symtab
        v = s_tab[n.scope.nameExpr.Name] if type(n) == ArrayAccessExpr else \
            s_tab[n.scope.name]
        if isinstance(v, td): return v
        typ = s_tab[n.scope.name].typee.name
        cls = s_tab[typ]
        return cls

    def trans_call(self, rcv_ty, mdec, callexpr):
        if not callexpr.scope:
            mdec = self.mdec_from_callexpr(utils.get_coid(callexpr), callexpr)
            self.printt('{}@{}'.format(str(mdec), mdec.parentNode.name))
            nm = [] if td.isStatic(mdec) else [NameExpr({u'@t':u'NameExpr',u'name':u'self'})]
            self.printArguments(nm + callexpr.args)
            # self.printt(';')
            return
        args = callexpr.args
        mname = str(callexpr)
        if not td.isStatic(mdec):
            args = [NameExpr({u'@t':u'NameExpr',u'name':callexpr.scope.name})] + callexpr.args
        else:
            self.printt('@'.join([mname, mdec.parentNode.name]))
            self.printArguments(args)
            if type(callexpr.parentNode) == ExpressionStmt: self.printt(';')
            return
        clss, call = [rcv_ty] + filter(lambda c: not c.interface, rcv_ty.supers()), []
        for c in clss:
            md = c.symtab.get(str(callexpr))
            if (md and str(md) != mname) or not md:
                mname = str(callexpr)
                md = self.mdec_from_callexpr(rcv_ty, callexpr)
            call.append(md)
        t = 'IfStmt' if type(mdec.typee) == VoidType else 'ConditionalExpr'
        conexprs = [self.make_dispatch(callexpr, args, c, t) for c in zip(call, clss)]
        def combine(l, r):
            if t == 'ConditionalExpr': l.elseExpr = r
            else: l.elseStmt = r
            return l
        conexprs = reduce(combine, conexprs)
        if t == 'ConditionalExpr': self.printt('(')
        self.print_dispatch(conexprs)
        if t == 'ConditionalExpr': self.printt(')')

    def print_dispatch(self, c):
        # we need to do this b/c the elseExpr's are going to have MethodCallExpr which
        # get handled differently
        if type(c) == ConditionalExpr:
            c.condition.accept(self)
            self.printt(' ? ')
            self.printt('{}'.format(c.thenExpr.name))
            self.printArguments(c.thenExpr.args)
            self.printt(' : ')
            if type(c.elseExpr) == IntegerLiteralExpr:
                self.printt(c.elseExpr.value)
            else:
                self.print_dispatch(c.elseExpr)
        else:
            self.printt('if (')
            c.condition.accept(self)
            self.printt(') { ')
            self.printt('{}'.format(c.thenStmt.name))
            self.printArguments(c.thenStmt.args)
            self.printt('; }')
            if type(c.elseStmt) == IntegerLiteralExpr:
                self.printLn()
                self.printt('else {{ {}; }}'.format(c.elseStmt.value))
            else:
                self.printLn()
                self.printt('else ')
                self.print_dispatch(c.elseStmt)

    def make_dispatch(self, callexpr, args, mdec_cls, typee):
        d = {
            "@t": "",
            "condition": {
                "@t": "BinaryExpr",
                "op": {
                    "name": "equals"
                },
                "left": {
                    "@t": "NameExpr",
                    "name": "",
                },
                "right": {
                    "@t": "IntegerLiteralExpr",
                    "value": "",
                },
            },
            "thenExpr": {
                "@t": "MethodCallExpr",
                "scope": {
                    "@t": "NameExpr",
                    "name": "",
                },
                "name": {
                    "name": "",
                },
                "args": {},
            },
            "elseExpr": {
                "@t": "IntegerLiteralExpr",
                "value": "0",
            },
        }
        d['@t'] = typee
        d['condition']['left']['name'] = '.'.join([callexpr.scope.name, '__cid'])
        d['condition']['right']['value'] = '{}()'.format(mdec_cls[1].name)
        if typee == 'ConditionalExpr':
            d['thenExpr']['scope']['name'] = callexpr.scope.name
            d['thenExpr']['name'] = '@'.join([str(mdec_cls[0]), mdec_cls[0].parentNode.name])
            dis = ConditionalExpr(d)
            dis.thenExpr.args = args
        else:
            d['thenStmt'] = d.pop('thenExpr')
            d['elseStmt'] = d.pop('elseExpr')
            d['thenStmt']['scope']['name'] = callexpr.scope.name
            d['thenStmt']['name'] = '@'.join([str(mdec_cls[0]), mdec_cls[0].parentNode.name])
            dis = IfStmt(d)
            dis.thenStmt.args = args
        return dis
        
    def mdec_from_callexpr(self, rcv_ty, n):
        mdec = rcv_ty.symtab.get(str(n))
        if mdec: return mdec
        atypes = n.arg_typs()
        # TODO: if we can't find the method in any parent classes it might have been defined
        # with a different signature
        def permute_args(typs):
            candidates = []
            for i in xrange(len(n.args)):
                if type(n.args[i]) == NameExpr:
                    typ = n.args[i].symtab[n.args[i].name].typee
                    cls = n.args[i].symtab[typ.name]
                    candidates.append(map(lambda s: s.name, cls.supers()))
            return ['_'.join(s) for s in itertools.product(*candidates)]
        pargs = ['_'.join([n.name, a]) for a in permute_args(atypes)]
        for p in pargs:
            mdec = self.find_in_parent(rcv_ty, p)
            if mdec: return mdec
        exit('Cant find {} in {}'.format(str(n), rcv_ty))
            
    # given a type, check all parent classes for name
    def find_in_parent(self, rcv_ty, name):
        if name in rcv_ty.symtab: return rcv_ty.symtab[name]
        else:
            c = []
            for e in rcv_ty.extendsList:
                print rcv_ty.symtab
                if e.name == u'Object': return None
                c = self.find_in_parent(rcv_ty.symtab[e.name], name)
                if c: return c

    def find_fld(self, n):
        cls = self.scope_to_cls(n)
        fld = None
        sups = cls.supers()
        if n.field.name in cls.symtab:
            fld = cls.symtab[n.field.name]
        else:
            sups = cls.supers()
            for c in sups:
                if n.field.name in c.symtab:
                    cls = c
                    fld = c.symtab[n.field.name]
                    break
        if not fld: exit('fld {} not found in class {} or super classes.'.format(n.field.name, cls.name))
        return fld
        
    def indent(self): self._level += 1
    def unindent(self): self._level -= 1
    
    def makeIndent(self):
        for i in xrange(self._level): self._buf.write(self._indentation)

    def printt(self, arg):
        if not self._indented:
            self.makeIndent()
            self.indented = True
        self.buf.write(arg)

    def printLn(self, arg=None):
        if arg:
            self.printt(arg)
        self.buf.write('\n')
        self.indented = False
        
    def printSepList(self, args, sep=','):
        if args:
            lenn = len(args)
            for i in xrange(lenn):
                args[i].accept(self)
                if i+1 < lenn: self.printt('{} '.format(sep))

    def printArguments(self, args):
        self.printt('(')
        self.printSepList(args)
        self.printt(')')
        
    @property
    def mtd(self): return self._mtd
    @mtd.setter
    def mtd(self, v): self._mtd = v

    @property
    def buf(self): return self._buf
    @buf.setter
    def buf(self, v): self._buf = v

    @property
    def indented(self): return self._indented
    @indented.setter
    def indented(self, v): self._indented = v

    @property
    def indentation(self): return self._indentation
    @indentation.setter
    def indentation(self, v): self._indentation = v

    @property
    def mtd(self): return self._mtd
    @mtd.setter
    def mtd(self, v):
        self._mtd = v
        self._cls = v.parentNode

    @property
    def cls(self): return self._cls
    @cls.setter
    def cls(self, v): self._cls = v

    @property
    def ty(self): return self._ty
    @ty.setter
    def ty(self, v): self._ty = v

    @property
    def flds(self): return self._flds
    @flds.setter
    def flds(self, v): self._flds = v

    @property
    def JT(self): return self._JT
    @JT.setter
    def JT(self, v): self._JT = v

    @property
    def ST(self): return self._ST
    @ST.setter
    def ST(self, v): self._ST = v

    @property
    def num_mtds(self): return self._num_mtds
    @num_mtds.setter
    def num_mtds(self, v): self._num_mtds = v

