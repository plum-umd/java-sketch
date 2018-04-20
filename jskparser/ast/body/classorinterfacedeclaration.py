#!/usr/bin/env python

from . import _import

from .typedeclaration import TypeDeclaration

from ..typeparameter import TypeParameter
from ..importdeclaration import ImportDeclaration

from ..type.classorinterfacetype import ClassOrInterfaceType

class ClassOrInterfaceDeclaration(TypeDeclaration):
    def __init__(self, kwargs={}):
        super(ClassOrInterfaceDeclaration, self).__init__(kwargs)

        # boolean interface_;
        self._interface = kwargs.get('interface_', False)

        # List<TypeParameters>
        typeParameters = kwargs.get(u'typeParameters', [])
        self._typeParameters = map(lambda x: TypeParameter(x) if u'@t' in x else [],
                                  typeParameters.get(u'@e', [])) if typeParameters else []

        # Can contain more than one item if this is an interface
        # List<ClassOrInterfaceType>
        self._extendsList = []
        if kwargs.get(u'extendsList'):
            self._add_supers(kwargs.get(u'extendsList', {}).get(u'@e', []), '_extendsList')
        elif self.name != u'Object':
            self._extendsList = [ClassOrInterfaceType({u'@t':u'ClassOrInterfaceType', u'name':u'Object'})]

        # List<ClassOrInterfaceType>
        self._implementsList = []
        if kwargs.get(u'implementsList'):
            self._add_supers(kwargs.get(u'implementsList', {}).get(u'@e', []), '_implementsList')
        self._subClasses = kwargs.get(u'subClasses', [])

        self._axiom = False
        if self.annotations:
            # self._axiom = any(map(lambda a: str(a) == 'axiomClass', self.annotations))
            self._axiom = any(map(lambda a: str(a) == 'rewriteClass', self.annotations))

        self.add_as_parent(self.typeParameters+self.extendsList+self.implementsList+self.subClasses)

    def _add_supers(self, supers, lst_name):
        locs = _import()

        lst = vars(self)[lst_name]
        for i in supers:
            s = i.get(u'@i')
            if s and s in self.GSYMTAB: lst.append(self.GSYMTAB[s])
            else: lst.append(locs[i.get(u'@t', {})](i))

    def supers(self):
        lst = []
        def get_sups(n):
            sups = []
            # COIT's don't have extends or implements lists
            if isinstance(n, (ClassOrInterfaceType, ImportDeclaration)): return
            for e in n.extendsList: # add items from extendsList to solution
                if e.name == u'Object': continue # ignore Object
                sc = n.symtab.get(e.name)
                if sc:
                    if isinstance(sc, ClassOrInterfaceType):
                        pass
                        # logging.warning('class {} extends unknown type {}'.format(n.name, e.name))
                    else: sups.append(sc)
                else:
                    print 'ERROR: class {} not in symbol table of {}'.format(e.name, n.name) # library?
                    return
            for i in n.implementsList:
                ic = n.symtab.get(i.name)
                if ic:
                    if isinstance(ic, ClassOrInterfaceType):
                        pass
                        # logging.warning('class {} implements type (no class def) {}'.format(str(self), i.name))
                    else: sups.append(ic)
                else:
                    print 'ERROR: class {} not in symbol table of {}'.format(e.name, n.name) # library?
                    continue
            lst.extend(sups)
            map(get_sups, sups)
        get_sups(self)
        return lst

    @property
    def interface(self): return self._interface
    @interface.setter
    def interface(self, v): self._interface = v

    @property
    def typeParameters(self): return self._typeParameters
    @typeParameters.setter
    def typeParameters(self, v): self._typeParameters = v

    @property
    def extendsList(self): return self._extendsList
    @extendsList.setter
    def extendsList(self, v): self._extendsList = v

    @property
    def implementsList(self): return self._implementsList
    @implementsList.setter
    def implementsList(self, v): self._implementsList = v

    @property
    def subClasses(self): return self._subClasses
    @subClasses.setter
    def subClasses(self, v): self._subClasses = v

    @property
    def fullname(self):
        return '_'.join(map(lambda c: c.name, self.enclosing_types()) + [self.name])
    @fullname.setter
    def fullname(self, v): self._fullname = v

    @property
    def typee(self): return ClassOrInterfaceType({u'name':self.name})
    @typee.setter
    def typee(self, v): self._typee = v

    @property
    def name(self): return self._name
    @name.setter
    def name(self, v): self._name = v

    @property
    def axiom(self): return self._axiom
    @axiom.setter
    def axiom(self, v): self._axiom = v

    def isinner(self): return type(self.parentNode) == ClassOrInterfaceDeclaration
    def enclosing_types(self):
        def up(n):
            return up(n.parentNode) + [n.parentNode] if type(n.parentNode) == ClassOrInterfaceDeclaration else []
        return [c for c in up(self) if c]

    def __str__(self):
        return self.sanitize_ty(self.fullname) if self.isinner() else self.sanitize_ty(self.name)
