#!/usr/bin/env python

import cStringIO
import visit as v

from .. import Operators as op
from .. import AssignOperators as assignop

from ..node import Node
from ..compilationunit import CompilationUnit
from ..importdeclaration import ImportDeclaration
from ..typeparameter import TypeParameter

from ..body.typedeclaration import TypeDeclaration
from ..body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ..body.fielddeclaration import FieldDeclaration
from ..body.variabledeclarator import VariableDeclarator
from ..body.variabledeclaratorid import VariableDeclaratorId
from ..body.methoddeclaration import MethodDeclaration
from ..body.constructordeclaration import ConstructorDeclaration
from ..body.parameter import Parameter
from ..body.annotationdeclaration import AnnotationDeclaration
from ..body.annotationmemberdeclaration import AnnotationMemberDeclaration
from ..body.axiomdeclaration import AxiomDeclaration
from ..body.axiomparameter import AxiomParameter

from ..stmt.blockstmt import BlockStmt
from ..stmt.returnstmt import ReturnStmt
from ..stmt.ifstmt import IfStmt
from ..stmt.expressionstmt import ExpressionStmt
from ..stmt.forstmt import ForStmt
from ..stmt.foreachstmt import ForeachStmt
from ..stmt.whilestmt import WhileStmt
from ..stmt.minrepeatstmt import MinrepeatStmt
from ..stmt.assertstmt import AssertStmt
from ..stmt.continuestmt import ContinueStmt
from ..stmt.breakstmt import BreakStmt
from ..stmt.trystmt import TryStmt
from ..stmt.catchclause import CatchClause
from ..stmt.switchstmt import SwitchStmt
from ..stmt.switchentrystmt import SwitchEntryStmt
from ..stmt.explicitconstructorinvocationstmt import ExplicitConstructorInvocationStmt
from ..stmt.assumestmt import AssumeStmt

from ..expr.variabledeclarationexpr import VariableDeclarationExpr
from ..expr.unaryexpr import UnaryExpr
from ..expr.binaryexpr import BinaryExpr
from ..expr.nameexpr import NameExpr
from ..expr.assignexpr import AssignExpr
from ..expr.integerliteralexpr import IntegerLiteralExpr
from ..expr.stringliteralexpr import StringLiteralExpr
from ..expr.doubleliteralexpr import DoubleLiteralExpr
from ..expr.longliteralexpr import LongLiteralExpr
from ..expr.charliteralexpr import CharLiteralExpr
from ..expr.booleanliteralexpr import BooleanLiteralExpr
from ..expr.methodcallexpr import MethodCallExpr
from ..expr.generatorexpr import GeneratorExpr
from ..expr.objectcreationexpr import ObjectCreationExpr
from ..expr.fieldaccessexpr import FieldAccessExpr
from ..expr.thisexpr import ThisExpr
from ..expr.enclosedexpr import EnclosedExpr
from ..expr.arraycreationexpr import ArrayCreationExpr
from ..expr.arrayinitializerexpr import ArrayInitializerExpr
from ..expr.arrayaccessexpr import ArrayAccessExpr
from ..expr.nullliteralexpr import NullLiteralExpr
from ..expr.qualifiednameexpr import QualifiedNameExpr
from ..expr.conditionalexpr import ConditionalExpr
from ..expr.superexpr import SuperExpr
from ..expr.castexpr import CastExpr
from ..expr.instanceofexpr import InstanceOfExpr
from ..expr.markerannotationexpr import MarkerAnnotationExpr
from ..expr.singlememberannotationexpr import SingleMemberAnnotationExpr
from ..expr.normalannotationexpr import NormalAnnotationExpr
from ..expr.annotationexpr import AnnotationExpr

from ..type.primitivetype import PrimitiveType
from ..type.voidtype import VoidType
from ..type.referencetype import ReferenceType
from ..type.classorinterfacetype import ClassOrInterfaceType

from ..comments.comment import Comment
from ..comments.linecomment import LineComment
from ..comments.javadoccomment import JavadocComment
from ..comments.blockcomment import BlockComment

