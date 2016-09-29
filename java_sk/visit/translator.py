#!/usr/bin/env python
import cStringIO
from .. import util

import visit as v
from ast import Operators as op
from ast.node import Node
from ast.compilationunit import CompilationUnit
from ast.body.typedeclaration import TypeDeclaration
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
from ast.type.primitivetype import PrimitiveType
from ast.type.voidtype import VoidType
from ast.type.referencetype import ReferenceType
from ast.type.classorinterfacetype import ClassOrInterfaceType

class Translator(object):
    JAVA_TYPES = {u'int':u'int',u'byte':u'byte',u'short':u'short',u'long':u'long',
                  u'Byte':'Byte',u'Short':u'Short',u'Long':u'Long',u'Int':u'Integer'}
    SKETCH_TYPES = {u'boolean':u'bit', u'this':'self'}
    def __init__(self):
        # convert the given type name into a newer one
        self.ty = {} # { tname : new_tname }

        self._JT = self.JAVA_TYPES
        self._ST = self.SKETCH_TYPES
        self._buf = None
        self._mtd = None
        self._clss = None
        
    @v.on("node")
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """

    @v.when(Node)
    def visit(self, node):
        print "Unimplemented node:", node

    @v.when(BlockStmt)
    def visit(self, node): map(lambda c: c.accept(self), node.childrenNodes)
    @v.when(IfStmt)
    def visit(self, node): map(lambda c: c.accept(self), node.childrenNodes)
    @v.when(ExpressionStmt)
    def visit(self, node): map(lambda c: c.accept(self), node.childrenNodes)
    @v.when(VariableDeclarationExpr)
    def visit(self, node): map(lambda c: c.accept(self), node.childrenNodes)
    @v.when(PrimitiveType)
    def visit(self, node): print node.nameOfBoxedType, node.name

    def trans_stmt(self, s):
        buf = cStringIO.StringIO()
        s.accept(self)
        return util.get_and_close(buf)

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

    def trans_fld(self, fld):
        buf = cStringIO.StringIO()
        buf.write(' '.join([self.trans_ty(fld.typee.name), fld.name]))
        # ignored initialised fields
        buf.write(';')
        return util.get_and_close(buf)

    def trans_params(self, (ty, nm)):
      return ' '.join([self.trans_ty(ty), nm])

    @property
    def mtd(self): return self._mtd
    @mtd.setter
    def mtd(self, v): self._mtd = v

    @property
    def buf(self): return self._buf
    @buf.setter
    def buf(self, v): self._buf = v

    @property
    def mtd(self): return self._mtd
    @mtd.setter
    def mtd(self, v): self._mtd = v

    @property
    def clss(self): return self._clss
    @clss.setter
    def clss(self, v): self._clss = v

    @property
    def JT(self): return self._JT
    @JT.setter
    def JT(self, v): self._JT = v

    @property
    def ST(self): return self._ST
    @ST.setter
    def ST(self, v): self._ST = v

