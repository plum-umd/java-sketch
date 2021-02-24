import logging

from ast.visit import visit as v

from ast.node import Node
from ast.expr.generatorexpr import GeneratorExpr
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.methoddeclaration import MethodDeclaration


"""
Finding hole declarations
"""
class HFinder(object):

    def __init__(self):
        self._holes = []
        self._cur_class = None
        self._cur_method = None 
    @property
    def holes(self):
        return self._holes

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes: c.accept(self)

    @v.when(ClassOrInterfaceDeclaration)
    def visit(self, node):
        self._cur_class = node.name
        for c in node.childrenNodes: c.accept(self)

    @v.when(MethodDeclaration)
    def visit(self, node):
        self._cur_method = node.name
        for c in node.childrenNodes: c.accept(self)

    @v.when(GeneratorExpr)
    def visit(self, node):
        if node.isHole:
            logging.debug("hole@: {}.{}".format(self._cur_class, self._cur_method))
            self._holes.append(node)


"""
Finding regex generators {| e* |}
"""
class EGFinder(object):

    def __init__(self):
        self._egens = []
        self._cur_class = None
        self._cur_method = None

    @property
    def egens(self):
        return self._egens

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes: c.accept(self)

    @v.when(ClassOrInterfaceDeclaration)
    def visit(self, node):
        self._cur_class = node.name
        for c in node.childrenNodes: c.accept(self)

    @v.when(MethodDeclaration)
    def visit(self, node):
        self._cur_method = node.name
        for c in node.childrenNodes: c.accept(self)

    @v.when(GeneratorExpr)
    def visit(self, node):
        if node.isHole:
            logging.debug("generator@: {}.{}".format(self._cur_class, self._cur_method))
            self._egens.append(node)