class SourcePrinter(object):
    def __init__(self, **kwargs):
        self._indentation = kwargs.get('indentation', "    ")
        self._level = kwargs.get('level', 0)
        self._indented = kwargs.get('indented', False)
        self._buf = cStringIO.StringIO()
        
    @v.on("node")
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """

    @v.when(Node)
    def visit(self, n):
        print "Unimplemented node:", n

    @v.when(CompilationUnit)
    def visit(self, n):
        self.printJavaComment(n.comment)

        if n.package: n.package.accep(self)
        for i in n.imports:
            if not i.implicit: i.accept(self)
        for ty in n.types: ty.accept(self)
        return self._buf.getvalue()
        self._buf.close()
        self._buf = cStringIO.StringIO()

        self.printOrphanCommentsEnding(n)
        
    @v.when(ImportDeclaration)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('import ')
        if n.static: self.printt('static ')
        n.name.accept(self)
        if n.asterisk: self.printt('.*')
        self.printLn(';')

        self.printOrphanCommentsEnding(n)

    # body
    @v.when(ClassOrInterfaceDeclaration)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printJavadoc(n.javadoc)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)

        if n.interface: self.printt('interface ')
        else: self.printt('class ')
        self.printt(n.name)

        # typeParameters
        self.printTypeParameters(n.typeParameters)

        # don't print extends Object
        if n.extendsList and \
           (u'Object' not in map(lambda e: e.name, n.extendsList) and len(n.extendsList) == 1):
            self.printt(' extends ')
            self.printSepList(n.extendsList)

        if n.implementsList:
            self.printt(' implements ')
            self.printSepList(n.implementsList)

        self.printLn(' {')
        self.indent()
        self.printMembers(n.members)

        self.printOrphanCommentsEnding(n)

        self.unindent()
        self.printLn('}')

    @v.when(FieldDeclaration)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)

        n.typee.accept(self)
        self.printt(' ')
        n.variable.accept(self)
        self.printLn(';')

    @v.when(MethodDeclaration)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)

        self.printTypeParameters(n.typeParameters)
        if n.typeParameters: self.printt(' ')

        n.typee.accept(self)
        self.printt(' ')
        self.printt(n.name)
        if n.bang: self.printt('!')
        self.printt('(')

        self.printSepList(n.parameters)
        self.printt(')')

        for i in xrange(n.arrayCount): self.printt('[]')
        if n.throws:
            self.printt(' throws ')
            self.printSepList(n.throws)
            
        if not n.body: self.printt(';')
        else:
            self.printt(' ')
            n.body.accept(self)
        self.printLn()

    @v.when(AxiomDeclaration)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)

        self.printt('axiom ')
        n.typee.accept(self)
        self.printt(' ')
        self.printt(n.name)
        self.printt('(')

        self.printSepList(n.parameters)
        self.printt(')')

        if not n.body: self.printt(';')
        else:
            self.printt(' ')
            n.body.accept(self)
        self.printLn()

    @v.when(ConstructorDeclaration)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)

        self.printTypeParameters(n.typeParameters)
        if n.typeParameters: self.printt(' ')

        self.printt(n.name)
        self.printt('(')

        self.printSepList(n.parameters)
        self.printt(')')

        for i in xrange(n.arrayCount): self.printt('[]')
        if n.throws:
            self.printt(' throws ')
            self.printSepList(n.throws)
            
        if not n.body: self.printt(';')
        else:
            self.printt(' ')
            n.body.accept(self)
        self.printLn()

    @v.when(Parameter)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)
        
        n.typee.accept(self)
        self.printt(' ')
        n.idd.accept(self)

    @v.when(AxiomParameter)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)
        
        if n.idd:
            n.typee.accept(self)
            self.printt(' ')
            n.idd.accept(self)
        elif n.method:
            self.printMods(n)
            n.method.typee.accept(self)
            self.printt(' ')
            self.printt(n.method.name)
            if n.method.bang: self.printt('!')
            self.printt('(')
            self.printSepList(n.method.parameters)
            self.printt(')')
            if n.method.body:
                self.printt(' ')
                n.method.body.accept(self)

    @v.when(VariableDeclarator)
    def visit(self, n):
        self.printJavaComment(n.comment)

        n.idd.accept(self)
        if n.init:
            self.printt(' = ')
            n.init.accept(self)

    @v.when(VariableDeclaratorId)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt(n.name)
        for i in xrange(n.arrayCount): self.printt('[]')

    @v.when(AnnotationDeclaration)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)

        self.printt('@interface')
        self.printt(n.name)
        self.printLn(' {')
        self.indent()
        for m in n.members:
            self.printMembers(n.members)
        self.unindent()
        self.printt('}')
        
    @v.when(AnnotationMemberDeclaration)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printMemberAnnotations(n.annotations)
        self.printMods(n)

        n.typee.accept(self)
        self.printt(' ')
        self.printt(n.name)
        self.printt('()')
        if n.defaultValue:
            self.printt(' default ')
            n.defaultValue.accept(self)
        self.printt(';')

    @v.when(MarkerAnnotationExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt('@')
        n.name.accept(self)

    @v.when(SingleMemberAnnotationExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt('@')
        n.name.accept(self)
        self.printt('(')
        n.member.accept(self)
        self.printt(')')

    @v.when(NormalAnnotationExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt('@')
        n.name.accept(self)
        self.printt('(')
        self.printSepList(n.pairs)
        self.printt(')')
        
    # Stmt
    @v.when(BlockStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

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
        self.printJavaComment(n.comment)

        self.printt('return')
        if n.expr:
            self.printt(' ')
            n.expr.accept(self)
        self.printt(';')

    @v.when(IfStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

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

    @v.when(ForeachStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('for (')
        n.var.accept(self)
        self.printt(' : ')
        n.iterable.accept(self)
        self.printt(') ')
        n.body.accept(self)

    @v.when(ForStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('for (')
        if n.init: self.printSepList(n.init)
        self.printt('; ')
        if n.compare: n.compare.accept(self)
        self.printt('; ')
        if n.update: self.printSepList(n.update)
        self.printt(') ')
        n.body.accept(self)

    @v.when(WhileStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('while (')
        if n.condition: n.condition.accept(self)
        self.printt(') ')
        n.body.accept(self)

    @v.when(MinrepeatStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('minrepeat ')
        n.body.accept(self)

    @v.when(ExpressionStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)
        n.expr.accept(self)
        self.printt(';')

    @v.when(AssertStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt("assert ")
        n.check.accept(self)
        if n.msg:
            self.printt(" : ")
            n.msg.accept(self)
        self.printt(";")

    @v.when(AssumeStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt("assume ")
        n.expr.accept(self)
        self.printt(";")
        
    @v.when(ContinueStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt("continue")
        if n.idd:
            self.printt(' {}'.format(n.idd))
        self.printt(";")

    @v.when(BreakStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt("break")
        if n.idd:
            self.printt(' {}'.format(n.idd))
        self.printt(";")

    @v.when(TryStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt("try ")
        if n.resources:
            self.printt('(')
            first = True
            size = len(n.resources)
            for i in xrange(size):
                self.visit(n.resources[i])
                if i < size - 1:
                    self.printLn(';')
                    if first: self.indent()
                first = False
            if size > 1: self.unindent()
            self.printt(")")
        n.tryBlock.accept(self)
        for c in n.catchs: c.accept(self)
        if n.finallyBlock: n.finallyBlock.accept(self)

    @v.when(CatchClause)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt(' catch (')
        n.param.accept(self)
        self.printt(') ')
        n.catchBlock.accept(self)
        
    @v.when(SwitchStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('switch (')
        n.selector.accept(self)
        self.printLn(') {')
        if n.entries:
            self.indent()
            for e in n.entries: e.accept(self)
            self.unindent()
        self.printt('}')

    @v.when(SwitchEntryStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        if n.label:
            self.printt('case ')
            n.label.accept(self)
            self.printt(':')
        else:
            self.printt('default:')
        self.printLn()
        self.indent()
        for s in n.stmts:
            s.accept(self)
            self.printLn()
        self.unindent()

    @v.when(ExplicitConstructorInvocationStmt)
    def visit(self, n):
        self.printJavaComment(n.comment)

        if n.isThis:
            self.printt('this')
        else:
            if n.expr:
                n.expr.accept(self)
                self.printt('.')
            self.printt('super')
        self.printArguments(n.args)
        self.printt(';')

    # Expr
    @v.when(NameExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt(n.name)

    @v.when(QualifiedNameExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        n.qualifier.accept(self)
        self.printt('.')
        self.printt(n.name)
        
    @v.when(VariableDeclarationExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printAnnotations(n.annotations)
        
        n.typee.accept(self)
        self.printt(' ')
        self.printSepList(n.varss)

    @v.when(UnaryExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt(UnaryExpr.PRE_OPS.get(n.op, ''))
        n.expr.accept(self)
        self.printt(UnaryExpr.POST_OPS.get(n.op, ''))

    @v.when(BinaryExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        n.left.accept(self)
        self.printt(' ')
        self.printt(op[n.op.upper()])
        self.printt(' ')
        n.right.accept(self)

    @v.when(GeneratorExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        if n.isHole: self.printt('??')
        else:
            self.printt('{| ')
            self.printSepList(n.exprs)
            self.printt(' |}')

    @v.when(ObjectCreationExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        if n.scope:
            n.scope.accept(self)
            self.printt(".")

        self.printt("new ")
        n.typee.accept(self)
        self.printArguments(n.args)
        if n.anonymousClassBody:
            self.printLn(' {')
            self.indent()
            for m in n.anonymousClassBody:
                print 'm:', m, m.name, type(m)
            self.printMembers(n.anonymousClassBody)
            self.unindent()
            self.printt('}')

    @v.when(AssignExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        n.target.accept(self)
        self.printt(" ")
        self.printt(assignop[n.op.upper()])
        self.printt(' ')
        n.value.accept(self)

    @v.when(MethodCallExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        if n.scope:
            n.scope.accept(self)
            self.printt('.')
        self.printt(n.name)
        self.printArguments(n.args)

    @v.when(FieldAccessExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        n.scope.accept(self)
        self.printt(".")
        n.field.accept(self)
        
    @v.when(ThisExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        if n.classExpr:
            n.classExpr.accept(self)
            self.printt(".")
        self.printt("this")

    @v.when(SuperExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        if n.classExpr:
            n.classExpr.accept(self)
            self.printt('.')
        self.printt('super')
        
    @v.when(EnclosedExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('(')
        if n.inner: n.inner.accept(self)
        self.printt(')')

    @v.when(ArrayCreationExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('new ')
        n.typee.accept(self)
        # TODO
        # List<List<AnnotationExpr>> arraysAnnotations = n.getArraysAnnotations();
        if n.dimensions:
            for d in n.dimensions:
                self.printt('[')
                d.accept(self)
                self.printt(']')
            for c in xrange(n.arrayCount):
                self.printt('[]')
        else:
            for c in xrange(n.arrayCount):
                self.printt('[]')
            self.printt(' ')
            n.initializer.accept(self)

    @v.when(ArrayInitializerExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        self.printt('{')
        self.printSepList(n.values)
        self.printt('}')

    @v.when(ArrayAccessExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)

        n.nameExpr.accept(self)
        self.printt('[')
        n.index.accept(self)
        self.printt(']')

    @v.when(NullLiteralExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt('null')

    @v.when(DoubleLiteralExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt(n.value)

    @v.when(LongLiteralExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt(n.value)

    @v.when(ConditionalExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        n.condition.accept(self)
        self.printt(' ? ')
        n.thenExpr.accept(self)
        self.printt(' : ')
        n.elseExpr.accept(self)

    @v.when(CastExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt('(')
        n.typee.accept(self)
        self.printt(')')
        n.expr.accept(self)
        
    @v.when(BooleanLiteralExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt(n.value)
        
    @v.when(AnnotationExpr)
    def visit(self, n):
        pass
        
    # Type
    @v.when(PrimitiveType)
    def visit(self, n):
        self.printJavaComment(n.comment)
        if n.annotations:
            for a in n.annotations:
                a.accept(self)
                self.printt(' ')
        self.printt(n.name)

    @v.when(IntegerLiteralExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt(n.value)

    @v.when(DoubleLiteralExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt(n.value)

    @v.when(StringLiteralExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt('"')
        self.printt(n.value)
        self.printt('"')

    @v.when(CharLiteralExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt("'")
        self.printt(n.value)
        self.printt("'")

    @v.when(VoidType)
    def visit(self, n):
        self.printJavaComment(n.comment)
        self.printt(n.name)

    @v.when(ReferenceType)
    def visit(self, n):
        self.printJavaComment(n.comment)
        if n.annotations:
            for a in n.annotations:
                a.accept(self)
                self.printt(' ')

        n.typee.accept(self)
        # TODO:
        # List<List<AnnotationExpr>> arraysAnnotations = n.getArraysAnnotations();
        for i in xrange(n.arrayCount):
            self.printt('[')
            if n.values:
                n.values[i].accept(self)
            self.printt(']')

    @v.when(ClassOrInterfaceType)
    def visit(self, n):
        self.printJavaComment(n.comment)
        if n.annotations:
            for a in n.annotations:
                a.accept(self)
                self.printt(' ')

        if n.scope:
            n.scope.accept(self)
            self.printt('.')
        self.printt(n.name)

        if n.isUsingDiamondOperator():
            self.printt('<>')
        else:
            self.printTypeArgs(n.typeArgs())

    @v.when(TypeParameter)
    def visit(self, n):
        self.printJavaComment(n.comment)

        # annotations
        if n.annotations:
            for a in n.annotations:
                a.accept(self)
                self.printt(' ')

        self.printt(n.name)
        if n.typeBound:
            self.printSepList(n.typeBound, '&')

    @v.when(InstanceOfExpr)
    def visit(self, n):
        self.printJavaComment(n.comment)
        n.expr.accept(self)
        self.printt(' instanceof ')
        n.typee.accept(self)
        
    # comments
    @v.when(Comment)
    def visit(self, n):
        n.accept(self)

    @v.when(LineComment)
    def visit(self, n):
        self.printt('//')
        tmp = n.content.replace('\r', ' ')
        tmp = tmp.replace('\n', ' ')
        self.printLn(tmp)

    @v.when(JavadocComment)
    def visit(self, n):
        self.printt('/**')
        self.printt(n.content)
        self.printLn('*/')

    @v.when(BlockComment)
    def visit(self, n):
        self.printt('/*')
        self.printt(n.content)
        self.printLn('*/')

    def printJavadoc(self, javadoc):
        if javadoc: javadoc.accept(self)

    def printJavaComment(self, javacomment):
        if javacomment: javacomment.accept(self)

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

    def printMembers(self, members):
        for m in members: m.accept(self)
        
    def printMods(self, mods):
        if TypeDeclaration.isHarness(mods): self.printt('harness ')
        if TypeDeclaration.isPublic(mods): self.printt('public ')
        if TypeDeclaration.isPrivate(mods): self.printt('private ')
        if TypeDeclaration.isProtected(mods): self.printt('protected ')
        if TypeDeclaration.isAbstract(mods): self.printt('abstract ')
        if TypeDeclaration.isStatic(mods): self.printt('static ')
        if TypeDeclaration.isFinal(mods): self.printt('final ')
        if TypeDeclaration.isOptional(mods): self.printt('optional ')

    def printTypeArgs(self, args):
        self.printTypeParameters(args)
        
    def printTypeParameters(self, args):
        if args:
            self.printt('<')
            self.printSepList(args)
            self.printt('>')
        
    def indent(self): self._level += 1
    def unindent(self): self._level -= 1
    
    def makeIndent(self):
        for i in xrange(self._level): self._buf.write(self._indentation)

    def printt(self, arg):
        if not self._indented:
            self.makeIndent()
            self._indented = True
        self._buf.write(arg)

    def printLn(self, arg=None):
        if arg:
            self.printt(arg)
        self._buf.write('\n')
        self._indented = False

    def printOrphanCommentsEnding(self, n):
        for c in n.childrenNodes:
            if isinstance(c, Comment):
                c.accept(self)

    def printMemberAnnotations(self, annotations):
        if annotations:
            for a in annotations:
                a.accept(self)
                self.printLn()

    def printAnnotations(self, annotations):
        if annotations:
            for a in annotations:
                a.accept(self)
                self.printt(' ')
                
    @property
    def buf(self): return self._buf
    @buf.setter
    def buf(self, v): self._buf = v
