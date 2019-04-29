#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
try: unicode
except: unicode = u"".__class__
try: xrange
except: xrange = range

from functools import reduce
import sys
try:
    import cStringIO
except: # so sue me.
    import io as cStringIO
import logging
import copy
import os
import copy as cp

from . import util
from . import convert
from . import builtins

from . import visit as v

from ast import Operators as op
from ast import AssignOperators as assignop

from ast.utils import utils
from ast.node import Node
from ast.importdeclaration import ImportDeclaration
from ast.typeparameter import TypeParameter
from ast.compilationunit import CompilationUnit

from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.constructordeclaration import ConstructorDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.parameter import Parameter
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.variabledeclarator import VariableDeclarator
from ast.body.variabledeclaratorid import VariableDeclaratorId
from ast.body.axiomparameter import AxiomParameter
from ast.body.xform import Xform

from ast.stmt.blockstmt import BlockStmt
from ast.stmt.returnstmt import ReturnStmt
from ast.stmt.ifstmt import IfStmt
from ast.stmt.foreachstmt import ForeachStmt
from ast.stmt.forstmt import ForStmt
from ast.stmt.whilestmt import WhileStmt
from ast.stmt.continuestmt import ContinueStmt
from ast.stmt.minrepeatstmt import MinrepeatStmt
from ast.stmt.emptystmt import EmptyStmt
from ast.stmt.expressionstmt import ExpressionStmt
from ast.stmt.assertstmt import AssertStmt
from ast.stmt.assumestmt import AssumeStmt
from ast.stmt.switchstmt import SwitchStmt
from ast.stmt.breakstmt import BreakStmt
from ast.stmt.switchentrystmt import SwitchEntryStmt
from ast.stmt.throwstmt import ThrowStmt
from ast.stmt.explicitconstructorinvocationstmt import ExplicitConstructorInvocationStmt

from ast.expr.variabledeclarationexpr import VariableDeclarationExpr
from ast.expr.unaryexpr import UnaryExpr
from ast.expr.binaryexpr import BinaryExpr
from ast.expr.nameexpr import NameExpr
from ast.expr.assignexpr import AssignExpr
from ast.expr.methodcallexpr import MethodCallExpr
from ast.expr.generatorexpr import GeneratorExpr
from ast.expr.objectcreationexpr import ObjectCreationExpr
from ast.expr.fieldaccessexpr import FieldAccessExpr
from ast.expr.arraycreationexpr import ArrayCreationExpr
from ast.expr.arrayinitializerexpr import ArrayInitializerExpr
from ast.expr.arrayaccessexpr import ArrayAccessExpr
from ast.expr.enclosedexpr import EnclosedExpr
from ast.expr.conditionalexpr import ConditionalExpr
from ast.expr.thisexpr import ThisExpr
from ast.expr.superexpr import SuperExpr
from ast.expr.castexpr import CastExpr
from ast.expr.literalexpr import LiteralExpr
from ast.expr.booleanliteralexpr import BooleanLiteralExpr
from ast.expr.integerliteralexpr import IntegerLiteralExpr
from ast.expr.doubleliteralexpr import DoubleLiteralExpr
from ast.expr.nullliteralexpr import NullLiteralExpr
from ast.expr.charliteralexpr import CharLiteralExpr
from ast.expr.stringliteralexpr import StringLiteralExpr
from ast.expr.instanceofexpr import InstanceOfExpr

from ast.type.primitivetype import PrimitiveType
from ast.type.voidtype import VoidType
from ast.type.referencetype import ReferenceType
from ast.type.classorinterfacetype import ClassOrInterfaceType

from . import CONVERSION_TYPES

from ast.utils import utils

