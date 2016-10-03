#!/usr/bin/env python
import cStringIO
from .. import util

import visit as v

from ast import Operators as op
from ast.node import Node
from ast.compilationunit import CompilationUnit
from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.variabledeclarator import VariableDeclarator
from ast.body.variabledeclaratorid import VariableDeclaratorId
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.parameter import Parameter
from ast.stmt.blockstmt import BlockStmt
from ast.stmt.returnstmt import ReturnStmt
from ast.stmt.ifstmt import IfStmt
from ast.stmt.expressionstmt import ExpressionStmt
from ast.stmt.assertstmt import AssertStmt
from ast.expr.variabledeclarationexpr import VariableDeclarationExpr
from ast.expr.binaryexpr import BinaryExpr
from ast.expr.nameexpr import NameExpr
from ast.expr.assignexpr import AssignExpr
from ast.expr.integerliteralexpr import IntegerLiteralExpr
from ast.expr.methodcallexpr import MethodCallExpr
from ast.expr.generatorexpr import GeneratorExpr
from ast.expr.objectcreationexpr import ObjectCreationExpr
from ast.expr.fieldaccessexpr import FieldAccessExpr
from ast.expr.thisexpr import ThisExpr
from ast.type.type import Type
from ast.type.primitivetype import PrimitiveType
from ast.type.voidtype import VoidType
from ast.type.referencetype import ReferenceType
from ast.type.classorinterfacetype import ClassOrInterfaceType

