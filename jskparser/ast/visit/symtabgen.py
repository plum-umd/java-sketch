from __future__ import absolute_import
try: xrange
except: xrange = range
from . import visit as v

from .. import JAVA_LANG
from .. import PRIMITIVES

from ..utils import utils
from ..node import Node
from ..compilationunit import CompilationUnit
from ..importdeclaration import ImportDeclaration

from ..body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ..body.fielddeclaration import FieldDeclaration
from ..body.variabledeclarator import VariableDeclarator
from ..body.variabledeclaratorid import VariableDeclaratorId
from ..body.methoddeclaration import MethodDeclaration
from ..body.constructordeclaration import ConstructorDeclaration
from ..body.emptymemberdeclaration import EmptyMemberDeclaration
from ..body.axiomdeclaration import AxiomDeclaration
from ..body.axiomparameter import AxiomParameter

from ..stmt.blockstmt import BlockStmt
from ..stmt.ifstmt import IfStmt
from ..stmt.expressionstmt import ExpressionStmt

from ..expr.nameexpr import NameExpr
from ..expr.variabledeclarationexpr import VariableDeclarationExpr
from ..expr.binaryexpr import BinaryExpr
from ..expr.integerliteralexpr import IntegerLiteralExpr
from ..expr.methodcallexpr import MethodCallExpr
from ..expr.fieldaccessexpr import FieldAccessExpr
from ..expr.objectcreationexpr import ObjectCreationExpr

from ..type.primitivetype import PrimitiveType
from ..type.voidtype import VoidType
from ..type.referencetype import ReferenceType

