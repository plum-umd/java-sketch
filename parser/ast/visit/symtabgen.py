import visit as v

from .. import JAVA_LANG
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

# https://docs.oracle.com/javase/specs/jls/se8/html/jls-6.html#jls-6.3
class SymtabGen(object):
    NONSYM = [PrimitiveType, VoidType, IntegerLiteralExpr]
    # def __init__(self, **kwargs):

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
        map(lambda n: n.accept(self), node.childrenNodes)
        # print "Unimplemented node:", node

    @v.when(CompilationUnit)
    def visit(self, node):
        # The scope of a top level type is all type declarations in the package in
        # which the top level type is declared.
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
        d = dict([v for v in map(lambda t: (t.name,t), node.types)])
        for ty in node.types:
            ty.symtab.update({u'_cu_':node})
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
        [node.symtab.update({n.name:n}) for n in node.extendsList if n.name not in node.symtab]
        [node.symtab.update({n.name:n}) for n in node.implementsList if n.name not in node.symtab]
        map(lambda n: node.symtab.update({n.name:n} if type(n) == FieldDeclaration or type(n) == ClassOrInterfaceDeclaration else \
                                         {str(n):n}), node.members)
        map(lambda n: n.accept(self), node.members)

    @v.when(MethodDeclaration)
    def visit(self, node):
        # The scope of a formal parameter of a method is the entire body of the method
        self.new_symtab(node, cp=True)
        node.parentNode.symtab.update({str(node):node})
        if type(node.parentNode) == ObjectCreationExpr:
            target = utils.anon_nm(node)
            nm = '_'.join([str(node), target.name])
            node.parentNode.symtab.update({nm:node})
            target.symtab.update({nm:node})
            node.symtab.update({nm:node})
            node.parentNode.symtab.update({str(node):node})
        node.symtab.update({str(node):node})
        if str(node.typee) not in node.symtab: node.symtab.update({str(node.typee):node.typee})
        map(lambda p: p.accept(self), node.parameters)
        map(lambda t: node.symtab.update({t.name:t}), node.typeParameters)
        map(lambda p: node.symtab.update({p.name:p}), node.parameters)
        if node.body: node.body.accept(self)

    @v.when(ConstructorDeclaration)
    def visit(self, node):
        # The scope of a formal parameter of a constructor is the entire body of the constructor
        self.new_symtab(node, cp=True)
        node.parentNode.symtab.update({str(node):node})
        node.symtab.update({str(node):node})
        map(lambda p: p.accept(self), node.parameters)
        map(lambda p: node.symtab.update({p.name:p}), node.parameters)
        if node.body: node.body.accept(self)
        
    @v.when(FieldDeclaration)
    def visit(self, node):
        self.new_symtab(node, cp=True)
        node.symtab.update({node.name:node})

    @v.when(VariableDeclarator)
    def visit(self, node):
        self.new_symtab(node)
        node.symtab.update({node.name:node})
        map(lambda n: n.accept(self), node.childrenNodes)

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
        map(lambda n: n.accept(self), node.childrenNodes)

    # expr/
    @v.when(FieldAccessExpr)
    def visit(self, node):
        self.new_symtab(node, cp=True)
        map(lambda n: n.accept(self), node.childrenNodes)

    @v.when(MethodCallExpr)
    def visit(self, node):
        self.new_symtab(node, cp=True)
        map(lambda n: n.accept(self), node.childrenNodes)

    @v.when(VariableDeclarationExpr)
    def visit(self, node):
        self.new_symtab(node)
        map(lambda n: n.accept(self), node.childrenNodes)

    @v.when(BinaryExpr)
    def visit(self, node):
        self.new_symtab(node)
        map(lambda n: n.accept(self), node.childrenNodes)

    @v.when(NameExpr)
    def visit(self, node):
        self.new_symtab(node)
