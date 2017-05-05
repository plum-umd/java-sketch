#!/usr/bin/env python

def _import():
    from ..body.methoddeclaration import MethodDeclaration
    from ..body.variabledeclarator import VariableDeclarator

    from .nameexpr import NameExpr
    from .qualifiednameexpr import QualifiedNameExpr
    from .unaryexpr import UnaryExpr
    from .binaryexpr import BinaryExpr
    from .assignexpr import AssignExpr
    from .fieldaccessexpr import FieldAccessExpr
    from .thisexpr import ThisExpr
    from .methodcallexpr import MethodCallExpr
    from .enclosedexpr import EnclosedExpr
    from .generatorexpr import GeneratorExpr
    from .arraycreationexpr import ArrayCreationExpr
    from .arrayinitializerexpr import ArrayInitializerExpr
    from .arrayaccessexpr import ArrayAccessExpr
    from .objectcreationexpr import ObjectCreationExpr
    from .conditionalexpr import ConditionalExpr
    from .superexpr import SuperExpr
    from .castexpr import CastExpr
    from .integerliteralexpr import IntegerLiteralExpr
    from .stringliteralexpr import StringLiteralExpr
    from .nullliteralexpr import NullLiteralExpr
    from .doubleliteralexpr import DoubleLiteralExpr
    from .charliteralexpr import CharLiteralExpr
    from .booleanliteralexpr import BooleanLiteralExpr
    from .longliteralexpr import LongLiteralExpr
    from .instanceofexpr import InstanceOfExpr

    from ..type.primitivetype import PrimitiveType
    from ..type.referencetype import ReferenceType
    from ..type.classorinterfacetype import ClassOrInterfaceType

    return locals()
