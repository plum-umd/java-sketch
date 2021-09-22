#!/usr/bin/env python

from . import _import

from ..node import Node
from ..expr.nameexpr import NameExpr

class VariableDeclarator(Node):
    def __init__(self, kwargs={}, id_str="", type_obj=None, init_obj=None):
        if kwargs.get(u'id', id_str):
            super(VariableDeclarator, self).__init__(kwargs)
            locs = _import()

            # VariableDeclaratorId
            if id_str:
                self._id = locs[u'VariableDeclaratorId'](name_str=id_str)
            else:
                self._id = locs[u'VariableDeclaratorId'](kwargs.get(u'id'))

            # Type type
            if type_obj:
                self._typ = type_obj
            else:
                typ = kwargs.get(u'type')
                self._typ = locs[typ[u'@t']](typ) if typ else None

            # Expression
            if init_obj:
                self._init = init_obj
            else:
                i = kwargs.get('init')

                self._init = locs[i[u'@t']](i) if i else None
            # if self._init and self.parentNode and not self._typ:
            #     self._init.typee = self.parentNode.typee

            self.add_as_parent([self.idd, self.init])
    
    def to_name_expr(self):
        expr = NameExpr()
        expr.name = self.name
        return expr

    @property
    def idd(self): return self._id
    @idd.setter
    def idd(self, v): self._id = v

    @property
    def name(self): return self._id.name
    @name.setter
    def name(self, v): self._id.name = v

    @property
    def init(self): return self._init
    @init.setter
    def init(self, v): self._init = v

    @property
    def lbl(self): return (self.name, self.ati)
    @lbl.setter
    def lbl(self, v): self._lbl = v

    @property
    def typee(self): return self._typ if self._typ else self.parentNode.typee
    @typee.setter
    def typee(self, v): self._typ = v

    def gen(self): return set([self.lbl]) if self.init else set([])

    def __str__(self): return str(self.idd)
