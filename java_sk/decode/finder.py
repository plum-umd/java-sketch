from ast.body.variabledeclarator import VariableDeclarator
import logging

from ast.visit import visit as v

from ast.node import Node
from ast.expr.generatorexpr import GeneratorExpr
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration


"""
Finding hole declarations in variable declarators
"""
class HFinder(object):

    def __init__(self):
        self._holes = []
        self._cur_class = None
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
        self._cur_class = node
        for c in node.childrenNodes: c.accept(self)

    @v.when(VariableDeclarator)
    def visit(self, node):
        if isinstance(node.init, GeneratorExpr) and node.init.isHole:
            logging.debug("named hole found: {}.{}".format(self._cur_class.fullname, node.name))
            node.class_name = self._cur_class.name
            self._holes.append(node) 



"""
Finding regex generators {| e* |}
"""
class EGFinder(object):

    def __init__(self):
        self._egens = []
        self._cur_class = None

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
        self._cur_class = node
        for c in node.childrenNodes: c.accept(self)

    @v.when(VariableDeclarator)
    def visit(self, node):
        if isinstance(node.init, GeneratorExpr) and not node.init.isHole:
            logging.debug("regex generator found: {}.{}".format(self._cur_class.fullname, node.name))
            node.class_name = self._cur_class.name
            self._egens.append(node) 

