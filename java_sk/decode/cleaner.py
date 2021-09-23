import logging

from ast.visit import visit as v
from ast.body.methoddeclaration import MethodDeclaration
from ast.expr.annotationexpr import AnnotationExpr
from ast.body.typedeclaration import TypeDeclaration

from ast.node import Node

from ast.utils.utils import drop_node

class Cleaner(object):

    def __init__(self):
        pass

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes:
            c.accept(self)

    @v.when(MethodDeclaration)
    def visit(self, node):
        if TypeDeclaration.isGenerator(node):
            drop_node(node)
            return
        for c in node.childrenNodes:
            c.accept(self)
    
    @v.when(AnnotationExpr)
    def visit(self, node):
        if node.name.name == u"JavaCodeGen":
            drop_node(node)