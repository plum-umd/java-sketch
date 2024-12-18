#!/usr/bin/env python

def _import():
    from .classorinterfacedeclaration import ClassOrInterfaceDeclaration
    from .fielddeclaration import FieldDeclaration
    from .methoddeclaration import MethodDeclaration
    from .constructordeclaration import ConstructorDeclaration
    from .emptymemberdeclaration import EmptyMemberDeclaration
    from .initializerdeclaration import InitializerDeclaration
    from .parameter import Parameter
    from .bodydeclaration import BodyDeclaration
    from .variabledeclarator import VariableDeclarator
    from .variabledeclaratorid import VariableDeclaratorId
    from .axiomdeclaration import AxiomDeclaration
    from .axiomparameter import AxiomParameter

    from ..type.type import Type
    from ..type.classorinterfacetype import ClassOrInterfaceType
    from ..type.primitivetype import PrimitiveType
    from ..type.referencetype import ReferenceType
    from ..type.voidtype import VoidType

    from ..stmt.blockstmt import BlockStmt

    from ..expr.integerliteralexpr import IntegerLiteralExpr
    from ..expr.doubleliteralexpr import DoubleLiteralExpr
    from ..expr.stringliteralexpr import StringLiteralExpr
    from ..expr.longliteralexpr import LongLiteralExpr
    from ..expr.nullliteralexpr import NullLiteralExpr
    from ..expr.charliteralexpr import CharLiteralExpr
    from ..expr.booleanliteralexpr import BooleanLiteralExpr
    from ..expr.literalexpr import LiteralExpr
    from ..expr.nameexpr import NameExpr
    from ..expr.binaryexpr import BinaryExpr
    from ..expr.assignexpr import AssignExpr
    from ..expr.generatorexpr import GeneratorExpr
    from ..expr.objectcreationexpr import ObjectCreationExpr
    from ..expr.fieldaccessexpr import FieldAccessExpr
    from ..expr.methodcallexpr import MethodCallExpr
    from ..expr.arraycreationexpr import ArrayCreationExpr
    from ..expr.arrayinitializerexpr import ArrayInitializerExpr
    from ..expr.arrayaccessexpr import ArrayAccessExpr
    from ..expr.arrayrangeaccessexpr import ArrayRangeAccessExpr
    from ..expr.enclosedexpr import EnclosedExpr
    from ..expr.conditionalexpr import ConditionalExpr
    from ..expr.castexpr import CastExpr
    from ..expr.unaryexpr import UnaryExpr
    from ..expr.annotationexpr import AnnotationExpr
    from ..expr.markerannotationexpr import MarkerAnnotationExpr
    from ..expr.singlememberannotationexpr import SingleMemberAnnotationExpr
    from ..expr.normalannotationexpr import NormalAnnotationExpr
    from ..expr.thisexpr import ThisExpr
    from ..expr.instanceofexpr import InstanceOfExpr
    
    return locals()

