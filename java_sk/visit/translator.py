#!/usr/bin/env python
import cStringIO

from .. import util

import visit as v

from ast import Operators as op
from ast import AssignOperators as assignop
from ast.body.typedeclaration import TypeDeclaration as td

from ast.utils import utils
from ast.node import Node
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.variabledeclarator import VariableDeclarator
from ast.body.variabledeclaratorid import VariableDeclaratorId
from ast.stmt.blockstmt import BlockStmt
from ast.stmt.returnstmt import ReturnStmt
from ast.stmt.ifstmt import IfStmt
from ast.stmt.forstmt import ForStmt
from ast.stmt.expressionstmt import ExpressionStmt
from ast.stmt.assertstmt import AssertStmt
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
from ast.expr.arrayaccessexpr import ArrayAccessExpr
from ast.expr.enclosedexpr import EnclosedExpr
from ast.type.primitivetype import PrimitiveType
from ast.type.voidtype import VoidType
from ast.type.referencetype import ReferenceType
from ast.type.classorinterfacetype import ClassOrInterfaceType

class Translator(object):
    SELF = NameExpr({u'@t':u'NameExpr',u'name':u'self'})
    __cid = {u'@t': u'AssignExpr', u'op': {u'name': u'assign'},
             u'target': {u'name': u'__cid', u'@t': u'NameExpr'},
             u'value': {u'value': u'', u'@t': u'IntegerLiteralExpr'}}
    
    def __init__(self, **kwargs):
        # convert the given type name into a newer one
        self._ty = {}     # { tname : new_tname }
        self._flds = {}   # { cname.fname : new_fname }
        self._cnums = kwargs.get(u'cnums')
        self._mnums = kwargs.get(u'mnums')

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
        if n.init: self.printCommaList(n.init)
        self.printt('; ')
        if n.compare: n.compare.accept(self)
        self.printt('; ')
        if n.update: self.printCommaList(n.update)
        self.printt(') ')
        n.body.accept(self)

    @v.when(ExpressionStmt)
    def visit(self, n):
        n.expr.accept(self)
        self.printt(';')

    @v.when(AssertStmt)
    def visit(self, n):
        self.printt("assert ")
        n.check.accept(self)
        if n.msg:
            self.printt(" : ")
            n.msg.accept(self)
        self.printt(";")

    # expr
    @v.when(NameExpr)
    def visit(self, n):
        nd = n.symtab.get(n.name, None)
        if type(nd) == FieldDeclaration:
            new_fname = self.trans_fname(nd, nd.variables[0].name)
            if td.isStatic(nd):
                if utils.get_coid(nd).name == self.mtd.parentNode.name:
                    self.printt(nd.variables[0].name)
                else: self.printt(new_fname + "()")
            else: self.printt('.'.join([u'self', new_fname]))
        else: self.printt(n.name)

    @v.when(VariableDeclarationExpr)
    def visit(self, n):
        n.typee.accept(self)
        self.printt(' ')
        self.printCommaList(n.varss)

    @v.when(AssignExpr)
    def visit(self, n):
        n.target.accept(self)
        self.printt(' ')
        self.printt(assignop[n.op.upper()])
        self.printt(' ')
        n.value.accept(self)

    @v.when(FieldAccessExpr)
    def visit(self, n):
        cls = self.scope_to_cls(n)
        fld = cls.symtab[n.field.name]
        new_fname = self.trans_fname(fld, n.field.name)
        self.printt('.'.join([n.scope.name, new_fname]))

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
        self.printt("new ")
        n.typee.accept(self)
        cid = self.__cid
        cid[u'value'][u'value'] = str(self._cnums[n.typee.name])
        n.args = [AssignExpr(cid)] + n.args
        self.printArguments(n.args)
    
    @v.when(MethodCallExpr)
    def visit(self, n):
        rcv_ty = self.scope_to_cls(n)
        callee = rcv_ty.symtab.get(n.name)
        if not callee: callee = self.find_in_parent(rcv_ty, n.name)
        self.trans_call(callee, n)

    @v.when(EnclosedExpr)
    def visit(self, n):
        self.printt('(')
        if n.inner: n.inner.accept(self)
        self.printt(')')

    @v.when(GeneratorExpr)
    def visit(self, n):
        if n.isHole: self.printt('??')
        else: print '\n!!generator not implemented!!\n'

    @v.when(ArrayAccessExpr)
    def visit(self, n):
        n.nameExpr.accept(self)
        self.printt('[')
        n.index.accept(self)
        self.printt(']')

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

    def printCommaList(self, args):
        if args:
            lenn = len(args)
            for i in xrange(lenn):
                args[i].accept(self)
                if i+1 < lenn: self.printt(', ')

    def printArguments(self, args):
        self.printt('(')
        self.printCommaList(args)
        self.printt(')')

    def trans_call(self, callee, callexpr):
        args = callexpr.args
        if not td.isStatic(callee):
            args = [NameExpr({u'@t':u'NameExpr',u'name':callexpr.scope.name})] + callexpr.args
        mid = '@'.join([self.trans_mname(callexpr, True), callee.parentNode.typee.name])
        self.printt(mid)
        self.printArguments(args)
        # if td.isStatic(callee) or callee.name in self.SKETCH_BUILTIN: args = callexpr.args
        # elif callexpr.scope: args = [callexpr.scope] + callexpr.args
        # else: args = [self.SELF] + callexpr.args
        # self.printt(mid)

    def trans_stmt(self, s):
        self.buf = cStringIO.StringIO()
        s.accept(self)
        return util.get_and_close(self.buf)

    # def trans_mname(cname, mtd, arg_typs=[]):
    def trans_mname(self, mtd, call=False):
        # skipping memoized names and collections
        # ignore ambiguous or not found
        return util.repr_mtd(mtd, call)
    
    def trans_ty(self, typ, didrepr=False):
        # self.JT => JAVA_TYPES, self.ST => SKETCH_TYPES
        # ignoring a lot of 'advanced' type stuff
        _tname = typ if didrepr else util.sanitize_ty(typ.name.strip())
        r_ty = _tname

        if typ and type(typ) == ReferenceType:
            if typ.name in self.ty: r_ty = self.ty[typ.name]
            if typ.values: r_ty += ''.join(["[{}]".format(v.name) for v in typ.values])
        # we've already rewritten this type
        elif _tname in self.ty: r_ty = self.ty[_tname]
        # this type is a Sketh type
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
            buf.write('{} {};\n'.format(self.trans_ty(fld.typee), var.name))
        # ignored initialised fields
        return util.get_and_close(buf)

    def trans_params(self, (ty, nm)):
      return ' '.join([self.trans_ty(ty), nm])

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
        
    def scope_to_cls(self, node):
        s_tab = node.scope.symtab
        typ = s_tab[node.scope.name].typee.name
        cls = s_tab[typ]
        return cls

    # givent a type, check all parent classes for name
    def find_in_parent(self, rcv_ty, name):
        if name in rcv_ty.symtab: return rcv_ty.symtab[name]
        else:
            c = []
            for e in rcv_ty.extendsList:
                c = self.find_in_parent(rcv_ty.symtab[e.name], name)
                if c: return c
        
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

