#!/usr/bin/env python

import itertools

from . import _import

from .expression import Expression
from .fieldaccessexpr import FieldAccessExpr
from .thisexpr import ThisExpr
from .nameexpr import NameExpr

from ..type.primitivetype import PrimitiveType
from ..type.classorinterfacetype import ClassOrInterfaceType

from ..typeparameter import TypeParameter
from ..utils import utils

class MethodCallExpr(Expression):
    def __init__(self, kwargs={}):
        super(MethodCallExpr, self).__init__(kwargs)
        locs = _import()

        # Expression scope
        scope = kwargs.get(u'scope', {})
        self._scope = locs[scope[u'@t']](scope) if scope else None

        # List<Type> typeArgs;

        # List<Expression> args;
        args = kwargs.get(u'args', {})
        self._args = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                         args.get(u'@e', [])) if args else []

        self.add_as_parent([self.scope]+self.args)

        self._pure = kwargs.get(u'pure', {})

        self._unbox = kwargs.get(u'unbox', False)

    @property
    def unbox(self): return self._unbox
    @unbox.setter
    def unbox(self, v): self._unbox = v
        
    @property
    def pure(self): return self._pure
    @pure.setter
    def pure(self, v): self._pure = v
        
    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, v): self._scope = v

    @property
    def args(self): return self._args
    @args.setter
    def args(self, v): self._args = v

    @property
    def typee(self):
        if self.name == u'equals': return PrimitiveType({u'type': {u'name':u'boolean'}})
        obj = utils.node_to_obj(self.scope) if self.scope else self
        sym = obj.symtab
        # first look for this methed in the current scope
        sig = self.sig()
        if not self._pure:
            if sig[1:6] != "xform":
                sig = "a"+sig[1:]
                sig = sig.replace("_", "b_", 1)
        mtd = sym.get(sig)
        if not mtd:
            # check for equals
            cls = self.symtab.get(str(obj.typee))
            if isinstance(cls, TypeParameter):
                cls = self.symtab.get(str(cls.typeBound))
            mtd = cls.symtab.get(self.sig())
            if mtd: return mtd.typee
        if not mtd:
            mtd = sym.get(str(self))
            if not mtd:
                # try the scopes class
                cls = sym.get(str(obj.typee))
                if isinstance(cls, TypeParameter):
                    cls = sym.get(str(cls.typeBound))
                mtd = cls.symtab.get(self.name)
                if mtd:
                    return mtd.typee
                else:   # check for method signature using type parameters from cls
                    nm = self.sig().split('_')
                    args = nm[1:]
                    nm = nm[0]
                    tps = map(str, cls.typeParameters)
                    if len(args) == 1:
                        nms = map(lambda n: '_'.join([nm, n]), tps)
                    else:
                        nms = map(lambda n: '_'.join([nm]+list(n)), list(itertools.chain(itertools.product(tps,args), itertools.product(args,tps))))
                        nms.extend(map(lambda n: '_'.join([nm]+list(n)), list(itertools.chain(itertools.product(tps, tps)))))
                    for n in nms:
                        if cls.symtab.get(n): return cls.symtab.get(n).typee

                ftypes = utils.mtd_type_from_callexpr(self)
                return ClassOrInterfaceType({u'@t': u'ClassOrInterfaceType',
                                             u'name': unicode(ftypes[0][0][-1])})
        return mtd.typee
            
    @typee.setter
    def typee(self, v): self._typee = v

    def sig(self):
        return 'm{}'.format(str(self))
        # atyps = ','.join(map(str, self.arg_typs())) if self.args else ''
        # return '{} {}({});'.format(str(self.typee), str(self), atyps)

    def arg_typs(self):
        typs = []
        for a in self.args:
            # print type(a), a
            if isinstance(a, FieldAccessExpr):
                # TODO: if a field from an imported class is only used in a method call
                # this will fail :(
                fld = utils.find_fld(a, None)
                if not fld: return None
                typ = fld.typee
            elif isinstance(a, NameExpr):
                t = a.parentNode.symtab.get(a.name)
                if isinstance(t, NameExpr):
                    while t.parentNode:
                        t = t.parentNode
                        t = t.symtab.get(t.name)
                        if not t:
                            raise Exception('Unable to find VarDec in {} and all parents.'.format(self.name))
                        if not isinstance(t, NameExpr):
                            typ = t.typee
                            break
                else:
                    typ = t.typee
            elif isinstance(a, MethodCallExpr):
                typ = a.typee
            elif isinstance(a, ThisExpr):
                typ = utils.get_coid(self)
            elif not a.typee:
                typ = self.symtab[a.name].typee
            else:
                typ = a.typee
            typs.append(typ)
        return typs

    def __str__(self):
        a = self.arg_typs()
        if a:
            return '_'.join([self.sanitize_ty(self.name)] + \
                            map(lambda a: self.sanitize_ty(a.name), a))
        else:
            return self.name
