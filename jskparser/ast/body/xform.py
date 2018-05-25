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
from ..body.methoddeclaration import MethodDeclaration

from ..type.referencetype import ReferenceType

from ..utils import utils

from axiomparameter import AxiomParameter

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
        self.prev_arg = []

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
    def gen_xform(cls, name, adt_mtds, params, is_ax_cls, ax):
        from .methoddeclaration import MethodDeclaration
        # create a switch dictionary
        entries = []
        for a in adt_mtds:
            entries.append({u'@t':u'SwitchEntryStmt',
                            u'label':{u'@t':u'NameExpr',u'name':a.name_no_nested(False).capitalize(),},
                            u'adt_mtds':adt_mtds},)
        dec = {u'@t': u'VariableDeclarator',
               u'id': {u'@t':u'VariableDeclaratorId', u'name': u'self',},
               u'type': {u'@t': u'ClassOrInterfaceType', u'name': str(cls),},
               u'init': {u'@t':u'LiteralExpr', u'name':u'selff._'+str(cls).lower(),},}

        if not is_ax_cls:
            dec = {u'@t': u'VariableDeclarator',
                   u'id': {u'@t':u'VariableDeclaratorId', u'name': u'self',},
                   u'type': {u'@t': u'ClassOrInterfaceType', u'name': str(cls),},
                   u'init': {u'@t':u'LiteralExpr', u'name':u'selff',},}
            
        
        dec_self = {u'@t': u'VariableDeclarationExpr',
                    u'name': u'self',
                    u'vars': {u'@e': [dec],},
                    u'type': {u'@t': u'ClassOrInterfaceType', u'name': str(cls),},}

        dec_self_stmt = {u'@t':u'ExpressionStmt',
                         u'expr':dec_self,}        
        
        switch = {u'@t':u'SwitchStmt', u'selector':{u'@t':u'NameExpr',u'name':u'self'},
                  u'entries':{u'@e':entries,},}
        xform = {u'@t':u'Xform',u'stmt':switch,u'name':name,
                 u'type':{u'@t':u'ClassOrInterfaceType',u'name':str(cls),},}
        ret_none = {u'@t':u'ReturnStmt', u'expr': {u'@t':u'LiteralExpr', u'name':u'null',},}
        ax_typ = str(ax.typee)
        is_arr = False
        if isinstance(ax.typee, ReferenceType) and ax.typee.arrayCount > 0:
            is_arr = True
        if not is_ax_cls:
            if str(ax.typee) != u'void':
                prim_bot = {
                    u'boolean': u'0',
                    u'int': u'0',
                    u'double': u'0',
                    u'float': u'0',
                    u'Object': u'null'
                    }
                typ = prim_bot[str(ax.typee)] if str(ax.typee) in prim_bot else u'null'
                ret_none = {u'@t':u'ReturnStmt', u'expr': {u'@t':u'LiteralExpr', u'name':typ,},}
            else:
                ret_none = {u'@t':u'ReturnStmt',}
            if is_arr:
                return MethodDeclaration({u'type':{u'@t':u'ReferenceType', u'arrayCount': 1, u'type':{u'@t':u'ClassOrInterfaceType',u'name':str(ax_typ),}},
                                          u'name':name,u'adtType':True, u'modifiers':Modifiers[u'AT'],
                                          u'body':{u'@t':u'BlockStmt',
                                                   u'stmts':{u'@e':[dec_self_stmt, xform, ret_none],},},
                                          u'parameters':{u'@e':params},},)
            else:
                return MethodDeclaration({u'type':{u'@t':u'ClassOrInterfaceType',u'name':str(ax_typ),},
                                          u'name':name,u'adtType':True, u'modifiers':Modifiers[u'AT'],
                                          u'body':{u'@t':u'BlockStmt',
                                                   u'stmts':{u'@e':[dec_self_stmt, xform, ret_none],},},
                                          u'parameters':{u'@e':params},},)
        else:
            return MethodDeclaration({u'type':{u'@t':u'ClassOrInterfaceType',u'name':u'Object',},
                                      u'name':name,u'adtType':True, u'modifiers':Modifiers[u'AT'],
                                      u'body':{u'@t':u'BlockStmt',
                                               u'stmts':{u'@e':[dec_self_stmt, xform, ret_none],},},
                                      u'parameters':{u'@e':params},},)
    
    def gen_switch(self, adt_mtds, depth, arg, cls, mtd, args, is_ax_cls, mtd_name, arg_num):
        entries = []
        for a in adt_mtds:
            entries.append({u'@t':u'SwitchEntryStmt',
                            u'label':{u'@t':u'NameExpr',
                                      u'name':a.name_no_nested(False).capitalize(),},
                            u'adt_mtds':adt_mtds,},)

        mtds = utils.extract_nodes([MethodDeclaration], cls, recurse=False)
        mtd_name = str(mtd_name).split('_')[0]
        # print("HERE: "+str(mtd_name).lower())
        # for a in adt_mtds:
        #     print("\t: "+str(a.name).lower())
        current_mtds = filter(lambda m: m.adt and str(m.name).lower() == str(mtd_name).lower(), mtds)

        # name = u'selff'
        name = str(arg.name)
        if current_mtds != []:
            # name = current_mtds[0].parameters[arg_num-1].name
            name = current_mtds[0].parameters[arg_num-1].name            
            
        slf = name+((u'_'+name)*depth)
        
        # if (name != "self" and depth == 1):
        #     slf_dot = name+u'._'+str(self.typee).lower()
        # else:
        #     slf_dot = ((name+u'_')*(depth-1))+name+u'.self'
        # if (name != "self" and depth == 1):
        #     slf_dot = name+u'._'+str(self.typee).lower()
        # else:
        #     slf_dot = ((name+u'_')*(depth-1))+name+u'.self'
        if (name != "self" and depth == 1):
            if self.prev_arg != []:
                slf_dot = self.prev_arg[-1]+u'._'+str(self.typee).lower()
            else:
                slf_dot = name+u'._'+str(self.typee).lower()
        else:
            if self.prev_arg != []:
                slf_dot = ((self.prev_arg[-1]+u'_')*(depth-1))+self.prev_arg[-1]
                if not (name in self.prev_arg):
                    slf_dot += u'.'+name+u'._'+str(self.typee).lower()
                else:
                    slf_dot += u'.self'
            else:
                slf_dot = ((name+u'_')*(depth-1))+name+u'.self'
                
        # if (str(arg.name) != "self" and depth == 1):
        #     slf_dot = self.prev_arg+u'._'+str(self.typee).lower()
        # else:
        #     slf_dot = ((self.prev_arg+u'_')*(depth-1))+self.prev_arg+u'.self'

        self.prev_arg.append(name)
            
            
        check_null = {u'@t':u'BinaryExpr',
                      u'left': {u'@t':u'LiteralExpr', u'name':slf_dot,},
                      u'right': {u'@t':u'NullLiteralExpr',},
                      u'op': {u'name': u'equals',},}

        adt_mtd = filter(lambda m: m.adt and m.name == a.name, mtds)[0]        
        
        ret_val = u'new '+str(mtd.name).lower().capitalize()+u'(self=selff._'+str(cls).lower()
        for ap,mp in zip(adt_mtd.parameters, args[1:]):
            ret_val += u', '+str(ap.name)+u'='+str(mp.name)
        ret_val += u')'

        assn_self = {u'@t':u'AssignExpr',
                     u'target':{u'@t':u'LiteralExpr', u'name':u'selff._'+str(cls).lower(),},
                     u'value':{u'@t':u'LiteralExpr', u'name':ret_val,},
                     u'op':{u'name':u'ASSIGN',},}

        assn_self_stmt = {u'@t':u'ExpressionStmt',
                          u'expr':assn_self,}
        
        ret_self = {u'@t': u'ReturnStmt',
                    u'expr': {u'@t':u'LiteralExpr', u'name':u'selff',},}

        ret_block = {u'@t':u'BlockStmt',
                     u'stmts':{u'@e':[assn_self_stmt, ret_self],},}

        if is_ax_cls:
            ret_block = {u'@t': u'ReturnStmt',
                         u'expr': {u'@t':u'LiteralExpr', u'name':
                                   u'new Object(__cid='+str(cls)+u'(), _'+str(cls).lower()+u'='+ret_val+u')',},}
        
        
        if_stmt = {u'@t':u'IfStmt',
                   u'condition': check_null,
                   u'thenStmt': ret_block,}

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
                           u'stmts':{u'@e':[if_stmt, vdec_expr, assn_expr, xform],},},)
            
        return block

    def build_switch(self, cases, body, adt_mtds, depth, arg_num, args, switch, cls, mtd, is_ax_cls, mtd_name, current_index):
        new_switch = None

        if len(cases) > 0:
            if cases[0][1] != arg_num:
                arg_num = cases[0][1]
                depth = 1

        if not switch:
            new_block = self.gen_switch(adt_mtds, depth, args[arg_num], cls, mtd, args, is_ax_cls, mtd_name, arg_num)
            new_switch = new_block.stmts[3]
        else:
            new_switch = switch

        current_index = 0;
        for s in new_switch.stmt.entries:
            if str(s.label) == cases[0][0]:
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
                    body2 = self.build_switch(cases[1:], body, adt_mtds, depth+1, arg_num, args, switch2, cls, mtd, is_ax_cls, s.label, current_index+1)
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

    def add_body_nested(self, casess, body, adt_mtds, args, cls, a, is_ax_cls):
        # cases = []
        # for i in range(0, len(casess)):
        #     for c in casess[i]:
        #         cases.append((c,i))

        cases = [item for sublist in casess for item in sublist]        

        # i dont think i know what this means yet...but it's probably not good
        if len(cases) == 0:
            raise Exception('Length of cases == 0')

        for s in self.stmt.entries:
            s_label = str(s.label)
            if s_label == cases[0][0] or (len(s_label)> 6 and s_label[len(s_label)-6:] == '_empty' and s_label[0:len(s_label)-6].capitalize() == cases[0][0]):  
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
                    body2 = self.build_switch(cases[1:], body, adt_mtds, 1, 0, args, switch, cls, a, is_ax_cls, s.label, 0)
                    body = [body2] if not isinstance(body2, list) else body2
                    b.stmts = body
                    s.stmts = [b]
                    b.add_parent_post(s, True)
                    map(lambda s: s.add_parent_post(b), body)                       

    # def areNamesEqual(self, 
                    
    def __str__(self): return self._name
