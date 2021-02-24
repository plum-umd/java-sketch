import copy
import logging

from ast.visit import visit as v
from ast.node import Node
from ast.body.typedeclaration import TypeDeclaration
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.methoddeclaration import MethodDeclaration

# from .. import util
# from ..meta import class_nonce, register_class, class_lookup
# from ..meta.program import Program
# from ..meta.clazz import Clazz
# from ..meta.method import Method
# from ..meta.field import Field
# from ..meta.statement import Statement, to_statements
# from ..meta.expression import Expression, to_expression

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
        for c in node.childrenNodes: c.accept(self)

    @v.when(ClassOrInterfaceDeclaration)
    def visit(self, node):
        if TypeDeclaration.isGenerator(node):
            raise NotImplementedError
        for c in node.childrenNodes: c.accept(self)


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
        self._mgens = {}
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
        if TypeDeclaration.isGenerator(node):
            raise NotImplementedError
        for c in node.childrenNodes: c.accept(self)

    # @v.when(Program)
    # def visit(self, node):
    #     # collect method-level generators
    #     for cls in util.flatten_classes(node.classes, "inners"):
    #         for mtd in cls.mtds:
    #             if mtd.is_generator:
    #                 logging.debug(
    #                     "found method generator: {}.{}".format(cls.name, mtd.name))
    #                 self._mgens[mtd.name] = mtd

    # @v.when(Method)
    # def visit(self, node):
    #     self._cur_mtd = node

    # @v.when(Expression)
    # def visit(self, node):
    #     if node.kind != C.E.CALL:
    #         return node

    #     l_callee = unicode(node.f).split('.')
    #     u_callee = l_callee[-1]
    #     if u_callee not in self._mgens:
    #         return node
    #     # avoid recursive calls inside a method generator
    #     if u_callee == self._cur_mtd.name:
    #         return node
    #     # avoid calls inside a specialized method
    #     if hasattr(self._cur_mtd, "generator"):
    #         return node

    #     mgen_mtd = self._mgens[u_callee]
    #     # specialize the method generator
    #     specialized_mtd_name = u"{}{}".format(u_callee, MGenerator.fresh_cnt())

    #     _mods = list(set(mgen_mtd.mods) - set([C.mod.GN]))
    #     specialized_mtd = Method(clazz=mgen_mtd.clazz, name=specialized_mtd_name,
    #                              mods=_mods, typ=mgen_mtd.typ, params=mgen_mtd.params)
    #     # associate the method generator, for easier decoding
    #     setattr(specialized_mtd, "generator", mgen_mtd)

    #     # delegate the call
    #     args = u", ".join(mgen_mtd.param_vars)
    #     delegation = u"{}({});".format(u_callee, args)
    #     if mgen_mtd.typ != C.J.v:  # i.e., has a return value
    #         delegation = u"return {}".format(delegation)
    #     specialized_mtd.body = to_statements(specialized_mtd, delegation)

    #     mgen_mtd.clazz.add_mtd(specialized_mtd)

    #     # replace the callee, e.g., foo -> foo1
    #     logging.debug("specializing {} to {}".format(
    #         u_callee, specialized_mtd_name))
    #     n_callee = u'.'.join(l_callee[:-1] + [specialized_mtd_name])
    #     node.f = to_expression(n_callee)

    #     return node
