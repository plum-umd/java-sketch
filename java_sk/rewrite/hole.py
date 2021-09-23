import logging

from ast.visit import visit as v
from ast import Modifiers
from ast.node import Node
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.typedeclaration import TypeDeclaration
from ast.expr.generatorexpr import GeneratorExpr

from ast.stmt.ifstmt import IfStmt
from ast.type.primitivetype import PrimitiveType
from ast.body.variabledeclarator import VariableDeclarator
from ast.expr.nameexpr import NameExpr

from ast.utils.utils import replace_node

"""
class A {
    ... foo() {
        if (??) { doXoptional }
        if (??) { doYoptional }
    }
}

  =>

class A {
    static int e_h1 = ??;
    static int e_h2 = ??;
    ... foo() {
        if (A.e_h1) { doXoptional }
        if (A.e_h2) { doYoptional }
    }
}
"""


class EHole(object):

    # to avoid name conflict, use fresh counter as suffix
    __cnt = 0

    @classmethod
    def fresh_cnt(cls):
        cls.__cnt = cls.__cnt + 1
        return cls.__cnt

    def __init__(self):
        self._cur_mtd = None
        self._cur_cls = None
        self._visiting_s = False

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes: c.accept(self)

    @v.when(FieldDeclaration)
    def visit(self, node):
        # to avoid introducing another hole variable
        # reset the context statement
        self._visiting_s = False
        for c in node.childrenNodes: c.accept(self)

    @v.when(ClassOrInterfaceDeclaration)
    def visit(self, node):
        self._cur_cls = node
        for c in node.childrenNodes: c.accept(self)
        self._cur_cls = None

    @v.when(MethodDeclaration)
    def visit(self, node):
        self._cur_mtd = node
        if node.body:
            self._visiting_s = True
        for c in node.childrenNodes: c.accept(self)
        self._cur_mtd = None

    @v.when(GeneratorExpr)
    def visit(self, node):
        # avoid editing field initializing Expression
        if not self._visiting_s:
            return node
        # avoid editing hole(s) in a method-level generator
        if TypeDeclaration.isGenerator(self._cur_mtd):
            return node
        

        # Determine hole type by context
        # On if statement conditions, always use boolean
        if type(node.parentNode) == IfStmt and \
            node.parentNode.condition == node:
            type_name = "boolean"
        # On variable declearators, carry decleared type
        if type(node.parentNode) == VariableDeclarator:
            type_name = node.parentNode.typee.name
        # Default is int
        else:
            type_name = "int"

        cls = self._cur_cls
        hname = u"e_h{}".format(EHole.fresh_cnt())

        replace_node(node, NameExpr(name=hname))

        hole = FieldDeclaration(type_obj=PrimitiveType(type_name=type_name),
                modifier_bits=Modifiers['ST'],
                var_decl_obj=VariableDeclarator(
                    id_str=hname,
                    type_obj=PrimitiveType(type_name=type_name),
                    init_obj=node
                ))
        cls.prepend_member(hole)
        hole.add_parent_post(cls)

        logging.debug(
            "introducing e_hole type {} {} @ {}".format(type_name, hname, self._cur_mtd.sig()))


"""
class A {
    ty1 fld1; // fid 1
    ty2 fld2; // fid 2
}
class B {
    ty3 fld3; // fid 3
    ty4 fld4; // fid 4
    ... foo(A a) {
        ...
        this.?? = a.??;
    }
}

  =>

class B {
    ...
    static int fld_H1 = {| 1 | 2 |};
    static int fld_H2 = {| 3 | 4 |};
    ... foo(A a) { ...

        // read
        Object fld_h1;
        if (fld_H1 == 1) { fld_h1 = a.fld1; }
        else if (fld_H1 == 2) { fld_h1 = a.fld2; }

        // write
        if (fld_H2 == 3) { this.fld3 = fld_h1; }
        else if (fld_H2 == 4) { this.fld4 = fld_h2; }
    }
}
"""


class FHole(object):

    def __init__(self): pass

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes: c.accept(self)

"""
class A {
    int foo() { ... } // mid 1
    int bar() { ... } // mid 2
}
class B {
    B moo() { ... }   // mid 3
    B baa() { ... }   // mid 4
    void baz(int arg) { ... } // mid 5
}
class Test {
    ... f {
        A a; ...
        int x = a.??(); // (1)
        B b; ...
        B y = b.??(); // (2)
        b.??(x); // (3)
    }
}

  =>

class Test {
    static int mtd_H1 = {| 1 | 2 |};
    static int mtd_H2 = {| 3 | 4 |};
    static int mtd_H3 = {| 5 |}; // due to signature
    ... f {
        ...
        int r_mtd_h1; // (1)
        if (mtd_H1 == 1) { r_mtd_h1 = a.foo(); }
        else if (mtd_H1 == 2) { r_mtd_h1 = a.bar(); }
        int x = r_mtd_h1;

        B r_mtd_h2; // (2)
        if (mtd_H2 == 3) { r_mtd_h2 = b.moo(); }
        else if (mtd_H2 == 4) { r_mtd_h2 = b.baa(); }
        B y = r_mtd_h2;

        // (3)
        if (mtd_H3 == 5) { b.baz(); }
    }
}
"""


class MHole(object):

    def __init__(self): pass

    @v.on("node")
    def visit(self, node):
        """
        This is the generic method to initialize the dynamic dispatcher
        """

    @v.when(Node)
    def visit(self, node):
        for c in node.childrenNodes: c.accept(self)