class Translator(object):
    SELF = NameExpr({u'@t':u'NameExpr',u'name':u'self'})
    _cid = {u'@t': u'AssignExpr', u'op': {u'name': u'assign'},
            u'target': {u'name': u'__cid', u'@t': u'NameExpr'},
            u'value': {u'value': u'', u'@t': u'IntegerLiteralExpr'}}
    ARRAY_SIZE = 50
    def __init__(self, **kwargs):
        # convert the given type name into a newer one
        self._ty = {}     # { tname : new_tname }
        self._flds = {}   # { Cls.fld : str(fld) }
        self._cnums = kwargs.get('cnums')
        self._mnums = kwargs.get('mnums')
        self._sk_dir = kwargs.get('sk_dir')
        self._fs = kwargs.get('fs')
        self._is_ax_cls = kwargs.get('is_ax_cls')
        self._ax_clss = kwargs.get('ax_clss')            
        
        self._buf = None
        self._mtd = None
        self._cls = None

        # array bounds will be set to this if not specified
        self._num_mtds = 1

        # for pretty printing
        self._indentation = kwargs.get('indentation', '  ')
        self._level = kwargs.get('level', 0)
        self._indented = kwargs.get('indented', False)

        # struct Object { ... }
        self.obj_struct = None

        # already written uninterpreted functions
        self.unfuns = []

        # anything that needs to get written post-translation (e.g., anonymous class mtds)
        self._post_mtds = ''
        self.anon_ids = -1

        self.primitiveIds = { u'int':-2,
                              u'char':-3,
                              u'bit':-4,
                              u'float':-5,
                              u'double':-6 }

    @v.on('node')
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """

    @v.when(Node)
    def visit(self, n, **kwargs):
        logging.error('unimplemented node: {}'.format(n))
        # if isinstance(n, Type): print 'un:', n
        # map(lambda x: x.accept(self, **kwargs), n.childrenNodes)

    # body
    @v.when(ConstructorDeclaration)
    def visit(self, n, **kwargs):
        n = copy.copy(n)
        cls = n if isinstance(n, ClassOrInterfaceDeclaration) else n.get_coid()
        etypes = cls.enclosing_types()
        self.printt('Object {0}_{0}'.format(str(cls)))
        ptypes = n.param_typs()
        if cls.isinner(): self.printt('_{}'.format(str(cls.get_coid())))
        if ptypes: self.printt('_{}'.format('_'.join(map(str, ptypes))))
        self.printTypeParameters(n.typeParameters)

        p = [Parameter({u'id':{u'name':u'self'},
                       u'type':{u'@t':u'ClassOrInterfaceType',u'name':u'Object'}})]
        if cls.isinner():
            p.append(Parameter({u'id':{u'name':u'self_{}'.format(len(etypes)-1)},
                                u'type':{u'@t':u'ClassOrInterfaceType',u'name':u'Object'}}))
        n.parameters = p + n.parameters

        self.printt('(')
        # self.printSepList(n.parameters)
        for i in range(0, len(n.parameters)):
            param = n.parameters[i]
            if isinstance(param.typee, ReferenceType) and isinstance(param.typee.typee, ClassOrInterfaceType) and str(param.typee.typee) in [c.name for c in self._ax_clss] and not self._is_ax_cls:
                self.printt('Object')
            else:
                param.typee.accept(self, **kwargs)
            self.buf.write(' {}'.format(str(param.idd)))
            if i != len(n.parameters)-1: self.printt(', ')
            
        self.printt(') ')

        for i in xrange(n.arrayCount): self.printt('[]')
        if n.throws:
            self.printt(' throws ')
            self.printCommaList(n.throws)

        if not n.body: self.printt(';')
        else:
            if cls.isinner():
                n.body.stmts = ['self{0} = self_{0};'.format(len(etypes)-1)] + n.body.stmts
            n.body.stmts = n.body.stmts + [u'return self;']
            n.body.accept(self, **kwargs)
        self.printLn()

    @v.when(MethodDeclaration)
    def visit(self, n, **kwargs):
        if n.get_coid().interface: return
        self.printMods(n)
        if td.isHarness(n):
            self.printt('harness ')
            s = [u'Object self = Object_Object(new Object(__cid=Object()));']
            if self._fs:
                s.append(u'fs_s@Object(HashMap_NoHash_HashMap_NoHash(new Object(__cid=HashMap_NoHash())));')
            n.body.stmts = s + n.body.stmts

        boxedRet = u'boxedRet' in [str(a) for a in n.annotations] or n.boxedRet
            
        if (isinstance(n.typee, ReferenceType) and isinstance(n.typee.typee, ClassOrInterfaceType) and str(n.typee.typee) in [c.name for c in self._ax_clss] and not self._is_ax_cls) or boxedRet:
            self.printt('Object')
        else:
            n.typee.accept(self, **kwargs)
        self.printt(' ')
        self.printt(str(n))
        # self.printTypeParameters(n.typeParameters)
        
        self.printt('(')
        
        if not td.isStatic(n) and not td.isHarness(n) and not td.isADT(n):
            ty = n.get_coid().name if n.adtType else self.trans_ty(n.get_coid())
            self.printt('{} self'.format(ty))
            if n.parameters: self.printt(', ')

        if not td.isHarness(n) or not self._is_ax_cls:
            params = cp.copy(n.parameters)
            # if str(n).startswith('xform_'):
            #     _self = Parameter({u'id':{u'name':u'selff'},
            #                        u'type':{u'@t': u'ReferenceType', u'type': {u'@t':u'ClassOrInterfaceType', u'name':u'Object'},},},)
            #     params[0] = _self                

            # print("HERE: "+str(n))
            # for i in range(0, len(params)):
            #     p = params[i]
            #     if isinstance(p.typee, ReferenceType) and isinstance(p.typee.typee, ClassOrInterfaceType) and str(p.typee.typee) in [c.name for c in self._ax_clss] and not self._is_ax_cls:
            #         params[i] = Parameter({u'id':{u'name':p.name},
            #                                u'type':{u'@t': u'ReferenceType', u'type': {u'@t':u'ClassOrInterfaceType', u'name':u'Object'},},},)
            
            for i in range(0, len(params)):
                param = params[i]
                if ((isinstance(param.typee, ReferenceType) and isinstance(param.typee.typee, ClassOrInterfaceType) and str(param.typee.typee) in [c.name for c in self._ax_clss] and not self._is_ax_cls and not str(n).startswith('xform_')) or (i+1) in n.boxedArgs) or (i == 0 and n.boxedRet):
                    self.printt('Object')
                else:
                    param.typee.accept(self, **kwargs)
                self.buf.write(' {}'.format(str(param.idd)))
                if i != len(params)-1: self.printt(', ')

            # self.printSepList(params)            

            # if not td.isADT(n): self.printSepList(n.parameters)
            # elif n.parameters:
            #     self.printt(n.parameters[0].typee.name)
            #     self.printt(' ')
            #     self.printt(n.parameters[0].name)
            #     if len(n.parameters) > 1: self.printt(', ')
            #     self.printSepList(n.parameters[1:])
        else:
            self.printSepListHarness(n.parameters, **kwargs)
        self.printt(')')

        for i in xrange(n.arrayCount): self.printt('[]')

        if not n.body: self.printt(';')
        else:
            if self._is_ax_cls:
                self.printt(' ')            
                if td.isHarness(n):
                    for p in n.parameters:
                        if isinstance(p.typee, PrimitiveType):
                            if 'HasCurly' not in kwargs or not kwargs['HasCurly']:
                                self.printt('{\n');                            
                            typ = self.trans_ty(p.typee)
                            cid = self.primitiveIds[typ]
                            self.printt('  Object {0} = new Object(__cid={1}, _{2}={3}); \n'.format(p.name, cid, typ, '__'+p.name))
                            kwargs['HasCurly'] = True
                n.body.accept(self, **kwargs)
                kwargs['HasCurly'] = False
            else:
                self.printt(' ')
                kwargs[u'boxedRet'] = boxedRet
                n.body.accept(self, **kwargs)
                kwargs[u'boxedRet'] = False                
        self.printLn()

    @v.when(Xform)
    def visit(self, n, **kwargs):
        if n.normal_body:
            n.body.accept(self, **kwargs)
            return
        # going to have to parse switch statements differently here
        parent = n.parentNode
        while not isinstance(parent, ClassOrInterfaceDeclaration):
            parent = parent.parentNode
        xf = n.parentNode
        while not isinstance(xf, MethodDeclaration):
            xf = xf.parentNode

        if n.stmt:
            self.printt('switch(')
            n.stmt.selector.accept(self, **kwargs)
            self.printLn(') {')
            for e in n.stmt.entries:
                self.printt('case ')
                e.label.accept(self, **kwargs)
                self.printt(': ')
                if not e.stmts:
                    names = (str(n)[6:].split('_'))                    
                    names.insert(1, u'Object')
                    name = names[0]
                    for nam in names[1:]:
                        name += u'_'+nam
                    adt_mtd = [m for m in e.adt_mtds if str(m) == name or (str(m) == name.replace('_Object', '', 1))][0]
                    ret_val = str(n)[6:].lower().capitalize()+u'('
                    if not len(adt_mtd.parameters) == 0 and adt_mtd.parameters[0].name == u'self':
                        ret_val += u'self=selff._'+str(parent).lower()          
                    for ap,mp in zip(adt_mtd.parameters, xf.parameters[1:]):
                        if ret_val[-1] != '(':
                            ret_val += u', '
                        ret_val += str(ap.name)+u'='+str(mp.name)

                    ret_val += u')'
                    if self._is_ax_cls or xf.boxedRet:
                        ret_val = u'Object(__cid={0}(), _{1}=new {2})'.format(parent, parent.name.lower(), ret_val)
                        self.printt(u'return new '+ret_val+u';')
                        # self.printt('{ assert false; }')
                    else:
                        self.printt('{ assert false; }')
                    self.printLn()
                for s in e.stmts:
                    s.accept(self, **kwargs)
                    self.printLn()
                    
        if not n.stmt: self.printLn()
        self.printLn('}')

    @v.when(Parameter)
    def visit(self, n, **kwargs):
        n.typee.accept(self, **kwargs)
        self.buf.write(' {}'.format(str(n.idd)))
        
    @v.when(AxiomParameter)
    def visit(self, n, **kwargs):
        self.printt(str(n.typee))
        self.buf.write(' {}'.format(str(n.idd)))
        
    @v.when(VariableDeclarator)
    def visit(self, n, **kwargs):
        if self._is_ax_cls: kwargs['ArrayName'] = n.idd
        if n.init and self._is_ax_cls:
            self.printt(' ')
            n.idd.accept(self, **kwargs)
            self.printt(' = ')
            if isinstance(n.init, UnaryExpr):
                typ = self.getUnboxPrimitiveType(n.init.expr)
                cid = self.primitiveIds[typ]
                self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))
                n.init.accept(self, **kwargs)
                self.printt('))')
            elif isinstance(n.init, BinaryExpr):
                typ = self.getUnboxPrimitiveType(n.init.left)
                cid = self.primitiveIds[typ]
                self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))      
                n.init.accept(self, **kwargs)
                self.printt('))')
            elif isinstance(n.init, ArrayAccessExpr):
                if isinstance(n.typee, PrimitiveType):
                    typ = self.trans_ty(n.typee)
                    cid = self.primitiveIds[typ]
                    self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))   
                    n.init.accept(self, **kwargs)
                    self.printt('))')
                else:
                    n.init.accept(self, **kwargs)
            elif isinstance(n.init, GeneratorExpr):
                n.init.my_typ = n.typee
                n.init.accept(self, **kwargs)                
            else:
                if isinstance(n.init, ArrayInitializerExpr):
                    typ = self.trans_ty(n.typee)
                    kwargs['ArrayType'] = typ
                    self.printt('Wrap_Array_{}('.format(typ))
                    self.printt('new ')                
                    # n.typee.accept(self, **kwargs)
                    self.printt('Array_{}'.format(typ))
                    self.printt('(')
                n.init.accept(self, **kwargs)
        elif n.init and (u'box' in kwargs and kwargs[u'box']):
            self.printt(' ')
            n.idd.accept(self, **kwargs)
            self.printt(' = ')
            if isinstance(n.typee, PrimitiveType):
                typ = self.trans_ty(n.typee)
                cid = self.primitiveIds[typ]
                self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))   
                n.init.accept(self, **kwargs)
                self.printt('))')
            elif isinstance(n.typee, ReferenceType) and n.typee.arrayCount > 0:
                typ = self.trans_ty(n.typee)
                cid = self.primitiveIds[typ]
                self.printt('(new Object(__cid={0}, _array_{1}='.format(cid, typ))   
                n.init.accept(self, **kwargs)
                self.printt('))')                
            else:
                n.init.accept(self, **kwargs)            
        elif n.init and not self._is_ax_cls:
            self.printt(' ')
            n.idd.accept(self, **kwargs)
            self.printt(' = ')
            if isinstance(n.init, ArrayInitializerExpr):
                self.printt('new ')
                n.typee.accept(self, **kwargs)
                self.printt('(')
            n.init.accept(self, **kwargs)
        else:
            self.printt(' ')
            n.idd.accept(self, **kwargs)

    @v.when(VariableDeclaratorId)
    def visit(self, n, **kwargs):
        self.printt(str(n))        

    # stmt
    @v.when(BlockStmt)
    def visit(self, n, **kwargs):
        if 'HasCurly' not in kwargs or not kwargs['HasCurly'] or not self._is_ax_cls:
            self.printLn('{')
        else:
            kwargs['HasCurly'] = False            
        if n.stmts:
            self.indent()
            for s in n.stmts:
                if type(s) == str or type(s) == unicode:
                    self.printLn(s)
                else:
                    s.accept(self, **kwargs)
                    self.printLn()
            self.unindent()
        self.printt('}')

    @v.when(ReturnStmt)
    def visit(self, n, **kwargs):
        if self._is_ax_cls: kwargs['Return'] = True
        self.printt('return')
        if (n.expr and self._is_ax_cls):
            self.printt(' ')
            typ = ''
            if isinstance(n.expr, BinaryExpr) or isinstance(n.expr, UnaryExpr):
                if isinstance(n.expr.typee, PrimitiveType):
                    typ = self.trans_ty(n.expr.typee)
            elif isinstance(n.expr, ArrayAccessExpr):
                typ = self.trans_ty(n.expr.nameExpr.typee)
                if n.expr.nameExpr.name in n.expr.nameExpr.symtab:
                    typ = self.trans_ty(n.expr.nameExpr.symtab[n.expr.nameExpr.name].typee)
                else:
                    typ = self.trans_ty(utils.find_fld(n.expr.nameExpr, self.obj_struct).typee)
                if typ == 'Object': typ = ''
                if typ == 'byte': typ = 'char'                

            if typ != '':
                cid = self.primitiveIds[typ]
                self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))       
                n.expr.accept(self, **kwargs)
                self.printt('))')
            else:
                n.expr.accept(self, **kwargs)
        elif n.expr and kwargs[u'boxedRet']:
            typ = self.trans_ty(n.expr.typee)
            if typ == 'byte': typ = 'char'
            if typ == u'Object':
                self.printt(' ')
                n.expr.accept(self, **kwargs)
            else:
                cid = self.primitiveIds[typ]
                self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))       
                n.expr.accept(self, **kwargs)
                self.printt('))')            
        elif n.expr and not self._is_ax_cls:
            self.printt(' ')
            n.expr.accept(self, **kwargs)            
        if self._is_ax_cls: kwargs['Return'] = True        
        self.printt(';')

    @v.when(IfStmt)
    def visit(self, n, **kwargs):
        self.printt('if (')
        if isinstance(n.condition, GeneratorExpr) and self._is_ax_cls:
            n.condition.my_typ = PrimitiveType({u'type': {u'name': u'bit'}})
        n.condition.accept(self, **kwargs)
        if self._is_ax_cls:
            if isinstance(n.condition, NameExpr) or isinstance(n.condition, FieldAccessExpr):
                if isinstance(n.condition.typee, PrimitiveType):
                    self.printt('._'+self.trans_ty(n.condition.typee))     
            elif isinstance(n.condition, MethodCallExpr):
                self.printt('._bit')
            elif isinstance(n.condition, GeneratorExpr):
                self.printt('._bit')
        
            
        thenBlock = isinstance(n.thenStmt, BlockStmt)
        self.printt(') ')
        if not thenBlock: self.indent()
        n.thenStmt.accept(self, **kwargs)
        if not thenBlock: self.unindent()
        if n.elseStmt:
            self.printLn()
            elseIf = isinstance(n.elseStmt, IfStmt)
            elseBlock = isinstance(n.elseStmt, BlockStmt)
            if elseIf or elseBlock: self.printt('else ')
            else:
                self.printLn('else')
                self.indent()
            n.elseStmt.accept(self, **kwargs)
            if not (elseIf or elseBlock): self.unindent()

    # TODO: this needs work
    @v.when(ForeachStmt)
    def visit(self, n, **kwargs):
        tltr = copy.copy(self)
        tltr.indentation = ''
        it = tltr.trans(n.iterable)
        self.printt('for (int _i = 0; _i < ')
        self.printt('{}.length; ++_i)'.format(it))
        inits = []
        for vv in n.var.varss:
            inits.append('{} {} = {}.A[_i];'.format(self.trans_ty(n.iterable.typee), vv.name, it))
        s = [n.body] if isinstance(n.body, ExpressionStmt) else n.body.stmts
        n.body.stmts = ['\n'.join(inits)] + s
        n.body.accept(self, **kwargs)

    @v.when(ForStmt)
    def visit(self, n, **kwargs):
        self.printt('for (')
        if n.init: self.printSepList(n.init)
        self.printt('; ')
        if n.compare: n.compare.accept(self, **kwargs)
        self.printt('; ')
        if n.update: self.printSepList(n.update)
        self.printt(') ')
        n.body.accept(self, **kwargs)

    @v.when(WhileStmt)
    def visit(self, n, **kwargs):
        self.printt('while (')
        if n.condition:
            n.condition.accept(self, **kwargs)
            if self._is_ax_cls: self.unboxPrimitive(n.condition)
        self.printt(') ')
        n.body.accept(self, **kwargs)

    @v.when(MinrepeatStmt)
    def visit(self, n, **kwargs):
        self.printt('minrepeat ')
        n.body.accept(self, **kwargs)

    @v.when(ExpressionStmt)
    def visit(self, n, **kwargs):
        if n.expr: n.expr.accept(self, **kwargs)
        self.printt(';')

    @v.when(AssertStmt)
    def visit(self, n, **kwargs):
        self.printt('assert ')
        n.check.accept(self, **kwargs)
        if not isinstance(n.check, BinaryExpr) and not isinstance(n.check, UnaryExpr) and self._is_ax_cls:
            self.printt('._bit')
        # There are no messages in Sketch, I think
        # if n.msg:
        #     self.printt(' : ')
        #     n.msg.accept(self, **kwargs)
        self.printt(';')

    @v.when(AssumeStmt)
    def visit(self, n, **kwargs):
        self.printt('assume ')
        n.expr.accept(self, **kwargs)
        self.printt(';')

    @v.when(SwitchStmt)
    def visit(self, n, **kwargs):
        def print_stmts(stmts):
            self.indent()
            for s in stmts:
                s.accept(self, **kwargs)
                self.printLn()
            self.unindent()
            self.printLn('}')

        self.printt('if (')
        n.selector.accept(self, **kwargs)
        if self._is_ax_cls: self.unboxPrimitive(n.selector)
        # take care of the first case
        if n.entries:
            self.printt(' == ')
            n.entries[0].label.accept(self, **kwargs)
            if self._is_ax_cls: self.unboxPrimitive(n.entries[0].label)
            self.printLn(') {')
            if n.entries[0].stmts: print_stmts(n.entries[0].stmts)
            if len(n.entries) > 0: self.printt('else if (')
        
        for e in range(1,len(n.entries)):
            if n.entries[e].label:
                if e > 1 and n.entries[e-1].stmts: self.printt('else if (')
                if n.entries[e].stmts:
                    n.selector.accept(self, **kwargs)
                    if self._is_ax_cls: self.unboxPrimitive(n.selector)
                    self.printt(' == ')
                    n.entries[e].label.accept(self, **kwargs)
                    if self._is_ax_cls: self.unboxPrimitive(n.entries[e].label)
                    self.printLn(') {')
                    print_stmts(n.entries[e].stmts)
                else:
                    n.selector.accept(self, **kwargs)
                    if self._is_ax_cls: self.unboxPrimitive(n.selector)
                    self.printt(' == ')
                    n.entries[e].label.accept(self, **kwargs)
                    if self._is_ax_cls: self.unboxPrimitive(n.entries[e].label)
                    self.printt(' || ')
            else:
                self.printLn('else {')
                print_stmts(n.entries[e].stmts)

    @v.when(SwitchEntryStmt)
    def visit(self, n, **kwargs):
        pass

    @v.when(ExplicitConstructorInvocationStmt)
    def visit(self, n, **kwargs):
        if n.isThis:
            self.printt('_'.join([str(n.get_coid()), str(n.get_coid())] + [str(t) for t in n.arg_typs()]))
        else:
            if n.expr:
                n.expr.accept(self, **kwargs)
                self.printt('.')
            cls = n.get_coid()
            sups = cls.supers()
            if not sups: exit('Calling super with  with no super class: {}'.format(str(cls)))
            def ty(a):
                return a.typee.name if type(a) != NameExpr else n.symtab[a.name].typee.name
            self.printt('_'.join([str(sups[0]), str(sups[0])] + [ty(a) for a in n.args]))
            self.printt('@{}'.format(str(sups[0])))
        self.printt(u'(self')
        if n.args: self.printt(', ')
        self.printSepList(n.args)
        self.printt(')')
        self.printt(';')

    @v.when(ContinueStmt)
    def visit(self, n, **kwargs):
        self.printt('continue')
        if n.idd:
            self.printt(' {}'.format(n.idd))
        self.printt(';')

    @v.when(BreakStmt)
    def visit(self, n, **kwargs):
        self.printt('break')
        if n.idd:
            self.printt(' {}'.format(n.idd))
        self.printt(';')

    @v.when(ThrowStmt)
    def visit(self, n, **kwargs):
        pass
        
    @v.when(EmptyStmt)
    def visit(self, n, **kwargs):
        pass

    # expr
    @v.when(NameExpr)
    def visit(self, n, **kwargs):
        if not n.symtab:
            self.printt(n.name)
            return
        # catch special axiom arg
        if n.axparam:
            # self.printt("self_"+n.axparam)
            self.printt(n.axparam)
            return
        obj = utils.node_to_obj(n)
        if type(obj) == FieldDeclaration:
            if td.isStatic(obj):
                self.printt(obj.name)
                return
            this = n.get_coid()
            obj_cls = obj.get_coid()
            if obj.name in this.symtab and this == obj_cls:
                i = ''
            else:
                etypes = this.enclosing_types()
                if etypes:
                    for (i,j) in zip(xrange(len(etypes)), reversed(etypes)):
                        if j == obj_cls: break
                else:
                    i = ''
                # this is the index of the class where the field lives
            slf = 'self{}'.format(i)
            self.printt('{}.{}'.format(slf, str(obj)))
        elif type(obj) == VariableDeclarator:
            self.printt(obj.name)
        else:
            self.printt(n.name)

    @v.when(VariableDeclarationExpr)
    def visit(self, n, **kwargs):
        if self._is_ax_cls: kwargs['VariableDeclarationExpr'] = True        
        typ = n.varss[0].typee if len(n.varss) > 0 else None
        cls = None
        if typ and isinstance(typ, ClassOrInterfaceType) or isinstance(typ, ReferenceType):
            cls = typ.symtab.get(typ.name)

        if (cls and isinstance(cls, ClassOrInterfaceDeclaration) and cls.axiom) or (n.annotations != [] and ((u'isBoxed' in [str(a) for a in n.annotations] or u'box' in [str(a) for a in n.annotations]))):
            self.printt('Object')
        else:
            n.typee.accept(self, **kwargs)
        # self.printt(' ')
        kwargs[u'box'] = u'box' in [str(a) for a in n.annotations]
        kwargs[u'unbox'] = (u'unbox' in [str(a) for a in n.annotations], n.typee)
        self.printSepList(n.varss, **kwargs)
        kwargs[u'box'] = False
        kwargs[u'unbox'] = False                       
        # if u'unbox' in map(lambda a: str(a), n.annotations):
        #     self.printt('._')
        #     n.typee.accept(self, **kwargs)

    @v.when(AssignExpr)
    def visit(self, n, **kwargs):
        def print_op():
            self.printt(' ')
            o = n.op.upper()
            not_ass = False
            if o == u'ASSIGN': self.printt(assignop[o])
            else:
                if self._is_ax_cls:
                    self.printt('=')
                    self.printt(' ')
                    typ = self.getUnboxPrimitiveType(n.target)
                    cid = self.primitiveIds[typ]
                    self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ)) 
                    n.target.accept(self, **kwargs)
                    self.unboxPrimitive(n.target)
                    self.printt(' ')
                    self.printt(assignop['_{}'.format(o)])
                    not_ass = True
                else:
                    self.printt('=')
                    self.printt(' ')
                    n.target.accept(self, **kwargs)
                    self.printt(' ')
                    self.printt(assignop['_{}'.format(o)])                    
            self.printt(' ')
            return not_ass
        if self._is_ax_cls:
            # print 'AssignExpr'
            already_unboxed = False
            if type(n.target) == FieldAccessExpr:
                v = self.trans_faccess(n.target)
                if v:
                    not_ass = print_op()
                    if not not_ass:
                        if isinstance(n.value, UnaryExpr):
                            typ = self.getUnboxPrimitiveType(n.value.expr)
                            cid = self.primitiveIds[typ]
                            self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ)) 
                            n.value.accept(self, **kwargs)
                            self.printt('))')
                        elif isinstance(n.value, BinaryExpr):
                            typ = self.getUnboxPrimitiveType(n.value.left)
                            cid = self.primitiveIds[typ]
                            self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ)) 
                            n.value.accept(self, **kwargs)
                            self.printt('))')
                        elif isinstance(n.value, CastExpr):
                            if isinstance(n.value.typee, PrimitiveType):
                                typ = self.trans_ty(n.value.typee)
                                cid = self.primitiveIds[typ]
                                self.printt('(new Object(__cid={0}, _{1}=('.format(cid, typ)) 
                                n.value.accept(self, **kwargs)
                                self.unboxPrimitive(n.value.expr)
                                self.printt(')))')                        
                        elif isinstance(n.value, ArrayAccessExpr) and not isinstance(n.target, ArrayAccessExpr):                        
                            if isinstance(n.target.typee, PrimitiveType) or isinstance(n.value.typee, PrimitiveType):
                                typ = self.getUnboxPrimitiveType(n.value)
                                cid = self.primitiveIds[typ]
                                self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ)) 
                                n.value.accept(self, **kwargs)
                                self.printt('))')
                            else:
                                n.value.accept(self, **kwargs)
                        else:                    
                            if isinstance(n.value, ArrayInitializerExpr) or isinstance(n.value, ArrayCreationExpr):
                                kwargs['ArrayName'] = self.trans_faccess_no_print(n.target)
                                kwargs['ArrayType'] = self.trans_ty(self.getUnboxPrimitiveType(n.value))
                            n.value.accept(self, **kwargs)
                            if isinstance(n.value, ArrayInitializerExpr) or isinstance(n.value, ArrayCreationExpr):
                                kwargs['ArrayType'] = None
                                kwargs['ArrayName'] = None
                    else:
                        if isinstance(n.value, ArrayInitializerExpr) or isinstance(n.value, ArrayCreationExpr):
                            kwargs['ArrayName'] = n.target.name                        
                            kwargs['ArrayType'] = self.trans_ty(self.getUnboxPrimitiveType(n.value))
                        n.value.accept(self, **kwargs)
                        self.unboxPrimitive(n.value)                    
                        self.printt('))')
                        already_unboxed = True
                        if isinstance(n.value, ArrayInitializerExpr) or isinstance(n.value, ArrayCreationExpr):
                            kwargs['ArrayType'] = None
                            kwargs['ArrayName'] = None                                                
            else:
                n.target.accept(self, **kwargs)
                not_ass = print_op()
                if not not_ass and not (isinstance(n.target, ArrayAccessExpr) and str(n.target.typee) in [u'bit', u'byte', u'int', u'float', u'double']):
                    if isinstance(n.value, UnaryExpr):
                        typ = self.getUnboxPrimitiveType(n.value.expr)
                        cid = self.primitiveIds[typ]
                        self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ)) 
                        n.value.accept(self, **kwargs)
                        self.printt('))')
                    elif isinstance(n.value, BinaryExpr):
                        typ = self.getUnboxPrimitiveType(n.value.left)
                        cid = self.primitiveIds[typ]
                        self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ)) 
                        n.value.accept(self, **kwargs)
                        self.printt('))')
                    elif isinstance(n.value, CastExpr):
                        if isinstance(n.value.typee, PrimitiveType):
                            typ = self.trans_ty(n.value.typee)
                            cid = self.primitiveIds[typ]
                            self.printt('(new Object(__cid={0}, _{1}=('.format(cid, typ)) 
                            n.value.accept(self, **kwargs)
                            self.unboxPrimitive(n.value.expr)
                            self.printt(')))')                        
                    elif isinstance(n.value, ArrayAccessExpr) and not isinstance(n.target, ArrayAccessExpr):
                        if isinstance(n.target.typee, PrimitiveType) or isinstance(n.value.typee, PrimitiveType):
                            typ = self.getUnboxPrimitiveType(n.value)
                            cid = self.primitiveIds[typ]
                            self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ)) 
                            n.value.accept(self, **kwargs)
                            self.printt('))')
                        else:
                            n.value.accept(self, **kwargs)
                    else:
                        if isinstance(n.value, ArrayInitializerExpr) or isinstance(n.value, ArrayCreationExpr):
                            kwargs['ArrayName'] = n.target.name                        
                            kwargs['ArrayType'] = self.trans_ty(self.getUnboxPrimitiveType(n.value))
                        n.value.accept(self, **kwargs)
                        if isinstance(n.value, ArrayInitializerExpr) or isinstance(n.value, ArrayCreationExpr):
                            kwargs['ArrayType'] = None
                            kwargs['ArrayName'] = None
                else:
                    if isinstance(n.value, ArrayInitializerExpr) or isinstance(n.value, ArrayCreationExpr):                
                        kwargs['ArrayName'] = n.target.name
                        kwargs['ArrayType'] = self.trans_ty(self.getUnboxPrimitiveType(n.value))
                    n.value.accept(self, **kwargs)
                    if isinstance(n.value, ArrayInitializerExpr) or isinstance(n.value, ArrayCreationExpr):                
                        kwargs['ArrayType'] = None
                        kwargs['ArrayName'] = None
                    if not isinstance(n.value, CastExpr):
                        self.unboxPrimitive(n.value)
                    if not_ass:# or (isinstance(n.target, ArrayAccessExpr) and str(n.target.typee) in [u'bit', u'byte', u'int', u'float', u'double']):                
                        self.printt('))')
                    already_unboxed = True                                        

            if isinstance(n.target, ArrayAccessExpr) and not isinstance(n.value, ArrayAccessExpr) and not isinstance(n.value, NullLiteralExpr) and not already_unboxed:
                if isinstance(n.value.typee, PrimitiveType) or isinstance(n.target.typee, PrimitiveType):
                    self.printt('._'+self.trans_ty(n.value.typee))

        else:
            # print 'AssignExpr'
            if type(n.target) == FieldAccessExpr:
                v = self.trans_faccess(n.target)
                if v:
                    print_op()
                    n.value.accept(self, **kwargs)
            else:
                n.target.accept(self, **kwargs)
                print_op()
                n.value.accept(self, **kwargs)
            
    @v.when(FieldAccessExpr)
    def visit(self, n, **kwargs):
        self.trans_faccess(n)

    def unboxPrimitive(self, n, **kwargs):
        typ = ''
        if isinstance(n, NameExpr):
            if isinstance(n.typee, PrimitiveType):
                self.printt('._'+self.trans_ty(n.typee))
                typ = self.trans_ty(n.typee)
        elif isinstance(n, GeneratorExpr):
            if isinstance(n.typee, PrimitiveType):
                self.printt('._'+self.trans_ty(n.typee))
                typ = self.trans_ty(n.typee)                
        # elif isinstance(n, CastExpr):
        #     # if isinstance(n.expr, EnclosedExpr):
        #     #     typ = self.unboxPrimitive(n.expr.inner)
        #     # elif 
        #     if isinstance(n.expr.typee, PrimitiveType):
        #         self.printt('._'+self.trans_ty(n.expr.typee))
        #         typ = self.trans_ty(n.expr.typee)                                
        elif isinstance(n, FieldAccessExpr):
            fld = utils.find_fld(n, self.obj_struct)            
            if isinstance(fld.typee, PrimitiveType):
                self.printt('._'+self.trans_ty(fld.typee))
                typ = self.trans_ty(fld.typee)
            # elif n.name == 'length' and n.typee == None:
            #     self.printt('._int')
            #     typ = u'int'
            # elif 'BinOp' in kwargs:
            #     if kwargs['BinOp'] in ['+', '-', '/', '*']:
            #         self.printt('._int')
            #         typ = u'int'                                
        elif isinstance(n, MethodCallExpr):
            if n.ax_typ != '':
                self.printt('._'+n.ax_typ)
                typ = n.ax_typ
            else:                
                # scp = n.scope if n.scope else n
                # if utils.node_to_obj(scp):
                #     print("\t\tHERE33: "+str(n.name))                    
                if isinstance(n.typee, PrimitiveType):
                    self.printt('._'+self.trans_ty(n.typee))
                    typ = self.trans_ty(n.typee)
        elif isinstance(n, EnclosedExpr):
            self.unboxPrimitive(n.inner)        
        elif isinstance(n, BooleanLiteralExpr):
            self.printt('._bit')
            typ = u'bit'
        elif isinstance(n, IntegerLiteralExpr):
            self.printt('._int')
            typ = u'int'
        elif isinstance(n, DoubleLiteralExpr):
            self.printt('._double')
            typ = u'double'
        elif isinstance(n, CharLiteralExpr):
            self.printt('._char')
            typ = u'char'

        return typ

    def getUnboxPrimitiveType(self, n, **kwargs):
        typ = ''
        if isinstance(n, NameExpr):
            if isinstance(n.typee, PrimitiveType):
                typ = self.trans_ty(n.typee)
        elif isinstance(n, FieldAccessExpr):
            if isinstance(n.typee, PrimitiveType):
                typ = self.trans_ty(n.typee)                
            elif n.name == 'length' and n.typee == None:
                typ = u'int'
        elif isinstance(n, EnclosedExpr):
            if isinstance(n.inner.typee, PrimitiveType):
                typ = self.trans_ty(n.inner.typee)
        elif isinstance(n, CastExpr):
            # if isinstance(n.expr.typee, PrimitiveType):
                # typ = self.trans_ty(n.expr.typee)                                
            if isinstance(n.typee, PrimitiveType):
                typ = self.trans_ty(n.typee)                                
        elif isinstance(n, MethodCallExpr):
            if n.ax_typ != '':
                typ = n.ax_typ
            else:
                if n.scope:
                    if utils.node_to_obj(n.scope):
                        if isinstance(n.typee, PrimitiveType):
                            typ = self.trans_ty(n.typee)
        elif isinstance(n, ArrayAccessExpr):            
            if str(n.typee) in [u'byte', u'bit', u'int', u'double', u'float']:
                typ = self.trans_ty(n.typee)
        elif isinstance(n, BinaryExpr):
            typ = self.getUnboxPrimitiveType(n.left)
        elif isinstance(n, BooleanLiteralExpr):
            typ = u'bit'
        elif isinstance(n, IntegerLiteralExpr):
            typ = u'int'
        elif isinstance(n, DoubleLiteralExpr):
            typ = u'double'
        elif isinstance(n, CharLiteralExpr):
            typ = u'char'

        return typ

    @v.when(UnaryExpr)
    def visit(self, n, **kwargs):
        if self._is_ax_cls:
            op_after = UnaryExpr.POST_OPS.get(n.op, '')
            op_before = UnaryExpr.PRE_OPS.get(n.op, '')

            if op_before not in ['++', '--']:
                self.printt(UnaryExpr.PRE_OPS.get(n.op, ''))

            if (op_after != '' or op_before in ['++', '--']) and not isinstance(n.expr, ArrayAccessExpr):
                n.expr.accept(self, **kwargs)
                self.printt(' = new Object(__cid=-2, _int=') 
                n.expr.accept(self, **kwargs)
                self.unboxPrimitive(n.expr)
                if op_after == '++':
                    self.printt(' + 1')
                else:
                    self.printt(' - 1')
                self.printt(')')
            else:
                n.expr.accept(self, **kwargs)
                self.unboxPrimitive(n.expr)
        else:
            self.printt(UnaryExpr.PRE_OPS.get(n.op, ''))
            n.expr.accept(self, **kwargs)
            self.printt(UnaryExpr.POST_OPS.get(n.op, ''))
            

    @v.when(BinaryExpr)
    def visit(self, n, **kwargs):
        n.left.accept(self, **kwargs)
        if self._is_ax_cls:
            kwargs['BinOp'] = op[n.op.upper()]
            self.unboxPrimitive(n.left, **kwargs)
        self.printt(' ')
        self.printt(op[n.op.upper()])
        self.printt(' ')
        n.right.accept(self, **kwargs)
        if self._is_ax_cls:
            self.unboxPrimitive(n.right, **kwargs)
            kwargs['BinOp'] = None                       

    @v.when(ObjectCreationExpr)
    def visit(self, n, **kwargs):
        obj_cls = n.symtab.get(n.typee.name)
        if not obj_cls:
            raise Exception('ObjectCreationExpr: Cannot find {} '.format(n.typee.name))
        cls = obj_cls.symtab.get(obj_cls.name)
        if isinstance(obj_cls, ImportDeclaration): obj_cls = obj_cls.cname()
        if isinstance(obj_cls, ReferenceType): obj_cls = self.trans_ty(obj_cls)
        if n.scope:
            n.getScope.accept(self, **kwargs)
            self.printt('.')
        if n.args:
            typs = []
            tparam_nms = [t.name for t in cls.typeParameters]
            cons = utils.extract_nodes([ConstructorDeclaration], cls)
            if cls.axiom:
                cons += [m for m in utils.extract_nodes([MethodDeclaration], cls) if m.constructor]
            for a in n.args:
                if type(a) == FieldAccessExpr:
                    tname = utils.find_fld(a, self.obj_struct).typee
                elif not a.typee:
                    t = n.symtab.get(a.name)
                    if t:
                        tname = t.typee
                    else:
                        raise Exception('ObjectCreationExpr:{} - cannot find {}'.
                                        format(a.beginLine, str(a)))
                else:
                    tname = a.typee
                typs.append(tname)
            nm = ''
            for c in cons:
                if nm == '':
                    if len(typs) == len(c.param_typs()) and \
                       self.match_loose(typs, c.param_typs(), tparam_nms):
                        nm = str(c)
                        # break
                else:
                    if len(typs) == len(c.param_typs()) and \
                       all([(str(a) == str(b)) for (a, b) in zip(typs, c.param_typs())]):
                        nm = str(c)
                        break            
            self.printt(nm)
        else:
            self.printt('{0}_{0}'.format(str(obj_cls)))
        if n.anonymousClassBody:
            # find name of variabledeclarator
            target = utils.anon_nm(n)
            target = n.symtab.get(target.name)
            nm = '{}_{}'.format(n.typee, target.name)
            anon_cls = ClassOrInterfaceDeclaration({u'@t':u'ClassOrInterfaceDeclaration',
                                               u'name':{u'name':nm,},})
            anon_cls.members = n.anonymousClassBody
            anon_cls.childrenNodes.extend(anon_cls.members)
            anon_cls.symtab = {}
            anon_cls.symtab.update({anon_cls.name:anon_cls})
            for m in n.anonymousClassBody:
                anon_cls.symtab.update({str(m):m})
            target.symtab.update({nm:anon_cls})

            tltr = copy.copy(self)
            tltr.indentation = ''
            anon = [tltr.trans(m) for m in anon_cls.members]

            anon.append('int {}() {{ return {}; }}\n'.format(anon_cls.name, self.anon_ids))
            self.anon_ids -= 1
            self.post_mtds += '\n'.join(anon)

            obj_cls = anon_cls
        self.printt('(')
        if not cls.axiom:
            self.printt('new Object(__cid={}())'.format(str(obj_cls)))
            if cls.isinner(): self.printt(', self')
            if n.args: self.printt(', ')
        if self._is_ax_cls:
            self.printSepListObjectCreationExpr(n.args)
        else:
            self.printSepList(n.args)
        self.printt(')')

    @v.when(ArrayCreationExpr)
    def visit(self, n, **kwargs):
        # print 'arraycreationexpr'
        if self._is_ax_cls:
            typ = self.trans_ty(n.typee)
            self.printt('Wrap_Array_{0}(new Array_{0}('.format(typ))
            if n.dimensions:
                for d in n.dimensions:
                    self.printt('length=')
                    if isinstance(d, BinaryExpr) and isinstance(d.typee, PrimitiveType):
                        self.printt('(new Object(__cid=-2, _int=')
                        d.accept(self, **kwargs)
                        self.printt('))')
                    else:
                        d.accept(self, **kwargs)
                self.printt('))')
                # for c in xrange(n.arrayCount):
                #     self.printt('[]')
            else:
                kwargs['ArrayType'] = typ
                n.initializer.accept(self, **kwargs)
                kwargs['ArrayType'] = None

            # self.printt(')')
        else:
            self.printt('new Array_{}('.format(self.trans_ty(n.typee)))
            if n.dimensions:
                for d in n.dimensions:
                    self.printt('length=')
                    d.accept(self, **kwargs)
                self.printt(')')
                # for c in xrange(n.arrayCount):
                #     self.printt('[]')
            else:
                n.initializer.accept(self, **kwargs)
            

    @v.when(ArrayInitializerExpr)
    def visit(self, n, **kwargs):
        # print 'arrayinitializerexpr'
        if self._is_ax_cls:
            name = kwargs['ArrayName']
            typ = kwargs['ArrayType']
            self.printt('length=new Object(__cid=-2, _int={})))'.format(len(n.values)))
            for i in range(0, len(n.values)):
                v = n.values[i]
                self.printt('; {0}._array_{1}.A[{2}] = '.format(name, typ.lower(), str(i)))
                v.accept(self, **kwargs)
                if typ in ['int', 'bit', 'char', 'double', 'float']:
                    self.printt('._{}'.format(typ))
            # self.printSepList(n.values)
            # self.printt('})')
        else:
            self.printt('length={}, A={{'.format(len(n.values)))
            self.printSepList(n.values)
            self.printt('})')            

    def findType(self, n, name):
        if name in n.symtab:
            return n.symtab[name]
        elif n.parentNode:
            return self.findType(n.parentNode, name)
        return None
            
    @v.when(ArrayAccessExpr)
    def visit(self, n, **kwargs):
        # print 'arrayaccessexpr'
        if self._is_ax_cls:
            typ = self.trans_ty(n.nameExpr.typee)
            if isinstance(n.nameExpr, FieldAccessExpr):
                fld = utils.find_fld(n.nameExpr, self.obj_struct)
                typ = self.trans_ty(fld.typee)
            elif n.nameExpr.name in n.nameExpr.symtab:
                typ = self.trans_ty(n.nameExpr.symtab[n.nameExpr.name].typee)
            elif not isinstance(n.nameExpr, MethodCallExpr):
                typ = self.trans_ty(utils.find_fld(n.nameExpr, self.obj_struct).typee) 
            if typ == 'byte': typ = 'char'
        n.nameExpr.accept(self, **kwargs)
        if self._is_ax_cls: self.printt('._array_{}'.format(typ.lower()))
        # self.printt('._array.A[')
        self.printt('.A[')
        n.index.accept(self, **kwargs)
        if self._is_ax_cls: self.unboxPrimitive(n.index)        
        self.printt(']')

    @v.when(MethodCallExpr)
    def visit(self, n, **kwargs):
        self.trans_call(n, **kwargs)

    @v.when(EnclosedExpr)
    def visit(self, n, **kwargs):
        self.printt('(')
        if n.inner: n.inner.accept(self, **kwargs)
        self.printt(')')

    @v.when(GeneratorExpr)
    def visit(self, n, **kwargs):
        if n.isHole and self._is_ax_cls:
            typ = self.trans_ty(n.typee)
            cid = self.primitiveIds[typ]
            self.printt('(new Object(__cid={0}, _{1}=??))'.format(cid, typ))
        elif n.isHole and not self._is_ax_cls:
            self.printt('??')            
        else:
            self.printt('{|')            
            # if 'Return' in kwargs:
            #     self.printArguments(n.exprs, sep=' |')
            # else:
            #     self.printSepList(n.exprs, sep=' |')
            if self._is_ax_cls:
                self.printArguments(n.exprs, sep=' |')
            else:
                self.printSepList(n.exprs, sep=' |')
            self.printt('|}')

    def boxPrimitiveType(self, expr, **kwargs):
        if isinstance(expr, UnaryExpr) and isinstance(expr.typee, PrimitiveType):
            typ = self.getUnboxPrimitiveType(expr.expr)
            cid = self.primitiveIds[typ]
            self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))
            expr.accept(self, **kwargs)
            self.printt('))')
        else:
            expr.accept(self, **kwargs)            
            
    @v.when(ConditionalExpr)
    def visit(self, n, **kwargs):
        self.printt('(')
        n.condition.accept(self, **kwargs)
        if (isinstance(n.condition, NameExpr) or isinstance(n.condition, MethodCallExpr)) and self._is_ax_cls:
            if isinstance(n.condition.typee, PrimitiveType):
                self.printt('._'+self.trans_ty(n.condition.typee))        
        self.printt(' ? ')
        if self._is_ax_cls:
            self.boxPrimitiveType(n.thenExpr, **kwargs)
        else:
            n.thenExpr.accept(self, **kwargs)
        self.printt(' : ')
        if self._is_ax_cls:
            self.boxPrimitiveType(n.elseExpr, **kwargs)
        else:
            n.elseExpr.accept(self, **kwargs)
        self.printt(')')

    @v.when(ThisExpr)
    def visit(self, n, **kwargs):
        if n.classExpr:
            n.classExpr.accept(self, **kwargs)
            self.printt('.')
        self.printt('self')

    @v.when(SuperExpr)
    def visit(self, n, **kwargs):
        if n.classExpr:
            n.classExpr.accept(self, **kwargs)
            self.printt('.')
        self.printt('super')

    @v.when(CastExpr)
    def visit(self, n, **kwargs):
        if self._is_ax_cls:
            typ = str(n.typee)        
            if isinstance(n.typee, PrimitiveType):
                self.printt('(')
                if typ == 'byte': typ = u'char'
                self.printt(typ)
                # self.trans_ty(n.typee, **kwargs)
                # n.typee.accept(self, **kwargs)
                self.printt(')')
            expr = n.expr
            count = 0
            while isinstance(expr, EnclosedExpr):
                self.printt('(')
                expr = expr.inner
                count += 1
            expr.accept(self, **kwargs)
            if isinstance(expr.typee, PrimitiveType) and not isinstance(expr, CastExpr):
                typ = str(expr.typee)
                if typ == u'byte': typ = u'char'
                self.printt('._'+typ)
            self.printt(')'*count)
            # n.expr.accept(self, **kwargs)
        else:
            if isinstance(n.typee, PrimitiveType):
                self.printt('(')
                n.typee.accept(self, **kwargs)
                self.printt(')')
            n.expr.accept(self, **kwargs)            
        
    @v.when(LiteralExpr)
    def visit(self, n, **kwargs):
        self.printt(n.name)

    @v.when(BooleanLiteralExpr)
    def visit(self, n, **kwargs):
        # self.printt(n.value)
        # if 'VariableDeclarationExpr' in kwargs or 'AssignExpr' in kwargs or 'MethodCallExpr' in kwargs:        
        if self._is_ax_cls: self.printt('(new Object(__cid=-4, _bit=')
        self.printt(n.value)
        if self._is_ax_cls: self.printt('))')
        # else:
        #     self.printt(n.value)
        
    @v.when(IntegerLiteralExpr)
    def visit(self, n, **kwargs):
        # self.printt(n.value)
        # if 'VariableDeclarationExpr' in kwargs or 'AssignExpr' in kwargs:        
        if self._is_ax_cls: self.printt('(new Object(__cid=-2, _int=')
        self.printt(n.value)
        if self._is_ax_cls: self.printt('))')
        # else:
        #     self.printt(n.value)

    @v.when(DoubleLiteralExpr)
    def visit(self, n, **kwargs):
        # self.printt(n.value)
        # if 'VariableDeclarationExpr' in kwargs or 'AssignExpr' in kwargs:  
        if self._is_ax_cls: self.printt('(new Object(__cid=-6, _double=')
        self.printt(n.value)
        if self._is_ax_cls: self.printt('))')
        # else:
        #     self.printt(n.value)
        
    @v.when(NullLiteralExpr)
    def visit(self, n, **kwargs):
        self.printt('null')

    @v.when(StringLiteralExpr)
    def visit(self, n, **kwargs):
        length = len(n.value) - n.value.count("\\n")
        if self._is_ax_cls:
            # self.printt('String_String_char_int_int(new Object(__cid=String()), Wrap_Array_char(new Array_char(length={1}+1, A="{0}")), 0, {1})'.format(n.value, len(n.value)))
            self.printt('String_String_char_int_int(new Object(__cid=String()), Wrap_Array_char(new Array_char(length=new Object(__cid=-2, _int={1}+1), A="{0}")), new Object(__cid=-2, _int=0), new Object(__cid=-2, _int={1}))'.format(n.value, length))
        else:
            self.printt('String_String_char_int_int(new Object(__cid=String()), new Array_char(length={1}+1, A="{0}"), 0, {1})'.format(n.value, length))

    @v.when(CharLiteralExpr)
    def visit(self, n, **kwargs):
        # self.printt("'")
        # self.printt(n.value)
        # self.printt("'")
        # if 'VariableDeclarationExpr' in kwargs or 'AssignExpr' in kwargs:  
        if self._is_ax_cls: self.printt('(new Object(__cid=-3, _char=')        
        self.printt("'")
        self.printt(n.value)
        self.printt("'")
        if self._is_ax_cls: self.printt('))')
        # else:
        #     self.printt("'")
        #     self.printt(n.value)
        #     self.printt("'")

    @v.when(InstanceOfExpr)
    def visit(self, n, **kwargs):
        cls = n.symtab.get(n.typee.name)
        n.expr.accept(self, **kwargs)
        self.printt('.__cid == {}()'.format(str(cls)))

        def subclss(allsubs):
            if not allsubs: return
            self.printt(' || ')
            n.expr.accept(self, **kwargs)
            self.printt('.__cid == {}()'.format(str(allsubs[0])))
            subclss(allsubs[1:])

        subclss(utils.all_subClasses(cls))

    # type
    @v.when(ClassOrInterfaceType)
    def visit(self, n, **kwargs):
        self.printt(self.trans_ty(n))
        # if n.isUsingDiamondOperator():
        #     self.printt('<>')
        # else:
        # self.printTypeArgs(n.typeArgs())

    @v.when(TypeParameter)
    def visit(self, n, **kwargs):
        # annotations

        self.printt(self.trans_ty(n.name))
        if n.typeBound:
            self.printSepList(n.typeBound, sep='&')

    @v.when(PrimitiveType)
    def visit(self, n, **kwargs):
        if self._is_ax_cls:
            self.printt('Object')
        else:
            self.printt(self.trans_ty(n))            

    @v.when(VoidType)
    def visit(self, n, **kwargs):
        self.printt(n.name)

    @v.when(ReferenceType)
    def visit(self, n, **kwargs):
        # print 'ReferenceType -- type: {} arrayCount: {}'.format(n, n.arrayCount)
        if self._is_ax_cls:
            self.printt('Object')
        else:
            if n.arrayCount:
                if u'lower' in kwargs and kwargs[u'lower']:
                    self.printt('array_{}'.format(self.trans_ty(n.typee)))
                else:
                    self.printt('Array_{}'.format(self.trans_ty(n.typee)))
            else:
                n.typee.accept(self, **kwargs)

    def trans(self, s, **kwargs):
        self.buf = cStringIO.StringIO()
        s.accept(self, **kwargs)
        return util.get_and_close(self.buf)

    def trans_ty(self, typ, **kwargs):
        if typ and isinstance(typ, ClassOrInterfaceType) or isinstance(typ, ReferenceType):
            cls = typ.symtab.get(typ.name)
            if cls and isinstance(cls, ImportDeclaration): r_ty = cls.cname()
            else: r_ty = str(cls) if cls else str(typ)
        else:
            r_ty = str(typ)

        # print 'typ {},{} -> {}'.format(str(typ), type(typ), r_ty)
        # we've already rewritten this type
        if r_ty in self.ty: r_ty = self.ty[r_ty] if convert else r_ty
        # Java types to Sketch types
        elif r_ty in CONVERSION_TYPES: r_ty = CONVERSION_TYPES[r_ty]
        # Unknown type, cast as Object for now
        else: r_ty = u'Object'
        # print('typ {} -> {}'.format(repr(str(typ)), r_ty))

        return r_ty

    def trans_faccess(self, n, **kwargs):
        logging.debug('accessing {}.{}:{}'.format(n.scope.name, n.field.name, n.beginLine))
        
        arr_access = False
        if isinstance(n, FieldAccessExpr) and self._is_ax_cls:
            if isinstance(n.scope.typee, ReferenceType) and n.scope.typee.arrayCount > 0 and n.field.name == 'length':
                arr_access = True
                # self.printt('._array_{}'.format(n.typee))
                
        fld = utils.find_fld(n, self.obj_struct)

        logging.debug('found field: {}'.format(str(fld)))
        if td.isStatic(fld):
            if isinstance(n.scope, ThisExpr) or n.scope.name == n.get_coid().name:
                self.printt(fld.name)
            elif type(n.parentNode) == AssignExpr and n == n.parentNode.target:
                self.printt('{}_s@{}('.format(fld.name, str(fld.get_coid())))
                n.parentNode.value.accept(self, **kwargs)
                self.printt(')')
                return False
            else:
                self.printt('{}_g@{}()'.format(fld.name, str(fld.get_coid())))
        else:            
            logging.debug('non-static field - type(n.scope): {}'.format(type(n.scope)))
            n.scope.accept(self, **kwargs)
            if arr_access and self._is_ax_cls:
                # typ = self.trans_ty(n.scope.typee)
                typ = str(n.scope.typee)
                # typ = str(n.typee)
                if typ == 'byte': typ = 'char'
                if typ not in [u'int', u'bit', u'float', u'double', u'char']:
                    typ = u'Object'
                self.printt('._array_{}'.format(typ.lower())) 
            self.printt('.{}'.format(str(fld)))

        logging.debug('***END FIELD ACCESS***\n')
        return True

    def trans_faccess_no_print(self, n, **kwargs):
        field_name = ''
        
        if isinstance(n, FieldAccessExpr):
            fld = utils.find_fld(n, self.obj_struct)
            name = self.trans_fld(fld)[1]
        else:
            name = n.name
            
        if isinstance(n, FieldAccessExpr) and (isinstance(n.scope, FieldAccessExpr) or isinstance(n.scope, NameExpr)):
            # (ty, nm, init) = self.trans_fld(n.scope)
            field_name += self.trans_faccess_no_print(n.scope) + '.'
        return field_name + name
    
    def trans_fld(self, fld):
        init = ''
        nm = str(fld)
        if td.isStatic(fld):
            nm = fld.name
            if fld.variable.init:
                init = ' = '
                kwargs = {}
                if isinstance(fld.variable.init, ArrayInitializerExpr):
                    # init += 'Wrap_Array_{0}(new Array_{0}('.format(self.trans_ty(fld.typee))
                    if self._is_ax_cls:
                        kwargs['ArrayName'] = nm
                        kwargs['ArrayType'] = self.trans_ty(fld.typee)
                        init += 'new Object(__cid=-1, _array_{0}=new Array_{0}('.format(self.trans_ty(fld.typee))
                    else:
                        init += 'new Array_{}('.format(self.trans_ty(fld.typee))                        
                init += self.trans(fld.variable.init, **kwargs)
                
                if isinstance(fld.variable.init, ArrayInitializerExpr) and self._is_ax_cls: init += ')'
        ty = self.trans_ty(fld.typee)
        if self._is_ax_cls:
            if fld.typee.name in fld.symtab:
                typ_cls = fld.symtab[fld.typee.name]
                if isinstance(typ_cls, ClassOrInterfaceDeclaration) and typ_cls.axiom:
                    ty = u'Object'
                
        if isinstance(fld.typee, ReferenceType) and int(fld.typee.arrayCount) > 0:
            if self._is_ax_cls:
                if len(fld.name) > 7 and fld.name[0:7]=='_array_':
                    ty = 'Array_{}'.format(self.trans_ty(fld.typee))                    
                else:
                    ty = 'Object'
            else:
                ty = 'Array_{}'.format(ty)                            
        return (ty, nm, init)

    def trans_params(self, ty_nm):
        (ty, nm) = ty_nm
        return ' '.join([self.trans_ty(ty), nm])

    def trans_call(self, callexpr, **kwargs):
        semi = kwargs.get('semi', True)
        tltr = copy.copy(self)
        tltr.indentation = ''        
        
        def write_call():
            tltr.buf = cStringIO.StringIO()
            if callexpr.scope:
                scp = tltr.trans(callexpr.scope)
                if not isinstance(scope, ClassOrInterfaceType):
                    callexpr.args = [NameExpr({u'name':scp})] + callexpr.args
            self.printt(callexpr.name)
            self.printArguments(callexpr.args)

        if callexpr.name in builtins:
            write_call()
            return
        
        logging.info('calling: {} from {}'.format(str(callexpr), callexpr.get_coid()))
        # 15.12.1 Compile-Time Step 1: Determine Class or Interface to Search
        if not callexpr.scope:
            cls = callexpr.get_coid()
        else:
            if isinstance(callexpr.scope, SuperExpr):
                # super . [TypeArguments] Identifier ( [ArgumentList] )
                sups = callexpr.get_coid().supers()
                if not sups:
                    raise Exception('Calling super with no super class {} in {}'.format(
                        callexpr, callexpr.get_coid()))
                cls = sups[0]
                scope = NameExpr({u'name':u'self'})
            elif isinstance(callexpr.scope, MethodCallExpr):
                if not callexpr.unbox:
                    (cls, _) = utils.get_scopes_list(callexpr)
                    m = cls.symtab.get(callexpr.scope.sig())
                    typ = m.typee
                    for t in cls.typeParameters:
                        if str(t) == str(m.typee):
                            typ = t.typeBound[0]
                    cls = cls.symtab.get(str(typ))
                else:
                    cls = callexpr.symtab[u'#unboxer_'+callexpr.name+'#']
            else:
                scope = utils.node_to_obj(callexpr.scope)
                if not scope: return
                # TypeName . [TypeArguments] Identifier
                if type(scope) == ClassOrInterfaceDeclaration: cls = scope
                # ExpressionName . [TypeArguments] Identifier
                # Primary . [TypeArguments] Identifier
                else:
                    logging.debug('scope: {} {} {}'.format(scope, scope.typee, type(scope)))
                    if not isinstance(scope, (ClassOrInterfaceType, ImportDeclaration)):
                        cls = None
                        if callexpr.name in scope.symtab:
                            cls = scope.symtab.get('{}_{}'.format(scope.typee, scope.name))
                            if cls:
                                nm = '{}_{}'.format(callexpr.name, cls.name)
                                callexpr.name = nm
                        if not cls:
                            pmdec = utils.get_parent(callexpr, MethodDeclaration)
                            pcls = callexpr.get_coid()
                            tparams = [p for p in pcls.typeParameters] + \
                                      [p for p in pmdec.typeParameters] if pmdec else []
                            tparam = [p for p in tparams if p.name == scope.typee.name]
                            if tparam:
                                tparam = tparam[0]
                                cls = scope.symtab.get(tparam.typeBound[0].name)
                            else:
                                cls = scope.symtab.get(scope.typee.name)
                    else:
                        cls = None
            # TODO: more possibilities

        def uninterpreted():
            (ftypes, scope) = utils.mtd_type_from_callexpr(callexpr)
            meta = ClassOrInterfaceDeclaration({u'@t':u'ClassOrInterfaceDeclaration',
                                                u'name':u'meta',})
            subs = utils.all_subClasses(scope.symtab.get(str(scope.typee.name)))
            meta.subClasses = subs
            meta.members = []

            # write uninterpreted function signature
            # add fun declaration as uninterpreted
            with open(os.path.join(self.sk_dir, 'meta.sk'), 'a') as f:
                trans_ftypes = set([tuple([self.trans_ty(convert(t)) for t in c]) for c in ftypes])
                for fun in [list(d) for d in trans_ftypes]:
                    if len(fun) > 1:
                        sig = '{}.{}.{}'.format(fun[0], fun[1], callexpr.name)
                    else:
                        sig = '{}.{}'.format(fun[0], callexpr.name)
                    if sig in self.unfuns: continue
                    self.unfuns.append(sig)
                    rtyp = self.trans_ty(fun.pop())                    
                    if self._is_ax_cls:
                        f.write('{} {}('.format(rtyp, str(callexpr)+'__uninterp'))
                    else:
                        f.write('{} {}('.format(rtyp, str(callexpr)))                        
                    if not isinstance(scope, ClassOrInterfaceType):
                        f.write('{} p0'.format(self.trans_ty(scope.typee)))
                        if len(fun) > 0: f.write(', ')
                    for i in range(len(fun)-1):
                        f.write('{} {}, '.format(self.trans_ty(fun[i]), 'p'+str(i+1)))
                    if len(fun) > 0: f.write('{} {}'.format(self.trans_ty(fun[-1]), 'p'+str(len(fun))))
                    f.write(')')
                    f.write(';')
                    f.write('\n')

                    if self._is_ax_cls:
                         args = []

                         f.write('Object {}('.format(str(callexpr)))
                         if not isinstance(scope, ClassOrInterfaceType):
                             args.append('p0');
                             f.write('{} p0'.format(self.trans_ty(scope.typee)))
                             if len(fun) > 0: f.write(', ')
                         for i in range(len(fun)-1):
                             args.append(self.trans_ty(fun[i]))
                             f.write('{} {}, '.format(self.trans_ty(fun[i]), 'p'+str(i+1)))
                         if len(fun) > 0: f.write('{} {}'.format(self.trans_ty(fun[-1]), 'p'+str(len(fun))))
                         f.write(') {\n  ')
                         cid = self.primitiveIds[rtyp]
                         f.write('return new Object(__cid={0}, _{1}='.format(cid, rtyp))
                         f.write('{}('.format(str(callexpr)+'__uninterp'))
                         if len(args) > 0:
                             f.write(args[0])
                         if len(args) > 1:
                             for a in args:                        
                                 f.write(', {}'.format(a))
                         f.write('));\n}')
                            
                    typ = {u'@t':u'PrimitiveType',u'type':{u'name':rtyp},} if rtyp in CONVERSION_TYPES \
                          else {u'@t':u'ClassOrInterfaceType',u'name': rtyp,}
                    mtd = MethodDeclaration({u'@t':u'MethodDeclaration',
                                             u'name':callexpr.name,
                                             u'type':typ,})
                    params = []
                    for i in range(len(fun)):
                        params.append(Parameter({u'@t':u'Parameter',
                                                 u'type':{u'@t':u'ClassOrInterfaceType',
                                                          u'name':self.trans_ty(fun[i])},
                                                 u'id':{u'@t':u'VariableDeclarator',
                                                        u'id':{u'@t':u'VariableDeclaratorId',
                                                               u'name':'p'+str(i+1),},},}))
                    mtd.parameters = params
                    mtd.parentNode = meta
                    meta.members.append(mtd)
                    meta.childrenNodes.append(mtd)
                    meta.symtab.update({mtd.name:mtd})
            return meta
        
        if not cls or isinstance(cls, ImportDeclaration): cls = uninterpreted()
        logging.debug('searching in class: {}'.format(cls))
        if isinstance(cls, TypeParameter):
            cls = callexpr.symtab.get(cls.typeBound[0].name)
            
        # Compile-Time Step 2: Determine Method Signature
        # 15.12.2.1. Identify Potentially Applicable Methods
        pots = self.identify_potentials(callexpr, cls)
        logging.debug('potentitals: {}'.format([str(m) for m in pots]))
        if not pots:
            uninterpreted()
            return

        # 15.12.2.2. Phase 1: Identify Matching Arity Methods Applicable by Strict Invocation
        strict_mtds = self.identify_strict(callexpr, pots)
        logging.debug('strict_applicable: {}'.format([str(m) for m in strict_mtds]))

        # 15.12.2.3. Phase 2: Identify Matching Arity Methods Applicable by Loose Invocation
        loose_mtds = self.identify_loose(callexpr, pots)
        logging.debug('loose_applicable: {}'.format([str(m) for m in loose_mtds]))

        # 15.12.2.4. Phase 3: Identify Methods Applicable by Variable Arity Invocation
        # TODO: this

        if not strict_mtds + loose_mtds:
            raise Exception('Unable to find applicable method for {} in {}'.format(str(callexpr), str(cls)))

        # 15.12.2.5. Choosing the Most Specific Method
        mtd = self.most_specific(list(set(strict_mtds + loose_mtds)))

        # 15.12.2.6. Method Invocation Type
        # TODO: ignoring this for now. Type will just be type of method

        # TODO: super?
        if cls.interface: invocation_mode = 'interface'
        elif cls.name == 'meta': invocation_mode = 'uninterpreted'
        else: invocation_mode = 'static' if td.isStatic(mtd) or td.isADT(mtd) else 'virtual'

        logging.debug('most_specific - name: {}, qualifying type: {}, invocation_mode: {}'. \
            format(str(mtd), type(mtd.typee), invocation_mode))

        is_ax = False
        mtd_call = None
        is_ax2 = callexpr.add_bang
        is_adt = False

        xform_name = ""
        
        if str(mtd).startswith("xform_"):
            xform_name = str(mtd).split('_')[2]
            # if not self._is_ax_cls:
            # _self = Parameter({u'id':{u'name':u'selff'},
            #                            u'type':{u'@t': u'ReferenceType', u'type': {u'@t':u'ClassOrInterfaceType', u'name':u'Object'},},},)
            # mtd.parameters[0] = _self
            
        # 15.12.4. Run-Time Evaluation of Method Invocation
        # 15.12.4.1. Compute Target Reference (If Necessary)
        if invocation_mode == 'static':            
            if (callexpr.scope and isinstance(callexpr.scope, ThisExpr)) or \
               str(callexpr.get_coid()) == str(mtd.get_coid()):
                self.printt('{}'.format(str(mtd)))
            else:
                self.printt('{}@{}'.format(str(mtd), str(mtd.get_coid())))
            self.printArguments(callexpr.args, xform_name)
            # self.printt(';')
        elif not callexpr.scope:
            self.printt('{}@{}'.format(str(mtd), str(cls)))
            self.printArguments([NameExpr({u'name':u'self'})] + callexpr.args, "")
        else:
            if type(callexpr.scope) == SuperExpr:
                self.printt('{}@{}'.format(str(mtd), str(cls)))
                self.printArguments([NameExpr({u'name':u'self'})] + callexpr.args, xform_name)
                logging.debug('**END CALL***\n')
                return            
            clss = [cls] + utils.all_subClasses(cls) if invocation_mode != 'uninterpreted' else \
                   utils.all_subClasses(cls)
            clss = [c for c in clss if not c.interface]
            logging.debug('subclasses: {}'.format([str(c) for c in clss]))

            scp = tltr.trans(callexpr.scope)
            args = [NameExpr({u'name':scp})] + callexpr.args
            conexprs = []
            conexprs2 = []            
            for c in reversed(clss): # start from bottom of hierarchy
                (_, mdec) = self.find_mtd(c, mtd.sig())
                if self._ax_clss != []:
                    if mdec:
                        if is_ax2: mdec.add_bang = True;
                        conexprs.append(self.make_dispatch(scp, c, mdec, args))
                        mdec.add_bang = False;
                    if mdec and mdec.adt and not mdec.pure:
                        is_ax = not callexpr.add_bang
                        callexpr.add_bang = is_ax
                    elif mdec and mdec.adt:
                        is_adt = True
                else:
                    if mdec: conexprs.append(self.make_dispatch(scp, c, mdec, args))    
            if invocation_mode == 'uninterpreted':
                (_, mdec) = self.find_mtd(cls, str(mtd))
                conexprs[-1].elseExpr = copy.copy(conexprs[-1].thenExpr)
                conexprs[-1].elseExpr.name = '{}@{}'.format(str(mdec), str(cls))
            # else: raise Exception('Non-static mode, no mtd {} in {}'.format(str(mtd), str(cls)))
            # need to foldr then reverse
            def combine(l, r):
                if type(mtd.typee) != VoidType: r.elseExpr = l
                else: r.elseStmt = l
                return r
            conexprs = reduce(combine, reversed(conexprs))
            if type(mtd.typee) != VoidType: self.printt('(')
            # DIFFERENT ARGS HERE THEN FOR UNBOXED
            self.print_dispatch(conexprs, is_adt, is_ax2, xform_name, mtd, **kwargs)
            if type(mtd.typee) != VoidType: self.printt(')')                
            # if is_ax and self._is_ax_cls:
            if is_ax and self._ax_clss != []:
                if u'unbox' in kwargs and kwargs[u'unbox'][0]:
                    self.printt('._')
                    kwargs[u'lower'] = True
                    kwargs[u'unbox'][1].accept(self, **kwargs)
                    kwargs[u'lower'] = False
                    
                self.printt('; ')
                callexpr.scope.accept(self, **kwargs)
                self.printt(' = ')
                callexpr.accept(self, **kwargs)
            
        logging.debug('**END CALL***\n')
        
    def identify_potentials(self, callexpr, cls):
        mtds = []
        call_arg_typs = callexpr.arg_typs()
        for key,val in cls.symtab.items():
            if type(val) != MethodDeclaration: continue
            tparam_names = [t.name for t in val.typeParameters]
            tparam_names.extend([t.name for t in val.get_coid().typeParameters])
            if self._is_ax_cls or callexpr.name.startswith('xform'):
                name = callexpr.name
                if val.adtType and callexpr.name != val.name and len(call_arg_typs) > 1:
                    name += '_'+'_'.join(map(str, call_arg_typs[1:]))
                if name == val.name and len(callexpr.args) == len(val.parameters):
                    if all([t[1].name in tparam_names or utils.is_subtype(t[0], t[1]) for t in
                               zip(call_arg_typs, val.param_typs())]):
                        mtds.append(val)
            else:
                if callexpr.name == val.name and len(callexpr.args) == len(val.parameters):
                    if all([t[1].name in tparam_names or utils.is_subtype(t[0], t[1]) for t in
                               zip(call_arg_typs, val.param_typs())]):
                        mtds.append(val)                
        return mtds

    def identify_strict(self, callexpr, mtds, **kwargs):
        pots = []
        arg_typs = callexpr.arg_typs()
        for m in mtds:
            param_typs = m.param_typs()
            if self.match_strict(arg_typs, param_typs):
                pots.append(m)
        return pots

    def match_strict(self, arg_typs, param_typs, **kwargs):
        for atyp,ptyp in zip(arg_typs, param_typs):
            if ptyp.name in [p.name for p in param_typs]: continue
            if not (self.identity_conversion(atyp,ptyp) or \
                    self.primitive_widening(atyp,ptyp) or \
                    self.reference_widening(atyp,ptyp)):
                return False
        return True

    def identify_loose(self, callexpr, mtds, **kwargs):
        pots = []
        arg_typs = callexpr.arg_typs()

        for m in mtds:
            param_typs = m.param_typs()
            if self.match_loose(arg_typs, param_typs, m.typeParameters): pots.append(m)
        return pots

    def match_loose(self, arg_typs, param_typs, typeParameters):
        # TODO: Spec says if the result is a raw type, do an unchecked conversion. Does this already happen?
        for atyp,ptyp in zip(arg_typs, param_typs):
            if ptyp.name in [p.name for p in param_typs]: continue
            if ptyp.name in [p.name for p in typeParameters] and not isinstance(atyp, PrimitiveType): continue
            # going to ignore, identity and widenings b/c they should be caught with strict
            if not (self.boxing_conversion(atyp, ptyp) or \
                    (self.unboxing_conversion(atyp, ptyp) and \
                     self.primitive_widening(utils.unbox[atyp.name], ptyp))): return False
        return True

    def most_specific(self, mtds, **kwargs):
        def most(candidate, others):
            ctypes = candidate.param_typs()
            for i in range(len(others)):
                # if the parameters of the candidate aren't less specific than all the parameters of other
                if not all([utils.is_subtype(t[0], t[1]) for t in
                            zip(ctypes, others[i].param_typs())]):
                    return False
            return True
        for mi in xrange(len(mtds)):
            if most(mtds[mi], mtds[:mi] + mtds[mi+1:]): return mtds[mi]
        raise Exception('Unable to find most specific method!')

    # Conversions
    def identity_conversion(self, typ1, typ2, **kwargs):
        return True if typ1.name == typ2.name else False

    def primitive_widening(self, typ1, typ2, **kwargs):
        t1 = typ1 if type(typ1) == unicode else typ1.name
        t2 = typ2 if type(typ2) == unicode else typ2.name
        return True if t1 in utils.widen and t2 in utils.widen[t1] else False

    def reference_widening(self, typ1, typ2, **kwargs):
        if not typ1 or not typ2: return False
        return utils.is_subtype(typ1, typ2)

    def boxing_conversion(self, typ1, typ2, **kwargs): # TODO: reference widening here
        return typ1.name in utils.box and utils.box[typ1.name] == typ2.name

    def unboxing_conversion(self, typ1, typ2, **kwargs):
        if typ1.name in utils.unbox:
            return utils.unbox[typ1.name] == typ2.name or \
                self.primitive_widening(utils.unbox[typ1.name], typ2.name)
        else: return False

    # dynamic dispatch
    def find_mtd(self, cls, descriptor, **kwargs):
        # check current class for method
        m = cls.symtab.get(descriptor)
        # remove import declarations and interfaces from super classes
        s = [c for c in [cs for cs in cls.supers() if not isinstance(cs, ImportDeclaration)] if not c.interface]
        if m: return (cls, m) # found it!
        elif s: return self.find_mtd(s[0], descriptor) # nope, check superclasses
        else: return (None, None) # doesn't exist

    def print_dispatch(self, c, is_adt, is_ax, xform_name, mtd, **kwargs):
        # we need to do this b/c the elseExpr's are going to have MethodCallExpr which
        # get handled differently
        if isinstance(c, ConditionalExpr):
            c.condition.accept(self, **kwargs)
            self.printt(' ? ')
            self.printt('{}'.format(c.thenExpr.name))
            self.printArguments(c.thenExpr.args, xform_name)
            self.printt(' : ')
            if isinstance(c.elseExpr, IntegerLiteralExpr): self.printt('0')
            elif isinstance(c.elseExpr, PrimitiveType):
                if self._is_ax_cls or mtd.boxedRet:
                    self.printt('null')
                else:
                    if not is_ax:
                        if c.elseExpr.name == u'double' or c.elseExpr.name == u'float' or \
                           c.elseExpr.name == u'long': self.printt('0.0')
                        if c.elseExpr.name == u'int' or c.elseExpr.name == u'boolean' or c.\
                           elseExpr.name == u'bit' or c.elseExpr.name == u'short': self.printt('0')
                        if c.elseExpr.name == u'char' or c.elseExpr.name == u'byte': self.printt("'\\0'")
                    else:
                        self.printt('null')
            elif isinstance(c.elseExpr, (ClassOrInterfaceType, ReferenceType)): self.printt('null')
            else: self.print_dispatch(c.elseExpr, is_adt, is_ax, xform_name, mtd)
        elif isinstance(c, MethodCallExpr):
            self.printt('{}('.format(c.name))
            self.printArguments(c.args, xform_name)
            self.printt(')')
        else:
            if is_ax and self._is_ax_cls:
                self.printt('(')
                c.condition.accept(self, **kwargs)
                self.printt(' ? ')
                self.printt('{}'.format(c.thenStmt.name))
                self.printArguments(c.thenStmt.args, xform_name)
                self.printt(' : ')
                if type(c.elseStmt) == IntegerLiteralExpr:
                    self.printt('null)'.format(c.elseStmt.value))
                else:
                    # self.printLn()
                    # self.printt('else ')
                    self.print_dispatch(c.elseStmt, is_adt, is_ax, xform_name, mtd)
            else:
                self.printt('if (')
                c.condition.accept(self, **kwargs)
                self.printt(') { ')
                self.printt('{}'.format(c.thenStmt.name))
                self.printArguments(c.thenStmt.args, xform_name)
                self.printt(';')
                self.printt(' }')
                if type(c.elseStmt) == IntegerLiteralExpr:
                    self.printLn()
                    self.printt('else {{ 0; }}'.format(c.elseStmt.value))
                else:
                    self.printLn()
                    self.printt('else ')
                    self.print_dispatch(c.elseStmt, is_adt, is_ax, xform_name, mtd)

    def make_dispatch(self, scope, S, mdec, args, **kwargs):
        d = {
            "@t": "",
            "condition": {
                "@t": "BinaryExpr",
                "op": {
                    "name": "equals"
                },
                "left": {
                    "@t": "NameExpr",
                    "name": "",
                },
                "right": {
                    "@t": "IntegerLiteralExpr",
                    "value": "",
                },
            },
            "thenExpr": {
                "@t": "MethodCallExpr",
                "scope": {
                    "@t": "NameExpr",
                    "name": "",
                },
                "name": {
                    "name": "",
                },
                "args": {},
            },
            "elseExpr": {
                "@t": "IntegerLiteralExpr",
                "value": "0",
            },
        }
        d['condition']['left']['name'] = '.'.join([str(scope), '__cid'])
        d['condition']['right']['value'] = '{}()'.format(str(S))
        if type(mdec.typee) != VoidType:
            d['thenExpr']['scope']['name'] = scope
            coid = mdec.get_coid()
            if coid.interface: raise Exception('{} unimplemented from {}'.format(mdec, coid))
            d['thenExpr']['name'] = '@'.join([str(mdec), str(coid)])
            dis = ConditionalExpr(d)
            dis.thenExpr.args = args
            dis.elseExpr = mdec.typee
        else:
            d['thenStmt'] = d.pop('thenExpr')
            d['elseStmt'] = d.pop('elseExpr')
            d['thenStmt']['scope']['name'] = scope
            d['thenStmt']['name'] = '@'.join([str(mdec), str(mdec.get_coid())])
            dis = IfStmt(d)
            dis.thenStmt.args = args
        return dis

    # xname = name of xform
    # xform = body of xform (I believe this starts as an empty switch statement)
    #         it's what returned by get_xform() from method_declaration
    # stmts = body of axiom declaration (i.e. return add!(t, e1))
    def trans_xform(self, xname, xform, stmts, **kwargs):
        # SEEMS TO ALWAYS BE "self"???
        #    It seems like maybe this is for each selector in the switch
        #    They aren't actually initialized to not "self" until later
        label = str(xform.stmt.selector)

        # Unwraps function calls that are not the direct return
        #   This is so that "return size(h)+1" works
        #   i.e. size(h) is unwrapped
        # Wraps primitive returns from xforms
        #   i.e. "return 1"
        def wrapUnwrap(s, *args):
            # Handle function call unwrapping
            if isinstance(s, MethodCallExpr):
                name = s.name +"_"+self.getParentCls(s).name
                mdec = s.symtab.get('m'+str(s))
                if mdec and mdec.adtName:
                    
                    # get method declaration for corresponding Axiom Method Call
                    ax_mtd = mdec.symtab.get('m'+mdec.adtName)
                    # if not isDirectParentReturn(s):
                    if isinstance(ax_mtd.typee, PrimitiveType):
                        # s = self.unwrapBox(s, ax_mtd.typee.name)
                        s.ax_typ = self.trans_ty(ax_mtd.typee)
                            
            # # Handle primitive wrapping
            # if isDirectParentReturn(s):
            #     if isinstance(s.typee, PrimitiveType) and s.typee.name != 'null':
            #         s = self.wrapPrimitive(s)
                    
            return s

        # calls wrapUnwrap on n. then calls it on n's children and replaces
        #    n's children with wrapUnwrap'ed versions. Finally, for specific n's
        #    it replaces other relavent values with newly updated children
        def wrapUnwrapPrimitives(n, *args):
            # wrapUnwrap(n, *args)
            # for c in n.childrenNodes:
            #     wrapUnwrap(c, *args)
            prevChildren = n.childrenNodes
            n = wrapUnwrap(n, *args)
            children = []
            if n != None:
                for c in prevChildren:
                    children.append(wrapUnwrapPrimitives(c, *args))
                n.childrenNodes = children
                if isinstance(n, BinaryExpr):
                    n.left = children[0]
                    n.right = children[1]
                if isinstance(n, ReturnStmt):
                    n.expr = children[0]
                if isinstance(n, ConditionalExpr):
                    n.condition = children[0]
                    n.thenExpr = children[1]
                    n.elseExpr = children[2]
                if isinstance(n, ObjectCreationExpr):
                    if n.box:
                        n.children = n.args[0]
                        if isinstance(n.args[0], BinaryExpr):
                            n.args[0].left = children[0]
                            n.args[0].right = children[1]
                    
            return n

        # return true if the "direct" parent of expr is Return
        #    means the statement is "return expr" or
        #    "return if _ then expr else expr"
        def isDirectParentReturn(expr):
            if expr.parentNode:
                if isinstance(expr.parentNode, ConditionalExpr):
                    if expr.parentNode.condition == expr:
                        return False
                    else:
                        return isDirectParentReturn(expr.parentNode)
                elif isinstance(expr.parentNode, ReturnStmt):
                    return True
            return False
        
        # Transform xform function call into appropriate function call
        #    i.e A return of type add! in JSketch translated to a call to xform_addb
        def change_call(s, *args):
            # if s is a variable, t will be it's associated VariableDeclarator
            t = s.symtab.get(s.name)
            # if method call is reference to ADT, it needs to be changed
            #    could be recursive call to xform
            #    could be call to different xform
            #    could be call to ADT wrapper (for bang return types)
            #    could be call to outside function
            if isinstance(s, MethodCallExpr):
                # checks if there is an xform version of the function call
                name = 'xform_{}'.format(str(s))
                mdec = s.symtab.get('m'+name)
                if mdec or not s.pure:                 
                    # alter method call name to be xform call                   
                    s.name = 'xform_{}'.format(s.name)

                    if not s.pure:
                        s.name += "b"                                        
                        
            elif isinstance(s, ObjectCreationExpr):
                print("OBJ")
                        
            elif isinstance(t, VariableDeclarator):
                # if this variable is a parameter of the first argument
                #   (i.e. axiomParameter) add symbol to the table for
                #   this value
                if t.axiomParameter():
                    param_check = '#'+t.name+'_axparam#'
                    if param_check in s.symtab:
                        real_name = s.symtab[param_check]
                        s.axparam = real_name
                        
        # apply change_call to every statement, and every statement's children
        #    note that stmt is changed first, followed by it's children
        for s in stmts:
            utils.walk(change_call, s)

        # alter stmts to wrap and unwrap primitives appropriately
        new_stmts = []
        for s in stmts:
            new_stmts.append(wrapUnwrapPrimitives(s))
            
        return new_stmts
    
    # wrap prim in an object creation expr
    #   This is done when returning a primitive from an xform (must be an object)
    def wrapPrimitive(self, prim):
        primToBox = {
            u'int':u'Integer',
            u'byte':u'Byte',
            u'boolean':u'Boolean',
            u'short':u'Short',
            u'long':u'Long',
            u'float':u'Float',
            u'double':u'Double',
            u'char':u'Character'
        }

        boxName = primToBox[str(prim.typee)]
        
        if (isinstance(prim.typee, ReferenceType) and prim.typee.arrayCount > 0) or isinstance(prim, ArrayCreationExpr):
            return prim
        else:
            # Only create the expr if wrapper library included
            if boxName in prim.symtab:
                objCreExpr = ObjectCreationExpr({u'type':prim.symtab[boxName],u'box':True,},)
            else:
                logging.error('{} wrapper not found. Perhaps jsketch was run without including it.'.format(boxName))
                sys.exit()
        objCreExpr.symtab = prim.symtab
        # objCreExpr.symtab[prim.name] = prim
        objCreExpr.args = [prim]
        
        return objCreExpr

    # Returns highest parent that isn't compilation unit
    #    I believe this will always be the member class
    def getParentCls(self, expr):
        if expr.parentNode:
            if not isinstance(expr.parentNode, CompilationUnit):
                return self.getParentCls(expr.parentNode)
        return expr
    
    # creates wrapper for primType for unbox. This handles the instance when a return
    #    from an xform has primitive type and is being used as such (i.e not return)
    def unwrapBox(self, expr, primType=''):
        primToBox = {
            u'int':u'Integer',
            u'byte':u'Byte',
            u'boolean':u'Boolean',
            u'short':u'Short',
            u'long':u'Long',
            u'float':u'Float',
            u'double':u'Double',
            u'char':u'Character'
        }
        primToUnbox = {
            u'int':u'mintValue',
            u'byte':u'mbyteValue',
            u'boolean':u'mbooleanValue',
            u'short':u'mshortValue',
            u'long':u'mlongValue',
            u'float':u'mfloatValue',
            u'double':u'mdoubleValue',
            u'char':u'mcharValue'
        }
        if primType == '':
            mnm = "m"+expr.name
            parent = self.getParentCls(expr)
            primType = parent.symtab[mnm].typee.name
        boxType = primToBox[primType]
        unboxFuncName = primToUnbox[primType]
        unboxFuncName_nom = unboxFuncName.replace('m', '', 1)
        box = expr.symtab[boxType]
        unboxFunc = box.symtab[unboxFuncName]

        newExpr = MethodCallExpr({u'name':unboxFuncName_nom,
                                  u'type':{u'@t':u'ClassOrInterfaceType',
                                           u'name':primType,},
                                  u'args':[],
                                  u'pure':True,
                                  u'unbox':True,})

        newExpr.symtab[u'#unboxer_'+unboxFuncName_nom+'#'] = box
        newExpr.scope = expr
        
        return newExpr
    
    
        
    def indent(self): self._level += 1
    def unindent(self): self._level -= 1

    def makeIndent(self):
        for i in xrange(self._level): self._buf.write(self._indentation)

    def printt(self, arg, **kwargs):
        if not self._indented:
            self.makeIndent()
            self.indented = True
        self.buf.write(arg)

    def printLn(self, arg=None, **kwargs):
        if arg:
            self.printt(arg)
        self.buf.write('\n')
        self.indented = False

    def printSepList(self, args, xform_name = "", **kwargs):
        if xform_name != "":
            if len(args) > 0 and args[0].axparam:
                if (args[0].axparam.split('.')[-1] != u'self'):
                    args[0].axparam += u'._'+xform_name.lower()
        if args:
            lenn = len(args)
            for i in xrange(lenn):
                args[i].accept(self, **kwargs)
                if i+1 < lenn: self.printt('{} '.format(kwargs.get('sep', ',')))

    def printSepListHarness(self, args, **kwargs):
        if args:
            lenn = len(args)
            for i in xrange(lenn):
                if isinstance(args[i].typee, PrimitiveType):
                    self.buf.write('{0} {1}'.format(self.trans_ty(args[i].typee), '__'+str(args[i].idd)))
                else:
                    args[i].accept(self, **kwargs)
                if i+1 < lenn: self.printt('{} '.format(kwargs.get('sep', ',')))   

    def printSepListObjectCreationExpr(self, args, **kwargs):
        if args:
            lenn = len(args)
            for i in xrange(lenn):
                if isinstance(args[i], BinaryExpr) or isinstance(args[i], UnaryExpr) or isinstance(args[i], ArrayAccessExpr):
                    if isinstance(args[i].typee, PrimitiveType) or str(args[i].typee) in [u'int', u'bit', u'float', u'double']:
                        typ = self.trans_ty(args[i].typee)
                        cid = self.primitiveIds[typ]
                        self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))
                        args[i].accept(self, **kwargs)                        
                        self.printt('))')
                    else:
                        args[i].accept(self, **kwargs)                        
                else:
                    args[i].accept(self, **kwargs)
                if i+1 < lenn: self.printt('{} '.format(kwargs.get('sep', ',')))   
                
    def printArguments(self, args, xform_name = "", **kwargs):
        self.printt('(')
        if self._is_ax_cls:
            if args:
                lenn = len(args)
                for i in xrange(lenn):
                    if (isinstance(args[i], BinaryExpr) or isinstance(args[i], UnaryExpr) or isinstance(args[i], ArrayAccessExpr)):
                        if isinstance(args[i].typee, PrimitiveType) or str(args[i].typee) in [u'int', u'bit', u'float', u'double']:
                            typ = self.trans_ty(args[i].typee)
                            cid = self.primitiveIds[typ]
                            self.printt('(new Object(__cid={0}, _{1}='.format(cid, typ))
                            args[i].accept(self, **kwargs)                        
                            self.printt('))')
                        else:
                            args[i].accept(self, **kwargs)                        
                    else:
                       if i == 0 and xform_name != "":
                           self.printt('(new Object(__cid=-2, _{}='.format(xform_name.lower()))
                           args[i].accept(self, **kwargs)
                           self.printt('))')
                       else:
                           args[i].accept(self, **kwargs)
                    if i+1 < lenn: self.printt('{} '.format(kwargs.get('sep', ',')))
        else:
            self.printSepList(args, xform_name)
        self.printt(')')
        
    def printMods(self, mods, **kwargs):
        if td.isGenerator(mods): self.printt('generator ')

    def printTypeArgs(self, args, **kwargs):
        self.printTypeParameters(args)
        
    def printTypeParameters(self, args):
        if args:
            self.printt('<')
            self.printSepList(args)
            self.printt('>')

    @property
    def mtd(self): return self._mtd
    @mtd.setter
    def mtd(self, v): self._mtd = v

    @property
    def buf(self): return self._buf
    @buf.setter
    def buf(self, v): self._buf = v

    @property
    def indented(self): return self._indented
    @indented.setter
    def indented(self, v): self._indented = v

    @property
    def indentation(self): return self._indentation
    @indentation.setter
    def indentation(self, v): self._indentation = v

    @property
    def sk_dir(self): return self._sk_dir
    @sk_dir.setter
    def sk_dir(self, v): self._sk_dir = v

    @property
    def num_mtds(self): return self._num_mtds
    @num_mtds.setter
    def num_mtds(self, v): self._num_mtds = v

    @property
    def mtd(self): return self._mtd
    @mtd.setter
    def mtd(self, v):
        self._mtd = v
        self._cls = v.get_coid()

    @property
    def cls(self): return self._cls
    @cls.setter
    def cls(self, v): self._cls = v

    @property
    def ty(self): return self._ty
    @ty.setter
    def ty(self, v): self._ty = v

    @property
    def flds(self): return self._flds
    @flds.setter
    def flds(self, v): self._flds = v

    @property
    def post_mtds(self): return self._post_mtds
    @post_mtds.setter
    def post_mtds(self, v): self._post_mtds = v
