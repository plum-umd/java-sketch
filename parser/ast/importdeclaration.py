#!/usr/bin/env python

from node import Node

from . import _import

from .type.classorinterfacetype import ClassOrInterfaceType

class ImportDeclaration(Node):
    def __init__(self, kwargs={}):
        super(ImportDeclaration, self).__init__(kwargs)
        
        locs = _import()

        # NameExpr name;
        name = kwargs.get(u'name', {})
        self._name = locs[name[u'@t']](name) if name else None

        # boolean static_;
        self._static = kwargs.get(u'static_', False)

        # boolean asterisk;
        self._asterisk = kwargs.get(u'asterisk', False)

        # boolean isEmptyImportDeclaration;
        self._isEmptyDeclaration = kwargs.get(u'isEmptyImportDeclarationasterisk', False)

        # boolean implicit;
        self._implicit = kwargs.get(u'implicit', False)

        # list[ClassOrInterfaceDeclaration]
        self._subClasses = kwargs.get(u'subClasses', [])


    @property
    def static(self): return self._static
    @static.setter
    def static(self, v): self._static = v
  
    @property
    def asterisk(self): return self._asterisk
    @asterisk.setter
    def asterisk(self, v): self._asterisk = v
  
    @property
    def isEmptyDeclaration(self): return self._isEmptyDeclaration
    @isEmptyDeclaration.setter
    def isEmptyDeclaration(self, v): self._isEmptyDeclaration = v
  
    @property
    def implicit(self): return self._implicit
    @implicit.setter
    def implicit(self, v): self._implicit = v

    @property
    def typee(self):
        return ClassOrInterfaceType({u'@t':u'ClassOrInterfaceType',
                                     u'name':unicode(str(self).split('.')[-1]),})
    @typee.setter
    def typee(self, v): self._type = v

    @property
    def subClasses(self): return self._subClasses
    @subClasses.setter
    def subClasses(self, v): self._subClasses = v

    def cname(self): return str(self.typee)

    def __str__(self): return str(self.name)
