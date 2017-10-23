#!/usr/bin/env python

from . import _import

from .. import Modifiers

from .bodydeclaration import BodyDeclaration

from ..stmt.switchstmt import SwitchStmt
from ..stmt.blockstmt import BlockStmt
from ..stmt.expressionstmt import ExpressionStmt
from ..stmt.returnstmt import ReturnStmt
from ..expr.conditionalexpr import ConditionalExpr
from ..expr.binaryexpr import BinaryExpr

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
    def gen_switch(self, adt_mtds, depth):
        entries = []
        for a in adt_mtds:
            entries.append({u'@t':u'SwitchEntryStmt',
                            u'label':{u'@t':u'NameExpr',
                                      u'name':a.name.capitalize(),},},)

        slf = u'self'+(u'_self'*depth)
        slf_dot = (u'self_'*(depth-1))+u'self.self'

        assn = {u'@t':u'AssignExpr',
                u'target':{u'@t':u'LiteralExpr', u'name':slf,},
                u'value':{u'@t':u'LiteralExpr', u'name':slf_dot,},
                u'op':{u'name':u'ASSIGN',},}

        assn_expr = {u'@t':u'ExpressionStmt',
                     u'expr':assn,}
        
        vdecor = {u'@t':u'VariableDeclarator',
                  u'id':{u'@t':u'VariableDeclaratorId', u'name':slf,},
                  u'type':{u'@t':u'ClassOrInterfaceType',u'name':str(self.typee),},}

        vdec = {u'@t':u'VariableDeclarationExpr',
                u'type':{u'@t':u'ClassOrInterfaceType',u'name':str(self.typee),},
                u'vars':{u'@e':[vdecor],},}

        vdec_expr = {u'@t':u'ExpressionStmt',
                     u'expr':vdec,}
        
        switch = {u'@t':u'SwitchStmt',
                  u'selector':{u'@t':u'NameExpr',u'name':slf},
                  u'entries':{u'@e':entries,},}

        xform = {u'@t':u'Xform',u'stmt':switch,u'name':self.name,
                 u'type':{u'@t':u'ClassOrInterfaceType',u'name':self.name,},}
        
        block = BlockStmt({u'@t':u'BlockStmt',
                           u'stmts':{u'@e':[vdec_expr, assn_expr, xform],},},)
        
        return block

    def build_switch(self, cases, body, adt_mtds, depth, switch):
        new_switch = None
        if not switch:
            new_block = self.gen_switch(adt_mtds, depth)
            new_switch = new_block.stmts[2]
        else:
            new_switch = switch
            
        for s in new_switch.stmt.entries:
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
                else:
                    b = BlockStmt()
                    switch2 = s.stmts[0].stmts[0] if len(s.stmts) > 0 else None
                    body2 = self.build_switch(cases[1:], body, adt_mtds, depth+1, switch2)
                    body = [body2] if not isinstance(body2, list) else body2
                    b.stmts = body
                    s.stmts = [b]
                    b.add_parent_post(s, True)
                    map(lambda s: s.add_parent_post(b), body)                         
        
        return new_block
        
    # cases should be a list of NameExprs representing the tree of cases
    # body is the body to fill in for that case
    def add_body(self, cases, body, adt_mtds):
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
                else:
                    b = BlockStmt()
                    switch = s.stmts[0].stmts[0] if len(s.stmts) > 0 else None
                    body2 = self.build_switch(cases[1:], body, adt_mtds, 1, switch)
                    body = [body2] if not isinstance(body2, list) else body2
                    b.stmts = body
                    s.stmts = [b]
                    b.add_parent_post(s, True)
                    map(lambda s: s.add_parent_post(b), body)                       
                    
    def __str__(self): return self._name
