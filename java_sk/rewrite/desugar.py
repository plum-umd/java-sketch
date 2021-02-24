# import logging


from ast.visit import visit as v
from ast.node import Node
from ast.body.methoddeclaration import MethodDeclaration
from ast.stmt.minrepeatstmt import MinrepeatStmt


class Desugar(object):

    def __init__(self):
        self._cur_mtd = None

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes: c.accept(self)

    @v.when(MethodDeclaration)
    def visit(self, node):
        self._cur_mtd = node
        for c in node.childrenNodes: c.accept(self)
    
    @v.when(MinrepeatStmt)
    def visit(self, node):
        raise NotImplementedError

    # Old impl
    # @v.when(Statement)
    # def visit(self, node):
    #     if node.kind == C.S.MINREPEAT:
    #         b = '\n'.join(map(str, node.b))
    #         body = u""
    #         for i in xrange(9):  # TODO: parameterize
    #             body += u"""
    #       if (??) {{ {} }}
    #     """.format(b)
    #         logging.debug(
    #             "desugaring minrepeat @ {}".format(self._cur_mtd.name))
    #         return to_statements(self._cur_mtd, body)

    #     return [node]
