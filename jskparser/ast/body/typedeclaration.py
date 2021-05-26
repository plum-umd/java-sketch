#!/usr/bin/env python

from . import _import
from .. import Modifiers

from bodydeclaration import BodyDeclaration

class TypeDeclaration(BodyDeclaration):
    def __init__(self, kwargs={}):
        locs = _import()
        super(TypeDeclaration, self).__init__(kwargs)
    
        # int modifiers
        self._modifiers = kwargs.get(u'modifiers', 0)
    
        # List<BodyDeclaration>
        self._members = []
        self._members.extend(map(lambda x: locs[x[u'@t']](x),
                            kwargs.get(u'members', {}).get(u'@e', [])))
    
        self.add_as_parent(self.members)
    
    @property
    def members(self): return self._members
    @members.setter
    def members(self, v): self._members = v
    def add_member(self, v):
        self.members.append(v)
        self.childrenNodes.append(v)
    def prepend_member(self, v):
        self.members.insert(0, v)
        self.childrenNodes.insert(0, v)
  
    @property
    def modifiers(self): return self._modifiers
    @modifiers.setter
    def modifiers(self, v): self._modifiers = v
  
    @staticmethod
    def isPublic(mod):    return (mod.modifiers & Modifiers['PB']) != 0
    @staticmethod
    def isPrivate(mod):   return (mod.modifiers & Modifiers['PR']) != 0
    @staticmethod
    def isProtected(mod): return (mod.modifiers & Modifiers['PRO']) != 0
    @staticmethod
    def isAbstract(mod):  return (mod.modifiers & Modifiers['AB']) != 0
    @staticmethod
    def isStatic(mod):    return (mod.modifiers & Modifiers['ST']) != 0
    @staticmethod
    def isFinal(mod):     return (mod.modifiers & Modifiers['FN']) != 0
    @staticmethod
    def isOptional(mod):  return (mod.modifiers & Modifiers['OP']) != 0
    @staticmethod
    def isHarness(mod):   return (mod.modifiers & Modifiers['HN']) != 0
    @staticmethod
    def isGenerator(mod): return (mod.modifiers & Modifiers['GN']) != 0
    @staticmethod
    def isADT(mod):       return (mod.modifiers & Modifiers['AT']) != 0