# https://docs.oracle.com/javase/specs/jls/se8/html/jls-6.html#jls-6.3
class SymtabGen(object):
    NONSYM = [PrimitiveType, VoidType, IntegerLiteralExpr]
    def __init__(self, **kwargs):
       self. _lib = kwargs.get('lib', True)

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """

    def new_symtab(self, n, cp=False):
        if n.symtab: return
        if n.parentNode.symtab:
            n.symtab = n.parentNode.symtab.copy() if cp else n.parentNode.symtab
        elif not n.symtab: n.symtab = {}

    @v.when(Node)
    def visit(self, node):
        if type(node) in self.NONSYM: return
        self.new_symtab(node)
        for n in node.childrenNodes:
            n.accept(self)
        # print "Unimplemented node:", node

    @v.when(CompilationUnit)
    def visit(self, node):
        # The scope of a top level type is all type declarations in the package in
        # which the top level type is declared.
        if self.lib:
            for i in JAVA_LANG: # add in java.lang which is import by default
                nm = i.split('.')
                qn = {
                    u'@t': u'QualifiedNameExpr',
                    u'name': nm[-1],
                    u'qualifier': {
                        u'@t': u'QualifiedNameExpr',
                        u'name': u'lang',
                        u'qualifier': {
                            u'name': u'java',},},
                }
            node.imports.append(ImportDeclaration({u'@t':u'ImportDeclaration',u'name':qn, u'implicit': True}))
            for i in node.imports: node.symtab.update({str(i):i})
        d = dict([v for v in [(t.name,t) for t in node.types]])
        for ty in node.types:
            ty.symtab.update({u'_cu_':node})
            if self.lib:
                for i in node.imports: ty.symtab.update({str(i).split('.')[-1]:i})
            ty.symtab.update(d)
            ty.accept(self)

    # body/
    @v.when(ClassOrInterfaceDeclaration)
    def visit(self, node):
        # The scope of a declaration of a member m declared in or inherited by
        # a class type C is the entire body of C, including any nested type declarations.
        self.new_symtab(node, cp=True)
        # if type(node.parentNode) == ClassOrInterfaceDeclaration:
        #     node.parentNode.symtab.update({str(node):node})
        node.symtab.update({node.name:node})
        if node.name == u'Object': node.parentNode.symtab.update({node.name:node})
        [node.symtab.update({n.name:n}) for n in node.extendsList if n.name not in node.symtab]
        [node.symtab.update({n.name:n}) for n in node.implementsList if n.name not in node.symtab]
        [node.symtab.update({n.name:n}) for n in node.typeParameters if n.name not in node.symtab]
        node.members = [n for n in node.members if not isinstance(n, EmptyMemberDeclaration)]
        for n in node.members:
            node.symtab.update({n.name:n} if isinstance(n, FieldDeclaration) or \
                                         isinstance(n, ClassOrInterfaceDeclaration) else \
                                         {n.sig():n})
        for n in node.members:
            n.accept(self)
        
    @v.when(MethodDeclaration)
    def visit(self, node):
        # The scope of a formal parameter of a method is the entire body of the method
        self.new_symtab(node, cp=True)

        # node.parentNode.symtab.update({str(node):node})
        node.symtab.update({node.sig():node})

        if str(node.typee) not in PRIMITIVES and str(node.typee) not in node.symtab:
            node.symtab.update({str(node.typee):node.typee})
        # somethign is weird here. shouldnt have to visit idd and parameters
        for p in node.parameters:
            p.idd.accept(self)
        for p in node.parameters:
            p.accept(self)
        for t in node.typeParameters:
            node.symtab.update({t.name:t})
        for p in node.parameters:
            p.idd.symtab.update(node.symtab)
        # for c in node.childrenNodes:
        #     c.accept(self)
        if node.body: node.body.accept(self)

        if type(node.parentNode) == ObjectCreationExpr:
            target = node.symtab.get(utils.anon_nm(node).name)
            target.symtab.update({str(node):node})
            node.name = '{}_{}_{}'.format(str(node), node.parentNode.typee, target.name)
            target.symtab.update({str(node):node})

    @v.when(AxiomDeclaration)
    def visit(self, node):
        self.new_symtab(node, cp=True)
        # print '*'*10, str(node)
        # print 'axiomdeclaration:', str(node), node.name
        # print node.symtab
        node.parentNode.symtab.update({node.sig():node})

        if str(node.typee) not in PRIMITIVES and str(node.typee) not in node.symtab:
            node.symtab.update({str(node.typee):node.typee})
        # somethign is weird here. shouldnt have to visit idd and parameters
        # for p in node.parameters:
        #     if p.idd: p.idd.accept(self)
        #     if p.method: p.method.accept(self)
        for p in node.parameters:
            p.accept(self)
        for p in node.parameters:
            if p.idd:
                p.idd.symtab.update(node.symtab)
                # node.symtab = dict(p.idd.symtab.items() + node.symtab.items())
            # Catch args that are actually Axiom Declarations
            if p.method:
                p.method.symtab.update(node.symtab)
                node.symtab = dict(p.method.symtab.items() + node.symtab.items())
        if node.body:
            node.body.accept(self)
        # print node.symtab
        # print '*'*10, str(node)

    @v.when(AxiomParameter)
    def visit(self, node):
        self.new_symtab(node)
        # print '--'*8
        # print 'axiomparameter:', node.name
        # print node.symtab

        node.typee.accept(self)
        if node.idd:
            node.idd.accept(self)
        else:
            node.method.accept(self)
        # print 'axiomparameter:', node.name
        # print node.symtab
        # print '--'*8

    @v.when(ConstructorDeclaration)
    def visit(self, node):
        # The scope of a formal parameter of a constructor is the entire body of the constructor
        self.new_symtab(node, cp=True)
        node.parentNode.symtab.update({str(node):node})
        node.symtab.update({str(node):node})
        for p in node.parameters:
            p.idd.accept(self)
        for p in node.parameters:
            p.accept(self)
        for p in node.parameters:
            p.idd.symtab.update(node.symtab)
        if node.body: node.body.accept(self)

    @v.when(FieldDeclaration)
    def visit(self, node):
        self.new_symtab(node, cp=True)
        node.symtab.update({node.name:node})
        node.variable.accept(self)

    @v.when(VariableDeclarator)
    def visit(self, node):
        self.new_symtab(node)
        if isinstance(node.typee, ReferenceType) and node.typee.arrayCount > 0:
            fd = FieldDeclaration({u"@t": u"FieldDeclaration",
                                   u"variables": {
                                       u"@e": [{u"@t": u"VariableDeclarator",
                                                u"id": {u"name": u"length",},
                                                u'init': {u'@t': u'IntegerLiteralExpr',
                                                          u'value': u'0',},},]},
                                   u"type": {u"@t": u"PrimitiveType",
                                             u"type": {"name": "Int"},},})
            node.symtab.update({u'length':fd})
            if isinstance(node.parentNode, FieldDeclaration):
                node.parentNode.symtab.update({u'length':fd})
        node.symtab.update({node.name:node})
        if node.init: node.init.accept(self)

    @v.when(VariableDeclaratorId)
    def visit(self, node): self.new_symtab(node)

    # stmt/
    @v.when(BlockStmt)
    def visit(self, node):
        self.new_symtab(node, cp=True)
        stlen = len(node.stmts)
        if stlen > 0:
            node.stmts[0].accept(self)
        for i in xrange(1, stlen):
            node.stmts[i].symtab = node.stmts[i-1].symtab.copy()
            node.stmts[i].accept(self)

    @v.when(IfStmt)
    def visit(self, node):
        self.new_symtab(node)
        if node.condition: node.condition.accept(self)
        if node.thenStmt:
            self.new_symtab(node, cp=True)
            node.thenStmt.accept(self)
        if node.elseStmt:
            self.new_symtab(node, cp=True)
            node.elseStmt.accept(self)
            
    @v.when(ExpressionStmt)
    def visit(self, node):
        self.new_symtab(node)
        for n in node.childrenNodes:
            n.accept(self)

    # expr/
    @v.when(FieldAccessExpr)
    def visit(self, node):
        self.new_symtab(node, cp=True)
        for n in node.childrenNodes:
            n.accept(self)

    @v.when(MethodCallExpr)
    def visit(self, node):
        self.new_symtab(node, cp=True)
        for n in node.childrenNodes:
            n.accept(self)

    @v.when(VariableDeclarationExpr)
    def visit(self, node):
        self.new_symtab(node)
        for v in node.childrenNodes:
            v.accept(self)
        # for v in node.varss:
        #     v.accept(self)

    @v.when(BinaryExpr)
    def visit(self, node):
        self.new_symtab(node)
        for n in node.childrenNodes:
            n.accept(self)

    @v.when(NameExpr)
    def visit(self, node):
        self.new_symtab(node)

    @property
    def lib(self): return self._lib
    @lib.setter
    def lib(self, v): self._lib = v
