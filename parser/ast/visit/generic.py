#!/usr/bin/env python

import visit as v

from ..node import Node

class GenericVisitor(object):
    def __init__(self, f):
        # f is a function that takes a node
        self._f = f
        
    @v.on("node")
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """

    @v.when(Node)
    def visit(self, node):
        self._f(node)
        for c in node.childrenNodes: c.accept(self)

    @property
    def f(self): return self._f
    @f.setter
    def f(self, v): self._f = v
