#!/usr/bin/env python

def _import():
    from .ifstmt import IfStmt
    from .blockstmt import BlockStmt
    from .expressionstmt import ExpressionStmt
    from .returnstmt import ReturnStmt
    from .assertstmt import AssertStmt
    from .forstmt import ForStmt
    from .whilestmt import WhileStmt
    from .emptystmt import EmptyStmt
    from .continuestmt import ContinueStmt
    from .breakstmt import BreakStmt
    from .trystmt import TryStmt
    from .catchclause import CatchClause
    from .switchstmt import SwitchStmt
    from .switchentrystmt import SwitchEntryStmt
    from .explicitconstructorinvocationstmt import ExplicitConstructorInvocationStmt
    from .assumestmt import AssumeStmt
    from .minrepeatstmt import MinrepeatStmt

    from ..expr.unaryexpr import UnaryExpr
    from ..expr.binaryexpr import BinaryExpr
    from ..expr.nameexpr import NameExpr
    from ..expr.integerliteralexpr import IntegerLiteralExpr
    from ..expr.variabledeclarationexpr import VariableDeclarationExpr
    from ..expr.assignexpr import AssignExpr
    from ..expr.methodcallexpr import MethodCallExpr
    from ..expr.fieldaccessexpr import FieldAccessExpr
    from ..expr.stringliteralexpr import StringLiteralExpr
    from ..expr.nullliteralexpr import NullLiteralExpr
    from ..expr.objectcreationexpr import ObjectCreationExpr
    from ..expr.generatorexpr import GeneratorExpr
    from ..expr.superexpr import SuperExpr
    from ..expr.booleanliteralexpr import BooleanLiteralExpr
    from ..expr.instanceofexpr import InstanceOfExpr
    from ..expr.arrayaccessexpr import ArrayAccessExpr
    from ..expr.thisexpr import ThisExpr
    from ..expr.castexpr import CastExpr

    from ..body.parameter import Parameter

    return locals()
