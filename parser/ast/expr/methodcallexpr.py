#!/usr/bin/env python

from . import _import

from .expression import Expression
from .fieldaccessexpr import FieldAccessExpr
from .thisexpr import ThisExpr

from ..type.classorinterfacetype import ClassOrInterfaceType

from ..utils import utils

class MethodCallExpr(Expression):
    def __init__(self, kwargs={}):
        super(MethodCallExpr, self).__init__(kwargs)
        locs = _import()

        # Expression scope
        scope = kwargs.get(u'scope', {})
        self._scope = locs[scope[u'@t']](scope) if scope else None

        # List<Type> typeArgs;

        # Expression args
        args = kwargs.get(u'args', {})
        self._args = map(lambda x: locs[x[u'@t']](x) if u'@t' in x else [],
                         args.get(u'@e', [])) if args else []

    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, v): self._scope = v

    @property
    def args(self): return self._args
    @args.setter
    def args(self, v): self._args = v

    # this is going to be weird. traverse tree until a type or expressionstmt is found
    @property
    def typee(self):
        obj = utils.node_to_obj(self.scope) if self.scope else self
        sym = obj.symtab
        # first look for this methed in the current scope
        mtd = sym.get(self.name)
        if not mtd:
            ftypes = utils.mtd_type_from_callexpr(self)
            return ClassOrInterfaceType({u'@t': u'ClassOrInterfaceType', u'name': unicode(ftypes[0][-1])})
        else: return mtd.typee

    @typee.setter
    def typee(self, v): self._typee = v

    def sig(self):
        atyps = ','.join(map(str, self.arg_typs())) if self.args else ''
        return '{} {}({});'.format(str(self.typee), str(self), atyps)

    def arg_typs(self):
        typs = []
        for a in self.args:
            if type(a) == FieldAccessExpr:
                # TODO: if a field from an imported class is only used in a method call
                # this will fail :(
                fld = utils.find_fld(a, None)
                if not fld: return None
                typ = fld.typee
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
