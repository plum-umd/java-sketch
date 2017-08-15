#!/usr/bin/env python

from . import _import

from .. import Modifiers

from .bodydeclaration import BodyDeclaration

from ..stmt.switchstmt import SwitchStmt
from ..stmt.blockstmt import BlockStmt

# This is just going to be a child of MethodDeclaration and allow for special handling of
# the switch statements
class Xform(BodyDeclaration):
    def __init__(self, kwargs={}):
        super(Xform, self).__init__(kwargs)
        locs = _import()

        # SwitchStmt stmt - not sure if this is the best approach but for now it makes sense.
        s = kwargs.get(u'stmt', {})
        self._stmt = SwitchStmt(s) if s else None

        # this might not make sense but each xform has a type which corresponds to the
        # type it is switching on
        typdct = kwargs.get(u'type')
        self._type = locs[typdct[u'@t']](typdct) if typdct else None
        self.add_as_parent([self.stmt])

    @property
    def stmt(self): return self._stmt
    @stmt.setter
    def stmt(self, v): self._stmt = v

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    # this is just a helper cuz I'm not about having this all over the place
    @staticmethod
    def gen_xform(cls, name, adt_mtds, params):
        from .methoddeclaration import MethodDeclaration
        # create a switch dictionary
        entries = []
        for a in adt_mtds:
            entries.append({u'@t':u'SwitchEntryStmt',
                            u'label':{u'@t':u'NameExpr',u'name':a.name.capitalize(),},},)
        switch = {u'@t':u'SwitchStmt', u'selector':{u'@t':u'NameExpr',u'name':u'self'},
                  u'entries':{u'@e':entries,},}
        xform = {u'@t':u'Xform',u'stmt':switch,u'name':name,
                 u'type':{u'@t':u'ClassOrInterfaceType',u'name':str(cls),},}
        ret_none = {u'@t':u'ReturnStmt', u'expr': {u'@t':u'LiteralExpr', u'name':u'null',},}
        return MethodDeclaration({u'type':{u'@t':u'ClassOrInterfaceType',u'name':u'Object',},
                                  u'name':name,u'adtType':True, u'modifiers':Modifiers[u'AT'],
                                  u'body':{u'@t':u'BlockStmt',
                                           u'stmts':{u'@e':[xform, ret_none],},},
                                  u'parameters':{u'@e':params},},)

    # cases should be a list of NameExprs representing the tree of cases
    # body is the body to fill in for that case
    def add_body(self, cases, body):
        # i dont think i know what this means yet...but it's probably not good
        if len(cases) == 0:
            raise Exception('Length of cases == 0')
        for s in self.stmt.entries:
            if str(s.label) == cases[0]:
                if len(cases) == 1:
                    if s.stmts:
                        raise Exception('Are we overwriting an axiom??')
                    b = BlockStmt()
                    body = [body] if not isinstance(body, list) else body
                    b.stmts = body
                    s.stmts = [b]
                    b.add_parent_post(s, True)
                    map(lambda s: s.add_parent_post(b), body)

    def __str__(self): return self._name
