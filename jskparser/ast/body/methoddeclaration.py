#!/usr/bin/env python

from . import _import

from .bodydeclaration import BodyDeclaration

from ..typeparameter import TypeParameter
from ..comments.comment import Comment

from ..stmt.switchstmt import SwitchStmt

class MethodDeclaration(BodyDeclaration):
    def __init__(self, kwargs={}):
        super(MethodDeclaration, self).__init__(kwargs)
        locs = _import()
        
        # int modifiers
        self._modifiers = kwargs.get(u'modifiers', 0)

        # This is the return type and will be stored as a child of the method
        typdct = kwargs.get(u'type')
        self._type = locs[typdct[u'@t']](typdct)

        # List<Parameter> parameters
        params = kwargs.get(u'parameters', [])
        self._params = params
        self._parameters = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                               params.get(u'@e', [])) if params else []

        # List<TypeParameter>
        typeParameters = kwargs.get(u'typeParameters', [])
        self._typeParameters = map(lambda x: TypeParameter(x) if u'@t' in x else [],
                                   typeParameters.get(u'@e', [])) if typeParameters else []

        # int arrayCount;
        self._arrayCount = kwargs.get(u'arrayCount', 0)

        # List<ReferenceType> throws_;
        throws = kwargs.get(u'throws_', [])
        self._throws = map(lambda x: locs[u'ReferenceType'](x) if u'@t' in x else [],
                           throws.get(u'@e', [])) if throws else []

        # BlockStmt body;
        body = kwargs.get(u'body')
        self._body = locs[u'BlockStmt'](body) if body else None

        if self._body and self._body.childrenNodes:
            chs = filter(lambda c: not isinstance(c, Comment), self._body.childrenNodes)
            if chs: chs[0].in_set = set(map(lambda x: x.lbl, self._parameters))

        self._adt = False
        self._pure = False
        self._default = False
        self._constructor = False
        if self.annotations:
            self._adt = any(map(lambda a: str(a) == 'adt', self.annotations))
            self._pure = any(map(lambda a: str(a) == 'pure', self.annotations))
            self._default = any(map(lambda a: str(a) == 'default', self.annotations))
            self._constructor = any(map(lambda a: str(a) == 'constructor', self.annotations))            

        self._bang = kwargs.get(u'bang', False)
        self._adtType = kwargs.get(u'adtType', False)

        self._adtName = kwargs.get(u'adtName', None)

        self._add_bang = False
        
        self.add_as_parent(self.parameters+self.typeParameters+[self.typee]+self.throws+[self.body])

    @property
    def add_bang(self): return self._add_bang
    @add_bang.setter
    def add_bang(self, v): self._add_bang = v

    @property
    def params(self): return self._params
    @params.setter
    def params(self, v): self._params = v
    
    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v

    @property
    def typee(self): return self._type
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def parameters(self): return self._parameters
    @parameters.setter
    def parameters(self, v): self._parameters = v

    @property
    def body(self): return self._body
    @body.setter
    def body(self, v): self._body = v

    @property
    def arrayCount(self): return self._arrayCount
    @arrayCount.setter
    def arrayCount(self, v): self._arrayCount = v

    @property
    def throws(self): return self._throws
    @throws.setter
    def throws(self, v): self._throws = v

    @property
    def typeParameters(self): return self._typeParameters
    @typeParameters.setter
    def typeParameters(self, v): self._typeParameters = v

    @property
    def bang(self): return self._bang
    @bang.setter
    def bang(self, v): self._bang = v

    @property
    def adt(self): return self._adt
    @adt.setter
    def adt(self, v): self._adt = v

    @property
    def constructor(self): return self._constructor
    @constructor.setter
    def constructor(self, v): self._constructor = v
    
    @property
    def pure(self): return self._pure
    @pure.setter
    def pure(self, v): self._pure = v

    @property
    def default(self): return self._default
    @default.setter
    def default(self, v): self._default = v

    @property
    def adtType(self): return self._adtType
    @adtType.setter
    def adtType(self, v): self._adtType = v

    @property
    def adtName(self): return self._adtName
    @adtName.setter
    def adtName(self, v): self._adtName = v

    def param_typs(self): return map(lambda p: p.typee, self.parameters)
    def param_names(self): return map(lambda p: p.name, self.parameters)

    def get_xform(self):
        from .xform import Xform
        x = self.body.stmts[0]
        if not isinstance(x, Xform):
            raise Exception('Trying to get Xform from {} but body isnt an Xform'.format(self))
        return x

    def sig(self):
        return 'm{}'.format(str(self))

    @staticmethod
    def add_switch(adt_mtds, param, entries1):
        for e in entries1:
            if len(e.stmts) > 0:
                MethodDeclaration.add_switch(adt_mtds, param, e.stmts[0].entries)
            else:                
                entries2 = []
                for a in adt_mtds:
                    entries2.append({u'@t':u'SwitchEntryStmt',
                                     u'label':{u'@t':u'NameExpr',u'name':a.name.capitalize(),},},)
                switch = SwitchStmt({u'@t':u'SwitchStmt', u'selector':{u'@t':u'NameExpr',u'name':param.name},
                                     u'entries':{u'@e':entries2,},},)
                e.stmts.append(switch)
                    
    def add_switch_depth(self, adt_mtds, param):
        MethodDeclaration.add_switch(adt_mtds, param, self.body.stmts[0].stmt.entries)

    def name_no_nested(self, isCons):
        def ptypes():
            params = []
            ps = self.parameters
            # if not isCons:
            #     ps = ps[1:]
            for p in ps:
                typ = ''
                if p.idd: typ = str(p.typee.name)
                else: typ = str(p.method.typee)
                # if typ.capitalize() in map(str, self.parentNode.typeParameters):
                #     print("\t\tHERE43: "+str(typ.capitalize()))
                #     typ = u'Object'
                params.append(typ)
            return params
        return u'_'.join([self.name] + ptypes())
        
    def __str__(self):
        name = self.name
        if self.adtType:
            name = '_'.join(name.split('_')[:2])
            # return self.name_no_nested(False)
        
        params = map(self.sanitize_ty, map(lambda p: p.typee.name, self.parameters))
        if self.adt:
            params = ["Object"]+params

        # name = self.name+'b' if self.add_bang else self.name
        name = name+'b' if self.add_bang else name
            
        return u'_'.join([self.sanitize_ty(name)] + params)
