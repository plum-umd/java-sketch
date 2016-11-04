def imports():
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

JAVA_TYPES = {u'int':u'int',u'byte':u'byte',u'short':u'short',u'long':u'long',u'double':u'double',
            u'Byte':'Byte',u'Short':u'Short',u'Long':u'Long',u'Int':u'Integer'}
SKETCH_TYPES = {u'boolean':u'bit', u'this':'self'}