class Translator(object):
    JAVA_TYPES = {u'int':u'int',u'byte':u'byte',u'short':u'short',u'long':u'long',
                  u'Byte':'Byte',u'Short':u'Short',u'Long':u'Long',u'Int':u'Integer'}
    SKETCH_TYPES = {u'boolean':u'bit', u'this':'self'}
    def __init__(self, **kwargs):
        # convert the given type name into a newer one
        self._ty = {}     # { tname : new_tname }
        self._flds = {}   # { cname.fname : new_fname }
        self._s_flds = {} # { cname.fname : accessor }

        self._JT = self.JAVA_TYPES
        self._ST = self.SKETCH_TYPES
        self._buf = None
        self._mtd = None
        self._clss = None

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
        print 'node:', n
        # if isinstance(n, Type): print 'un:', n
        # map(lambda x: x.accept(self), n.childrenNodes)

    @v.when(VariableDeclarator)
    def visit(self, n):
        n.idd.accept(self)
        if n.init:
            self.printt(' = ')
            n.init.accept(self)

    @v.when(VariableDeclaratorId)
    def visit(self, n):
        self.printt(n.name)

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

    @v.when(IfStmt)
    def visit(self, node):
        self.printt('if (')
        node.condition.accept(self)
        thenBlock = isinstance(node.thenStmt, BlockStmt)
        self.printt(') ')
        if not thenBlock: self.indent()
        node.thenStmt.accept(self)
        if not thenBlock: self.unindent()
        if node.elseStmt:
            self.printLn()
            elseIf = isinstance(node.elseStmt, IfStmt)
            elseBlock = isinstance(node.elseStmt, BlockStmt)
            if elseIf or elseBlock: self.printt('else ')
            else:
                self.printLn('else')
                self.indent()
            node.elseStmt.accept(self)
            if not (elseIf or elseBlock): self.unindent()
                
    @v.when(ExpressionStmt)
    def visit(self, n):
        n.expr.accept(self)
        self.printt(';')

    @v.when(NameExpr)
    def visit(self, n):
        node = n.symtab.get(n.name, None)
        print 'node:', node, 'node.name:', node.name
        print 'n.symtab:', n.symtab
        if type(node) == FieldDeclaration:
            new_fname = self.trans_fname(node)
            if td.isStatic(node):
                # access to the static field inside the same class
                if node.parentNode == self.mtd.parentNode:
                    self.printt(node.name)
                # o.w., e.g., static constant in an interface, call the accessor
                else: self.printt(new_fname + "()")
            else: self.printt('.'.join([u'self', new_fname]))
        # this and super will be handled differently once i implement them
        # elif e.id in [C.J.THIS, C.J.SUP]: buf.write(C.SK.self)
        # string constants will be handled differently too
        # elif util.is_str(e.name): # constant string, such as "Hello, World"
            # str_init = trans_mname(C.J.STR, C.J.STR, [u"char[]", C.J.i, C.J.i])
            # s_hash = hash(e.id) % 256 # hash string value itself
            # buf.write("{}(new Object(hash={}), {}, 0, {})".format(str_init, s_hash, e.id, len(e.id)))
        else: self.printt(node.name)

    @v.when(VariableDeclarationExpr)
    def visit(self, n):
        n.typee.accept(self)
        self.printt(' ')
        lenn = len(n.varss)
        for i in xrange(lenn):
            n.varss[i].accept(self)
            if i+1 < lenn: self.printt(', ')

    @v.when(AssignExpr)
    def visit(self, n):
        n.target.accept(self)
        self.printt(' ')
        self.printt(op[n.op.upper()])
        self.printt(' ')
        n.value.accept(self)

    @v.when(BinaryExpr)
    def visit(self, node):
        node.left.accept(self)
        self.printt(' ')
        self.printt(op[node.op.upper()])
        self.printt(' ')
        node.right.accept(self)

    @v.when(ObjectCreationExpr)
    def visit(self, n):
        if n.scope:
            n.getScope.accept(self);
            self.printt(".");
        self.printt("new ");
        n.typee.accept(self);
        self.printArguments(n.args)
    
    @v.when(ClassOrInterfaceType)
    def visit(self, n):
        self.printt(self.trans_ty(n.typee.name))

    @v.when(IntegerLiteralExpr)
    def visit(self, node):
        self.printt(node.value)

    @v.when(VoidType)
    def visit(self, node):
        self.printt(node.name)

    @v.when(ReferenceType)
    def visit(self, n):
        n.typee.accept(self)

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

    def trans_stmt(self, s):
        self.buf = cStringIO.StringIO()
        s.accept(self)
        return util.get_and_close(self.buf)

    # def trans_mname(cname, mtd, arg_typs=[]):
    def trans_mname(self, mtd):
        # skipping memoized names and collections
        # ignore ambiguous or not found
        return util.repr_mtd(mtd)
    
    def trans_ty(self, tname):
        # self.JT => JAVA_TYPES, self.ST => SKETCH_TYPES
        # ignoring a lot of 'advanced' type stuff
        _tname = util.sanitize_ty(tname.strip())
        r_ty = _tname
        if _tname in self.ST: r_ty = self.ST[_tname]
        elif _tname in [self.JT[u'byte'], self.JT[u'short'], self.JT[u'long'], self.JT[u'Byte'], self.JT[u'Short'], 
                  self.JT[u'Long'], self.JT[u'Int']]: r_ty = self.JT[u'int']
        elif _tname in self.ty: r_ty = self.ty[_tname]
        return r_ty

    def trans_fname(self, fld):
        r_fld = fld.name
        fid = '.'.join([fld.parentNode.name, fld.name])
        if td.isStatic(fld) and fid in self.s_flds:
            r_fld = self.s_flds[fid]
        elif fid in self.flds:
            r_fld = self.flds[fid]
        return r_fld

    def trans_fld(self, fld):
        buf = cStringIO.StringIO()
        buf.write(' '.join([self.trans_ty(fld.typee.name), fld.name]))
        # ignored initialised fields
        buf.write(';')
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
    def mtd(self, v): self._mtd = v

    @property
    def ty(self): return self._ty
    @ty.setter
    def ty(self, v): self._ty = v

    @property
    def s_flds(self): return self._s_flds
    @s_flds.setter
    def s_flds(self, v): self._s_flds = v

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

