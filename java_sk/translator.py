#!/usr/bin/env python
import cStringIO
import logging
import copy
import os

from . import util
from . import convert
from . import builtins

import visit as v

from ast import Operators as op
from ast import AssignOperators as assignop

from ast.utils import utils
from ast.node import Node
from ast.importdeclaration import ImportDeclaration
from ast.typeparameter import TypeParameter

from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.constructordeclaration import ConstructorDeclaration
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.parameter import Parameter
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.variabledeclarator import VariableDeclarator
from ast.body.variabledeclaratorid import VariableDeclaratorId

from ast.stmt.blockstmt import BlockStmt
from ast.stmt.returnstmt import ReturnStmt
from ast.stmt.ifstmt import IfStmt
from ast.stmt.forstmt import ForStmt
from ast.stmt.whilestmt import WhileStmt
from ast.stmt.continuestmt import ContinueStmt
from ast.stmt.minrepeatstmt import MinrepeatStmt
from ast.stmt.emptystmt import EmptyStmt
from ast.stmt.expressionstmt import ExpressionStmt
from ast.stmt.assertstmt import AssertStmt
from ast.stmt.assumestmt import AssumeStmt
from ast.stmt.switchstmt import SwitchStmt
from ast.stmt.switchentrystmt import SwitchEntryStmt
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

    @v.on('node')
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """

    @v.when(Node)
    def visit(self, n):
        logging.error('unimplemented node: {}'.format(n))
        # if isinstance(n, Type): print 'un:', n
        # map(lambda x: x.accept(self), n.childrenNodes)

    # body
    @v.when(ConstructorDeclaration)
    def visit(self, n):
        cls = n if isinstance(n, ClassOrInterfaceDeclaration) else utils.get_coid(n)
        etypes = cls.enclosing_types()
        self.printt('Object {0}_{0}'.format(str(cls)))
        ptypes = n.param_typs()
        if cls.isinner(): self.printt('_{}'.format(str(utils.get_coid(cls))))
        if ptypes: self.printt('_{}'.format('_'.join(map(str, ptypes))))
        self.printTypeParameters(n.typeParameters)

        p = [Parameter({u'id':{u'name':u'self'},
                       u'type':{u'@t':u'ClassOrInterfaceType',u'name':u'Object'}})]
        if cls.isinner():
            p.append(Parameter({u'id':{u'name':u'self_{}'.format(len(etypes)-1)},
                                u'type':{u'@t':u'ClassOrInterfaceType',u'name':u'Object'}}))
        n.parameters = p + n.parameters

        self.printt('(')
        self.printSepList(n.parameters)
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
            n.body.accept(self)
        self.printLn()

    @v.when(MethodDeclaration)
    def visit(self, n):
        if utils.get_coid(n).interface: return
        self.printMods(n)
        if td.isHarness(n):
            self.printt('harness ')
            n.body.stmts = [u'Object self = Object_Object(new Object(__cid=Object()));'] + n.body.stmts
        n.typee.accept(self)
        self.printt(' ')
        if type(n.parentNode) == ObjectCreationExpr:
            self.printt('_'.join([str(n), utils.anon_nm(n).name]))
        else: self.printt(str(n))
        self.printTypeParameters(n.typeParameters)
        
        self.printt('(')

        if not td.isStatic(n) and not td.isHarness(n):
            ty = self.trans_ty(utils.get_coid(n))
            self.printt('{} self'.format(ty))
            if n.parameters: self.printt(', ')
        self.printSepList(n.parameters)
        self.printt(')')

        for i in xrange(n.arrayCount): self.printt('[]')

        if not n.body: self.printt(';')
        else:
            self.printt(' ')
            n.body.accept(self)
        self.printLn()

    @v.when(Parameter)
    def visit(self, n):
        self.buf.write(' '.join([self.trans_ty(n.typee), str(n.idd)]))

    @v.when(VariableDeclarator)
    def visit(self, n):
        # print 'VariableDeclarator'
        if n.init:
            self.printt(' ')
            n.idd.accept(self)
            self.printt(' = ')
            if isinstance(n.init, ArrayInitializerExpr):
                self.printt('new ')
                n.typee.accept(self)
                self.printt('(')
            n.init.accept(self)
        else:
            self.printt(' ')
            n.idd.accept(self)

    @v.when(VariableDeclaratorId)
    def visit(self, n):
        self.printt(str(n))

    # stmt
    @v.when(BlockStmt)
    def visit(self, n):
        self.printLn('{')
        if n.stmts:
            self.indent()
            for s in n.stmts:
                if type(s) == str or type(s) == unicode:
                    self.printLn(s)
                else:
                    s.accept(self)
                    self.printLn()
            self.unindent()
        self.printt('}')

    @v.when(ReturnStmt)
    def visit(self, n):
        self.printt('return')
        if n.expr:
            self.printt(' ')
            n.expr.accept(self)
        self.printt(';')

    @v.when(IfStmt)
    def visit(self, n):
        self.printt('if (')
        n.condition.accept(self)
        thenBlock = isinstance(n.thenStmt, BlockStmt)
        self.printt(') ')
        if not thenBlock: self.indent()
        n.thenStmt.accept(self)
        if not thenBlock: self.unindent()
        if n.elseStmt:
            self.printLn()
            elseIf = isinstance(n.elseStmt, IfStmt)
            elseBlock = isinstance(n.elseStmt, BlockStmt)
            if elseIf or elseBlock: self.printt('else ')
            else:
                self.printLn('else')
                self.indent()
            n.elseStmt.accept(self)
            if not (elseIf or elseBlock): self.unindent()

    @v.when(ForStmt)
    def visit(self, n):
        self.printt('for (')
        if n.init: self.printSepList(n.init)
        self.printt('; ')
        if n.compare: n.compare.accept(self)
        self.printt('; ')
        if n.update: self.printSepList(n.update)
        self.printt(') ')
        n.body.accept(self)

    @v.when(WhileStmt)
    def visit(self, n):
        self.printt('while (')
        if n.condition: n.condition.accept(self)
        self.printt(') ')
        n.body.accept(self)

    @v.when(MinrepeatStmt)
    def visit(self, n):
        self.printt('minrepeat ')
        n.body.accept(self)

    @v.when(ExpressionStmt)
    def visit(self, n):
        n.expr.accept(self)
        self.printt(';')

    @v.when(AssertStmt)
    def visit(self, n):
        self.printt('assert ')
        n.check.accept(self)
        if n.msg:
            self.printt(' : ')
            n.msg.accept(self)
        self.printt(';')

    @v.when(AssumeStmt)
    def visit(self, n):
        self.printt('assume ')
        n.expr.accept(self)
        self.printt(';')

    @v.when(SwitchStmt)
    def visit(self, n):
        for e in xrange(len(n.entries)):
            self.printt('if (') if e == 0 else self.printt('else if (')
            n.selector.accept(self)
            self.printt(' == ')
            n.entries[e].label.accept(self)
            self.printLn(') {')
            self.indent()
            for s in n.entries[e].stmts: s.accept(self)
            self.unindent()
            self.printLn()
            self.printLn('}')

    @v.when(SwitchEntryStmt)
    def visit(self, n):
        pass

    @v.when(ExplicitConstructorInvocationStmt)
    def visit(self, n):
        if n.isThis:
            self.printt('self')
        else:
            if n.expr:
                n.expr.accept(self)
                self.printt('.')
            cls = utils.get_coid(n)
            sups = cls.supers()
            if not sups: exit('Calling super with  with no super class: {}'.format(str(cls)))
            def ty(a):
                return a.typee.name if type(a) != NameExpr else n.symtab[a.name].typee.name
            self.printt('_'.join([str(sups[0]), str(sups[0])] + map(ty, n.args)))
            self.printt('@{}'.format(str(sups[0])))
        self.printt(u'(self')
        if n.args: self.printt(', ')
        self.printSepList(n.args)
        self.printt(');')

    @v.when(ContinueStmt)
    def visit(self, n):
        self.printt('continue')
        if n.idd:
            self.printt(' {}'.format(n.idd))
        self.printt(';')

    @v.when(EmptyStmt)
    def visit(self, n): pass

    # expr
    @v.when(NameExpr)
    def visit(self, n):
        obj = utils.node_to_obj(n)
        if type(obj) == FieldDeclaration:
            if td.isStatic(obj):
                self.printt(obj.name)
                return
            this = utils.get_coid(n)
            obj_cls = utils.get_coid(obj)
            if obj.name in this.symtab and this == obj_cls:
                i = ''
            else:
                etypes = this.enclosing_types()
                if etypes:
                    for (i,j) in zip(xrange(len(etypes)), reversed(etypes)):
                        if j == obj_cls: break
                # this is the index of the class where the field lives
            slf = 'self{}'.format(i)
            self.printt('{}.{}'.format(slf, str(obj)))
        else: self.printt(n.name)

    @v.when(VariableDeclarationExpr)
    def visit(self, n):
        # print 'VariableDeclarationExpr'
        n.typee.accept(self)
        # self.printt(' ')
        self.printSepList(n.varss)

    @v.when(AssignExpr)
    def visit(self, n):
        # print 'AssignExpr'
        if type(n.target) == FieldAccessExpr:
            v = self.trans_faccess(n.target)
            if v:
                self.printt(' ')
                self.printt(assignop[n.op.upper()])
                self.printt(' ')
                n.value.accept(self)
        else:
            n.target.accept(self)
            self.printt(' ')
            self.printt(assignop[n.op.upper()])
            self.printt(' ')
            n.value.accept(self)

    @v.when(FieldAccessExpr)
    def visit(self, n):
        self.trans_faccess(n)

    @v.when(UnaryExpr)
    def visit(self, n):
        self.printt(UnaryExpr.PRE_OPS.get(n.op, ''))
        n.expr.accept(self)
        self.printt(UnaryExpr.POST_OPS.get(n.op, ''))

    @v.when(BinaryExpr)
    def visit(self, n):
        n.left.accept(self)
        self.printt(' ')
        self.printt(op[n.op.upper()])
        self.printt(' ')
        n.right.accept(self)

    @v.when(ObjectCreationExpr)
    def visit(self, n):
        # print 'ObjectCreationExpr:', n, n.beginLine
        obj_cls = n.symtab.get(n.typee.name)
        if isinstance(obj_cls, ReferenceType): obj_cls = self.trans_ty(obj_cls)
        enclosing_cls = obj_cls.enclosing_types()[-1] \
            if type(obj_cls) == ClassOrInterfaceDeclaration and obj_cls.isinner() else None
        if n.scope:
            n.getScope.accept(self)
            self.printt('.')
        if n.args:
            typs = []
            for a in n.args:
                if type(a) == FieldAccessExpr:
                    tname = utils.find_fld(a, self.obj_struct).typee.name
                elif not a.typee:
                    t = n.symtab.get(a.name)
                    if t:
                        tname = t.typee.name
                    else:
                        print a, type(a)
                else:
                    tname = a.typee.name
                typs.append(tname)

            self.printt('{0}_{0}_'.format(str(obj_cls)))
            if enclosing_cls: self.printt('{}_'.format(str(enclosing_cls)))
            self.printt('_'.join(typs))
        else:
            self.printt('{0}_{0}'.format(str(obj_cls)))
            if enclosing_cls: self.printt('_{}'.format(str(enclosing_cls)))

        self.printt('(new Object(__cid={}())'.format(str(obj_cls)))
        if enclosing_cls: self.printt(', self')
        if n.args: self.printt(', ')
        self.printSepList(n.args)
        self.printt(')')

    @v.when(ArrayCreationExpr)
    def visit(self, n):
        # print 'arraycreationexpr'
        self.printt('new Array_{}('.format(self.trans_ty(n.typee)))
        if n.dimensions:
            for d in n.dimensions:
                self.printt('sz=')
                d.accept(self)
            self.printt(')')
            # for c in xrange(n.arrayCount):
            #     self.printt('[]')
        else:
            n.initializer.accept(self)

    @v.when(ArrayInitializerExpr)
    def visit(self, n):
        # print 'arrayinitializerexpr'
        self.printt('sz={}, A={{'.format(len(n.values)))
        self.printSepList(n.values)
        self.printt('})')

    @v.when(ArrayAccessExpr)
    def visit(self, n):
        # print 'arrayaccessexpr'
        n.nameExpr.accept(self)
        self.printt('.A[')
        n.index.accept(self)
        self.printt(']')

    @v.when(MethodCallExpr)
    def visit(self, n):
        self.trans_call(n)

    @v.when(EnclosedExpr)
    def visit(self, n):
        self.printt('(')
        if n.inner: n.inner.accept(self)
        self.printt(')')

    @v.when(GeneratorExpr)
    def visit(self, n):
        if n.isHole: self.printt('??')
        else:
            self.printt('{| ')
            self.printSepList(n.exprs, ' | ')
            self.printt(' |}')

    @v.when(ConditionalExpr)
    def visit(self, n):
        n.condition.accept(self)
        self.printt(' ? ')
        n.thenExpr.accept(self)
        self.printt(' : ')
        n.elseExpr.accept(self)

    @v.when(ThisExpr)
    def visit(self, n):
        if n.classExpr:
            n.classExpr.accept(self)
            self.printt('.')
        self.printt('self')

    @v.when(SuperExpr)
    def visit(self, n):
        if n.classExpr:
            n.classExpr.accept(self)
            self.printt('.')
        self.printt('super')

    @v.when(CastExpr)
    def visit(self, n):
        if isinstance(n.typee, PrimitiveType):
            self.printt('(')
            n.typee.accept(self)
            self.printt(')')
        n.expr.accept(self)

    @v.when(BooleanLiteralExpr)
    def visit(self, n):
        self.printt(n.value)

    @v.when(IntegerLiteralExpr)
    def visit(self, n):
        self.printt(n.value)

    @v.when(DoubleLiteralExpr)
    def visit(self, n):
        self.printt(n.value)

    @v.when(NullLiteralExpr)
    def visit(self, n):
        self.printt('null')

    @v.when(StringLiteralExpr)
    def visit(self, n):
        self.printt('String_String_char_int_int(new Object(__cid=String()), new Array_char(sz={1}+1, A="{0}"), 0, {1})'.format(n.value, len(n.value)))

    @v.when(CharLiteralExpr)
    def visit(self, n):
        self.printt("'")
        self.printt(n.value)
        self.printt("'")

    @v.when(InstanceOfExpr)
    def visit(self, n):
        cls = n.symtab.get(n.typee.name)
        n.expr.accept(self)
        self.printt('.__cid == {}()'.format(str(cls)))

        def subclss(allsubs):
            if not allsubs: return
            self.printt(' || ')
            n.expr.accept(self)
            self.printt('.__cd == {}()'.format(str(allsubs[0])))
            subclss(allsubs[1:])

        subclss(utils.all_subClasses(cls))

    # type
    @v.when(ClassOrInterfaceType)
    def visit(self, n):
        self.printt(self.trans_ty(n))
        if n.isUsingDiamondOperator():
            self.printt('<>')
        else:
            self.printTypeArgs(n.typeArgs())

    @v.when(TypeParameter)
    def visit(self, n):
        # annotations

        self.printt(self.trans_ty(n.name))
        if n.typeBound:
            self.printSepList(n.typeBound, '&')

    @v.when(PrimitiveType)
    def visit(self, n):
        self.printt(self.trans_ty(n))

    @v.when(VoidType)
    def visit(self, n):
        self.printt(n.name)

    @v.when(ReferenceType)
    def visit(self, n):
        # print 'ReferenceType -- arrayCount: {}'.format(n.arrayCount)
        if n.arrayCount:
            self.printt('Array_{}'.format(self.trans_ty(n.typee)))
        else:
            n.typee.accept(self)

    def trans(self, s):
        self.buf = cStringIO.StringIO()
        s.accept(self)
        return util.get_and_close(self.buf)

    def trans_ty(self, typ, convert=True):
        # tname = str(typ)
        # _tname = typ.sanitize_ty(typ.name.strip()) if not isinstance(typ, unicode) and not isinstance(typ, str) else typ
        r_ty = str(typ)
        # r_ty = _tname
        # if typ and (type(typ) == ClassOrInterfaceType or type(typ) == ReferenceType):
        #     cls = typ.symtab.get(typ.name)
        #     tname = str(cls)
        #     print '_tname:', _tname

        # we've already rewritten this type
        if r_ty in self.ty: r_ty = self.ty[r_ty] if convert else r_ty
        # Java types to Sketch types
        elif r_ty in CONVERSION_TYPES: r_ty = CONVERSION_TYPES[r_ty]
        # Unknown type, cast as Object for now
        else: r_ty = u'Object'

        if typ and type(typ) == ReferenceType:
            if typ.arrayCount > 0: r_ty = 'Array_{}'.format(r_ty)
            
        return r_ty

    def trans_faccess(self, n):
        logging.debug('accessing {}.{}'.format(n.scope.name, n.field.name))
        fld = utils.find_fld(n, self.obj_struct)
        logging.debug('found field: {}'.format(str(fld)))
        if td.isStatic(fld):
            if isinstance(n.scope, ThisExpr) or n.scope.name == utils.get_coid(n).name:
                self.printt(fld.name)
            elif type(n.parentNode) == AssignExpr and n == n.parentNode.target:
                self.printt('{}_s@{}('.format(fld.name, str(utils.get_coid(fld))))
                n.parentNode.value.accept(self)
                self.printt(')')
                return False
            else:
                self.printt('{}_g@{}()'.format(fld.name, str(utils.get_coid(fld))))
        else:
            logging.debug('non-static field - type(n.scope): {}'.format(type(n.scope)))
            n.scope.accept(self)
            self.printt('.{}'.format(str(fld)))

        logging.debug('***END FIELD ACCESS***\n')
        return True

    def trans_fld(self, fld):
        init = ''
        nm = str(fld)
        if td.isStatic(fld):
            nm = fld.name
            if fld.variable.init:
                init = ' = '
                if isinstance(fld.variable.init, ArrayInitializerExpr):
                    init += 'new {}('.format(self.trans_ty(fld.typee))
                init += self.trans(fld.variable.init)
        return (self.trans_ty(fld.typee), nm, init)

    def trans_params(self, (ty, nm)):
        return ' '.join([self.trans_ty(ty), nm])

    def trans_call(self, callexpr):
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
            
        logging.info('calling: {} from {}'.format(str(callexpr), utils.get_coid(callexpr)))
        # 15.12.1 Compile-Time Step 1: Determine Class or Interface to Search
        if not callexpr.scope:
            cls = utils.get_coid(callexpr)
        else:
            if type(callexpr.scope) == SuperExpr:
                # super . [TypeArguments] Identifier ( [ArgumentList] )
                sups = utils.get_coid(callexpr).supers()
                if not sups:
                    raise Exception('Calling super with no super class {} in {}'.format(
                        callexpr, utils.get_coid(callexpr)))
                cls = sups[0]
                scope = NameExpr({u'name':u'self'})
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
                        cls = scope.symtab.get(scope.typee.name)
                    else:
                        cls = None
            # TODO: more possibilities

        def uninterpreted():
            (ftypes, scope) = utils.mtd_type_from_callexpr(callexpr)
            # write call
            write_call()

            # write uninterpreted function signature
            # add fun declaration as uninterpreted
            with open(os.path.join(self.sk_dir, 'meta.sk'), 'a') as f:
                trans_ftypes = set([tuple(map(self.trans_ty, map(convert, c))) for c in ftypes])
                for fun in [list(d) for d in trans_ftypes]:
                    f.write('{} {}('.format(self.trans_ty(fun.pop()), callexpr.name))
                    if not isinstance(scope, ClassOrInterfaceType):
                        f.write('{} p0'.format(self.trans_ty(scope.typee)))
                        if len(fun) > 0: f.write(', ')
                    for i in range(len(fun)-1):
                        f.write('{} {}, '.format(self.trans_ty(fun[i]), 'p'+str(i+1)))
                    if len(fun) > 0: f.write('{} {}'.format(self.trans_ty(fun[-1]), 'p'+str(len(fun))))
                    f.write(');\n')

        logging.debug('searching in class: {}'.format(cls))
        if not cls:
            uninterpreted()
            return

        # Compile-Time Step 2: Determine Method Signature
        # 15.12.2.1. Identify Potentially Applicable Methods
        pots = self.identify_potentials(callexpr, cls, [])
        if not pots:
            uninterpreted()
            return

        logging.debug('potentitals: {}'.format(map(lambda m: str(m), pots)))

        # 15.12.2.2. Phase 1: Identify Matching Arity Methods Applicable by Strict Invocation
        strict_mtds = self.identify_strict(callexpr, pots)
        logging.debug('strict_applicable: {}'.format(map(lambda m: str(m), strict_mtds)))

        # 15.12.2.3. Phase 2: Identify Matching Arity Methods Applicable by Loose Invocation
        loose_mtds = self.identify_loose(callexpr, pots)
        logging.debug('loose_applicable: {}'.format(map(lambda m: str(m), loose_mtds)))

        # 15.12.2.4. Phase 3: Identify Methods Applicable by Variable Arity Invocation
        # TODO: this

        if not strict_mtds + loose_mtds:
            raise Exception('Unable to find applicable method for {} in {}'.format(str(callexpr), str(cls)))

        # 15.12.2.5. Choosing the Most Specific Method
        mtd = self.most_specific(strict_mtds + loose_mtds)

        # 15.12.2.6. Method Invocation Type
        # TODO: ignoring this for now. Type will just be type of method

        # TODO: super?
        if cls.interface: invocation_mode = 'interface'
        else: invocation_mode = 'static' if td.isStatic(mtd) else 'virtual'

        logging.debug('most_specific - name: {}, qualifying type: {}, invocation_mode: {}'. \
            format(str(mtd), type(mtd.typee), invocation_mode))

        # 15.12.4. Run-Time Evaluation of Method Invocation
        # 15.12.4.1. Compute Target Reference (If Necessary)
        if invocation_mode == 'static':
            if (callexpr.scope and isinstance(callexpr.scope, ThisExpr)) or \
               str(utils.get_coid(callexpr)) == str(utils.get_coid(mtd)):
                self.printt('{}'.format(str(mtd), str(utils.get_coid(mtd))))
            else:
                self.printt('{}@{}'.format(str(mtd), str(utils.get_coid(mtd))))
            self.printArguments(callexpr.args)
        elif not callexpr.scope:
            self.printt(str(mtd))
            self.printArguments([NameExpr({u'name':u'self'})] + callexpr.args)
        else:
            if type(callexpr.scope) == SuperExpr:
                self.printt('{}@{}'.format(str(mtd), str(cls)))
                self.printArguments([NameExpr({u'name':u'self'})] + callexpr.args)
                logging.debug('**END CALL***\n')
                return
            clss = filter(lambda c: not c.interface, [cls] + utils.all_subClasses(cls))
            logging.debug('subclasses: {}'.format(map(lambda c: str(c), clss)))

            tltr.buf = cStringIO.StringIO()
            scp = tltr.trans(callexpr.scope)
            args = [NameExpr({u'name':scp})] + callexpr.args

            # tltr.buf = cStringIO.StringIO()
            # scp = tltr.trans(callexpr.scope)

            conexprs = []
            for c in reversed(clss): # start from bottom of hierarchy
                (cls, mdec) = self.find_mtd(c, str(mtd))
                if cls: conexprs.append(self.make_dispatch(scp, c, mdec, args))
                else: raise Exception('Non-static mode, no mtd {} in {}'.format(str(mtd), str(cls)))
            # need to foldr then reverse
            def combine(l, r):
                if type(mtd.typee) != VoidType: r.elseExpr = l
                else: r.elseStmt = l
                return r
            conexprs = reduce(combine, reversed(conexprs))
            if type(mtd.typee) != VoidType: self.printt('(')
            self.print_dispatch(conexprs)
            if type(mtd.typee) != VoidType: self.printt(')')

        logging.debug('**END CALL***\n')

    def identify_potentials(self, callexpr, cls, mtds):
        mtds = []
        for key,val in cls.symtab.items():
            if type(val) != MethodDeclaration: continue
            if callexpr.name == val.name and len(callexpr.args) == len(val.parameters):
                mtds.append(val)
        return mtds

    def identify_strict(self, callexpr, mtds):
        pots = []
        arg_typs = callexpr.arg_typs()
        for m in mtds:
            param_typs = m.param_typs()
            if self.match_strict(arg_typs, param_typs): pots.append(m)
        return pots

    def match_strict(self, arg_typs, param_typs):
        for atyp,ptyp in zip(arg_typs, param_typs):
            return self.identity_conversion(atyp,ptyp) or \
                self.primitive_widening(atyp,ptyp) or \
                self.reference_widening(atyp,ptyp)
        # if there are no arguments
        return True

    def identify_loose(self, callexpr, mtds):
        pots = []
        arg_typs = callexpr.arg_typs()

        for m in mtds:
            param_typs = m.param_typs()
            if self.match_loose(arg_typs, param_typs): pots.append(m)
        return pots

    def match_loose(self, arg_typs, param_typs):
        # TODO: Spec says if the result is a raw type, do an unchecked conversion. Does this already happen?
        for atyp,ptyp in zip(arg_typs, param_typs):
            # going to ignore, identity and windenings b/c they should be caught with strict
            # TODO: spec says boxing then reference_widening, dont know what that means
            if self.boxing_conversion(atyp, ptyp): return True
            elif self.unboxing_conversion(atyp, ptyp):
                if self.primitive_widening(utils.unbox[atyp.name], ptyp): return True
                else: return True
            else: return False
        # if there are no arguments
        return True

    def most_specific(self, mtds):
        def most(candidate, others):
            ctypes = candidate.param_typs()
            for i in range(len(others)):
                # if the parameters of the candidate aren't less specific than all the parameters of other
                if not all(map(lambda t: utils.is_subtype(t[0], t[1]),
                               zip(ctypes, others[i].param_typs()))):
                    return False
            return True
        for mi in xrange(len(mtds)):
            if most(mtds[mi], mtds[:mi] + mtds[mi+1:]): return mtds[mi]
        return []

    # Conversions
    def identity_conversion(self, typ1, typ2):
        return True if typ1.name == typ2.name else False

    def primitive_widening(self, typ1, typ2):
        t1 = typ1 if type(typ1) == unicode else typ1.name
        t2 = typ2 if type(typ2) == unicode else typ2.name
        return True if t1 in utils.widen and t2 in utils.widen[t1] else False

    def reference_widening(self, typ1, typ2):
        if not typ1 or not typ2: return False
        return utils.is_subtype(typ1, typ2)

    def boxing_conversion(self, typ1, typ2): # TODO: reference widening here
        return typ1.name in utils.box and utils.box[typ1.name] == typ2.name

    def unboxing_conversion(self, typ1, typ2):
        if typ1.name in utils.unbox:
            return utils.unbox[typ1.name] == typ2.name or \
                self.primitive_widening(utils.unbox[typ1.name], typ2.name)
        else: return False

    # dynamic dispatch
    def find_mtd(self, cls, descriptor):
        # check current class for method
        m = cls.symtab.get(descriptor)
        # remove import declarations and interfaces from super classes
        s = [c for c in [cs for cs in cls.supers() if not isinstance(cs, ImportDeclaration)] if not c.interface]
        if m: return (cls, m) # found it!
        elif s: return self.find_mtd(s[0], descriptor) # nope, check superclasses
        else: return (None, None) # doesn't exist

    def print_dispatch(self, c):
        # we need to do this b/c the elseExpr's are going to have MethodCallExpr which
        # get handled differently
        if type(c) == ConditionalExpr:
            c.condition.accept(self)
            self.printt(' ? ')
            self.printt('{}'.format(c.thenExpr.name))
            self.printArguments(c.thenExpr.args)
            self.printt(' : ')
            if isinstance(c.elseExpr, IntegerLiteralExpr): self.printt('0')
            elif isinstance(c.elseExpr, PrimitiveType):
                # print 'name:', c.elseExpr.name
                if c.elseExpr.name == u'double': self.printt('0.0')
                if c.elseExpr.name == u'int': self.printt('0')
                if c.elseExpr.name == u'char': self.printt("'\\0'")
            elif isinstance(c.elseExpr, (ClassOrInterfaceType, ReferenceType)): self.printt('null')
            else: self.print_dispatch(c.elseExpr)
        else:
            self.printt('if (')
            c.condition.accept(self)
            self.printt(') { ')
            self.printt('{}'.format(c.thenStmt.name))
            self.printArguments(c.thenStmt.args)
            self.printt('; }')
            if type(c.elseStmt) == IntegerLiteralExpr:
                self.printLn()
                self.printt('else {{ 0; }}'.format(c.elseStmt.value))
            else:
                self.printLn()
                self.printt('else ')
                self.print_dispatch(c.elseStmt)

    def make_dispatch(self, scope, S, mdec, args):
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
            d['thenExpr']['name'] = '@'.join([str(mdec), str(utils.get_coid(mdec))])
            dis = ConditionalExpr(d)
            dis.thenExpr.args = args
            dis.elseExpr = mdec.typee
        else:
            d['thenStmt'] = d.pop('thenExpr')
            d['elseStmt'] = d.pop('elseExpr')
            d['thenStmt']['scope']['name'] = scope
            d['thenStmt']['name'] = '@'.join([str(mdec), str(utils.get_coid(mdec))])
            dis = IfStmt(d)
            dis.thenStmt.args = args
        return dis

    def indent(self): self._level += 1
    def unindent(self): self._level -= 1

    def makeIndent(self):
        for i in xrange(self._level): self._buf.write(self._indentation)

    def printt(self, arg):
        if not self._indented:
            self.makeIndent()
            self.indented = True
        self.buf.write(arg)

    def printLn(self, arg=None):
        if arg:
            self.printt(arg)
        self.buf.write('\n')
        self.indented = False

    def printSepList(self, args, sep=','):
        if args:
            lenn = len(args)
            for i in xrange(lenn):
                args[i].accept(self)
                if i+1 < lenn: self.printt('{} '.format(sep))

    def printArguments(self, args):
        self.printt('(')
        self.printSepList(args)
        self.printt(')')

    def printMods(self, mods):
        if td.isGenerator(mods): self.printt('generator ')

    def printTypeArgs(self, args):
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
        self._cls = utils.get_coid(v)

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
