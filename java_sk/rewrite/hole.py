import logging

import lib.const as C
import lib.visit as v

from ..meta.program import Program
from ..meta.clazz import Clazz
from ..meta.method import Method
from ..meta.field import Field
from ..meta.statement import Statement
from ..meta.expression import Expression, to_expression

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
    self._visiting_s = False

  @v.on("node")
  def visit(self, node):
    """
    This is the generic method to initialize the dynamic dispatcher
    """

  @v.when(Program)
  def visit(self, node): pass

  @v.when(Clazz)
  def visit(self, node): pass

  @v.when(Field)
  def visit(self, node):
    # to avoid introducing another hole variable
    # reset the context statement
    self._visiting_s = False

  @v.when(Method)
  def visit(self, node):
    self._cur_mtd = node
    if node.body:
      self._visiting_s = True

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node):
    # in case of visiting field initializing Expression
    if not self._visiting_s: return node

    if node.kind == C.E.HOLE:
      cls = self._cur_mtd.clazz
      hname = u"e_h{}".format(EHole.fresh_cnt())
      hole = Field(clazz=cls, mods=[C.mod.ST], typ=C.J.i, name=hname, init=node)
      cls.add_fld(hole)
      logging.debug("introducing e_hole {} @ {}".format(hname, self._cur_mtd.signature))
      return to_expression(hname)

    return node


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

  @v.when(Program)
  def visit(self, node): pass

  @v.when(Clazz)
  def visit(self, node): pass

  @v.when(Field)
  def visit(self, node): pass

  @v.when(Method)
  def visit(self, node): pass

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node): return node


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

  @v.when(Program)
  def visit(self, node): pass

  @v.when(Clazz)
  def visit(self, node): pass

  @v.when(Field)
  def visit(self, node): pass

  @v.when(Method)
  def visit(self, node): pass

  @v.when(Statement)
  def visit(self, node): return [node]

  @v.when(Expression)
  def visit(self, node): return node

