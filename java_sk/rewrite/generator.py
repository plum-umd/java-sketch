import copy
from ast.stmt.returnstmt import ReturnStmt
from ast.stmt.expressionstmt import ExpressionStmt
from ast.expr.methodcallexpr import MethodCallExpr
import logging

from ast.visit import visit as v
from ast.node import Node
from ast.body.typedeclaration import TypeDeclaration
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.stmt.blockstmt import BlockStmt
from ast import Modifiers
from ast.utils.utils import replace_node, replace_child

"""
generator class Automaton { body_of_Automaton }

class RegularLanguage extends Automaton { ... }
class DBConnection {
    class Monitor extends Automaton { ... }
}

  =>

class Automaton1 { copy_of_body_of_Automaton }
class Automaton2 { copy_of_body_of_Automaton }

class RegularLanague extends Automaton1 { ... }
class DBConnection {
    class Monitor extends Automaton2 { ... }
}
"""


class CGenerator(object):

    # to avoid name conflict, use fresh counter as suffix
    __cnt = 0

    @classmethod
    def fresh_cnt(cls):
        cls.__cnt = cls.__cnt + 1
        return cls.__cnt

    def __init__(self):
        self._cgens = []

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes:
            c.accept(self)

    @v.when(ClassOrInterfaceDeclaration)
    def visit(self, node):
        if TypeDeclaration.isGenerator(node):
            raise NotImplementedError
        for c in node.childrenNodes:
            c.accept(self)

    # @v.when(Program)
    # def visit(self, node):
    #     self._pgr = node
    #     # collect class-level generators
    #     for cls in util.flatten_classes(node.classes, "inners"):
    #         if C.mod.GN in cls.mods:
    #             logging.debug("found class generator: {}".format(cls.name))
    #             self._cgens.append(cls)

    # @v.when(Clazz)
    # def visit(self, node):
    #     if not node.sup:
    #         return
    #     sup = class_lookup(node.sup)
    #     if sup not in self._cgens:
    #         return

    #     # specialize the class generator
    #     specialized_cls_name = u"{}{}".format(node.sup, CGenerator.fresh_cnt())
    #     # deep copy
    #     specialized_cls = copy.deepcopy(sup)
    #     # rename <init>s
    #     for init in specialized_cls.inits:
    #         init.name = specialized_cls_name
    #         init.typ = specialized_cls_name
    #     # rename the class
    #     specialized_cls.name = specialized_cls_name
    #     register_class(specialized_cls)
    #     self._pgr.add_classes([specialized_cls])

    #     node.sup = specialized_cls_name
    #     logging.debug("specializing {} for {}".format(
    #         specialized_cls_name, node.name))


"""
class A {
  static generator foo(...) {
    ... foo(...); // may be recursive
  }
}

class X {
  ... bar(...) {
    ... A.foo(...);
    ... A.foo(...);
  }
}

  =>

class A {
  ...
  static foo1(...) {
    return foo(...); // delegation
  }
  static foo2(...) {
    return foo(...); // delegation
  }
}

class X {
  ... bar(...) {
    ... A.foo1(...);
    ... A.foo2(...);
  }
}
"""


class MGenerator(object):

    # to avoid name conflict, use fresh counter as suffix
    __cnt = 0

    @classmethod
    def fresh_cnt(cls):
        cls.__cnt = cls.__cnt + 1
        return cls.__cnt

    def __init__(self):
        # { mname: mtd } for easier lookup
        self._mgens = None
        self._cur_mtd = None
        self._cur_cls = None
        self._added_mtds = set()

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes:
            c.accept(self)

    @v.when(ClassOrInterfaceDeclaration)
    def visit(self, node):
        self._cur_cls = node
        # Generators should be local to each class, for now
        self._mgens = {}
        for m in node.members:
            if isinstance(m, MethodDeclaration) and TypeDeclaration.isGenerator(m):
                self._mgens[m.name] = m
        for c in node.childrenNodes:
            c.accept(self)

    @v.when(MethodDeclaration)
    def visit(self, node):
        self._cur_mtd = node
        for c in node.childrenNodes:
            c.accept(self)
    
    @v.when(MethodCallExpr)
    def visit(self, node):
        callee = node.name
        if not callee in self._mgens:
            for c in node.childrenNodes:
                c.accept(self)
            return
        # Avoid calls inside a specialized method
        if self._cur_mtd.name in self._added_mtds:
            return
        # Avoid calls inside a generator
        if TypeDeclaration.isGenerator(self._cur_mtd):
            return
        
        mgen = self._mgens[callee]
        specialized_mtd_name = u"{}{}".format(callee, MGenerator.fresh_cnt())
        self._added_mtds.add(specialized_mtd_name)
        new_modifiers = mgen.modifiers & (~ Modifiers['GN'])
        specialized_mtd = mgen.clone({
            u'name': specialized_mtd_name,
            u'modifiers': new_modifiers,
        })


        # TODO: Below are code to generate delegated calls to the real generator
        # in the specialized functions. To handle recursive generators, these
        # delegations are needed, and reconstruction of the generated function
        # from sketch output is required in the decode module.
        # Currently due to the lack of such reconstruction techniques, we are
        # taking a different approach of inlining the real generator into
        # specialized functions, this way the holes in them would be rewritten
        # into named holes seperately and then populated by the decode module
        # later after synthesis. But this approach would lack the ability to
        # handle recursive and more complex generators


        # delegated_call = node.clone()
        # new_args = [p.idd.to_name_expr() for p in specialized_mtd.parameters]
        # for old_arg, new_arg in zip(delegated_call.args, new_args):
        #     replace_child(old_arg, new_arg)
        # delegated_call.args = new_args

        # body = BlockStmt()
        # if mgen.typee.name == u'void':
        #     stmt = ExpressionStmt()
        # else:
        #     stmt = ReturnStmt()
        # stmt.childrenNodes.append(delegated_call)
        # stmt.expr = delegated_call
        # body.childrenNodes.append(stmt)
        # body.stmts.append(stmt)

        # replace_child(specialized_mtd.body, body)
        # specialized_mtd.body = body

        new_call = node.clone({
            u"name": specialized_mtd_name
        })
        replace_node(node, new_call)

        self._cur_cls.add_member(specialized_mtd)
        specialized_mtd.add_parent_post(self._cur_cls)
