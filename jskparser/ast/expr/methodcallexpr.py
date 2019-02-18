#!/usr/bin/env python

from __future__ import absolute_import
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
from ..body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ..body.methoddeclaration import MethodDeclaration

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

        self._add_bang = False

        self._ax_typ = ''

    @property
    def ax_typ(self): return self._ax_typ
    @ax_typ.setter
    def ax_typ(self, v): self._ax_typ = v
        
    @property
    def add_bang(self): return self._add_bang
    @add_bang.setter
    def add_bang(self, v): self._add_bang = v
        
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
            if obj == self:
                cls = self.get_coid()
            else:
                cls = self.symtab.get(str(obj.typee))
            if isinstance(cls, TypeParameter):
                cls = self.symtab.get(str(cls.typeBound))
            if cls:
                mtd = cls.symtab.get(self.sig())
                if not mtd:
                    mtd = self.getMtd(cls)
            if mtd: return mtd.typee
        if not mtd:
            mtd = sym.get(str(self))
            if not mtd:
                # try the scopes class
                if obj == self:
                    cls = self.get_coid()
                else:
                    cls = sym.get(str(obj.typee))
                if isinstance(cls, TypeParameter):
                    cls = sym.get(str(cls.typeBound))
                    if not cls:
                        cls = sym.get(u'Object')
                mtd = cls.symtab.get(self.name)
                if not mtd:
                    mtd = self.getMtd(cls)
                if not mtd:
                    mtd = cls.symtab.get('m'+self.name)
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
    
    def getMtd(self, cls):
        pots = self.identify_potentials(self, cls)
        if not pots:
            return None

        strict_mtds = self.identify_strict(self, pots)

        loose_mtds = self.identify_loose(self, pots)

        if not strict_mtds + loose_mtds:
            return None
            
        # 15.12.2.5. Choosing the Most Specific Method
        mtd = self.most_specific(list(set(strict_mtds + loose_mtds)))

        return mtd
        
    def identify_potentials(self, callexpr, cls):
        mtds = []
        call_arg_typs = callexpr.arg_typs()
        for key,val in cls.symtab.items():
            if type(val) != MethodDeclaration: continue
            tparam_names = map(lambda t: t.name, val.typeParameters)
            tparam_names.extend(map(lambda t: t.name, val.get_coid().typeParameters))

            if callexpr.name == val.name and len(callexpr.args) == len(val.parameters):
                if all(map(lambda t: t[1].name in tparam_names or utils.is_subtype(t[0], t[1]),
                           zip(call_arg_typs, val.param_typs()))):
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
            if ptyp.name in map(lambda p: p.name, param_typs): continue
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
            if ptyp.name in map(lambda p: p.name, param_typs): continue
            if ptyp.name in map(lambda p: p.name, typeParameters) and not isinstance(atyp, PrimitiveType): continue
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
                if not all(map(lambda t: utils.is_subtype(t[0], t[1]), \
                               zip(ctypes, others[i].param_typs()))):
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
                    if str(typ) in self.symtab:
                        typ2 = self.symtab[str(typ)]
                        if isinstance(typ2, TypeParameter):
                            typ = ClassOrInterfaceDeclaration({u'name':u'Object'})
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
        name = self.name+'b' if self._add_bang else self.name
        if a:
            return '_'.join([self.sanitize_ty(name)] + \
                            map(lambda a: self.sanitize_ty(a.name), a))
        else:
            return self.name        
