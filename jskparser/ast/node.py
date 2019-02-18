#!/usr/bin/env python
from __future__ import absolute_import
try: unicode
except: unicode = u"".__class__
import json

from . import _import

from copy import copy

class Node(object):
    GSYMTAB = {}
    def __init__(self, kwargs={}):
        locs = _import()
        if kwargs.get(u'GSYMTAB'): self.GSYMTAB.clear()
        self._locs = _import()
        self._symtab = {}

        self._beginLine = kwargs.get(u'beginLine', 1)
        self._beginColumn = kwargs.get(u'beginColumn', 1)
        self._endLine = kwargs.get(u'endLine', 1)
        self._endColumn = kwargs.get(u'endColumn', 1)

        self._type = None

        # name can be either a unicode object or a NameNode. We don't use NameNode.
        self._name = kwargs.get(u'name')
        if self._name and not isinstance(self._name, unicode) and not isinstance(self._name, str):
            self._name = kwargs.get(u'name', {}).get(u'name')

        # List<Node>
        childrenNodes = kwargs.get(u'childrenNodes')
        self._childrenNodes = []
        if childrenNodes and u'@e' in childrenNodes:
            for c in childrenNodes.get(u'@e'):
                if u'@t' in c: self._childrenNodes.append(locs[c[u'@t']](c))

        # Node
        pNode = kwargs.get(u'parentNode')
        self._parentNode = self._add_parent(pNode) if pNode else None
        if self._parentNode:
            self._parentNode.childrenNodes.append(self)
        self._ati = kwargs.get(u'@i')
        if self.ati:
            # print 'ADDING: {0} : {1}'.format(self._ati, self)
            self._add_symbol(self._ati, self)
        self._atr = self._parentNode._ati if self._parentNode else None
        self._at = kwargs.get(u'@t', None)

        # Comment comment
        c = kwargs.get(u'comment', {})
        if c: self._comment = locs[c[u'@t']](c) if u'@t' in c else {}
        else: self._comment = {}
        
        # List<Comment> orphanComments
        orphanComments = kwargs.get(u'orphanComments', [])
        self._orphanComments = [locs[x[u'@t']](x) if u'@t' in x else [] for x in
                                   orphanComments.get(u'@e', [])] if orphanComments else []
        # JavadocComment javadocComment;
        jdc = kwargs.get(u'javadoccomment', {})
        self._javadocComment = locs[u'JavadocComment'](jdc) if jdc else {}

        # This attribute can store additional information from semantic analysis.
        # TODO: I don't know what this means, but it might be helpful.
        # Object data
        self._data = kwargs.get('data', {})

        # for dataflow analysis
        self._lbl = (self._name, self._ati)
        self._in_set = set([])
        self._out_set = set([])
        self._inputs = []

        self._outputs = []

    @property
    def beginLine(self): return self._beginLine
    @beginLine.setter
    def beginLine(self, v): self._beginLine = v

    @property
    def beginColumn(self): return self._beginColumn
    @beginColumn.setter
    def beginColumn(self, v): self._beginColumn = v
    
    @property
    def endLine(self): return self._endLine
    @endLine.setter
    def endLine(self, v): self._endLine = v

    @property
    def endColumn(self): return self._endColumn
    @endColumn.setter
    def endColumn(self, v): self._endColumn = v
    
    @property
    def parentNode(self): return self._parentNode
    @parentNode.setter
    def parentNode(self, v): self._parentNode = v
    
    @property
    def childrenNodes(self): return self._childrenNodes
    @childrenNodes.setter
    def childrenNodes(self, v): self._childrenNodes = v
    
    @property
    def orphanComments(self): return self._orphanComments
    @orphanComments.setter
    def orphanComments(self, v): self._orphanComments = v
    
    @property
    def data(self): return self._data
    @data.setter
    def data(self, v): self._data = v
    
    @property
    def comment(self): return self._comment
    @comment.setter
    def comment(self, v): self._comment = v
    
    @property
    def name(self): return self._name
    @name.setter
    def name(self, v): self._name = v

    @property
    def ati(self): return self._ati
    @ati.setter
    def ati(self, v): self._ati = v

    @property
    def atr(self): return self._atr
    @atr.setter
    def atr(self, v): self._atr = v

    @property
    def at(self): return self._at
    @at.setter
    def at(self, v): self._at = v

    @property
    def comment(self): return self._comment
    @comment.setter
    def comment(self, v): self._comment = v
    
    @property
    def orphanComment(self): return self._orphanComment
    @orphanComment.setter
    def orphanComment(self, v): self._orphanComment = v
    
    @property
    def javadoc(self): return self._javadocComment
    @javadoc.setter
    def javadoc(self, v): self._javadocComment = v
    
    @property
    def data(self): return self._data
    @data.setter
    def data(self, v): self._data = v
    
    @property
    def in_set(self): return self._in_set
    @in_set.setter
    def in_set(self, v): self._in_set = v

    @property
    def out_set(self): return self._out_set
    @out_set.setter
    def out_set(self, v): self._out_set = v

    @property
    def lbl(self): return (self._name, self.ati)
    @lbl.setter
    def lbl(self, v): self._lbl = v

    @property
    def inputs(self): return self._inputs
    @inputs.setter
    def inputs(self, v): self._inputs = v

    @property
    def outputs(self): return self._outputs
    @outputs.setter
    def outputs(self, v): self._outputs = v

    @property
    def symtab(self): return self._symtab
    @symtab.setter
    def symtab(self, v): self._symtab = v

    @property
    def typee(self):
        if hasattr(self, '_type'): return self._type
        else: return self
    @typee.setter
    def typee(self, v): self._type = v

    def to_json(self, d): return json.dumps(d)

    def dct(self, clean=True):
        def to_dct(d):
            dct = {}
            for k,v in d.items():
                if k == '_parentNode': continue
                if k == '_atr': k = '@r'
                elif k == '_ati': k = '@i'
                elif k == '_at': k = '@t'
                k = k.replace('_','')
                new_v = v
                if isinstance(v, Node):
                    new_v = to_dct(vars(v))
                dct.update({k:new_v})
            if clean:
                if u'parentNode' in d: del d[u'parentNode']
                if u'@i' in d: del d[u'@i']
            return dct

        return to_dct(vars(self))

    def _add_parent(self, p):
        if p.get(u'@r') in self.GSYMTAB:
            return self.GSYMTAB[p[u'@r']]
        return self._locs[p[u'@t']](p) if u'@t' in p else None

    def _add_symbol(self, k, v):
        global GSYMTAB
        if k not in self.GSYMTAB: self.GSYMTAB[k] = v
        # else:
        #     print '!!! K : V = {0} : {1} already in symbol_table !!!' \
        #         .format(k,v)
        #     print '*'*20,'\nSYMBOL TABLE:'

    def add_parent_post(self, p, recurse=True):
        # print 'adding parent:', p, str(p), type(p), self, type(self), self.childrenNodes
        nm = self.sig() if type(self).__name__ == 'MethodDeclaration' else self.name
        tmp_symtab = self.symtab
        special_syms = {}
        for key,val in tmp_symtab.items():
            if str(key)[:8] == "#unboxer":
                special_syms[key] = val
        if nm not in tmp_symtab:
            self.symtab = {nm:self}
        else:
            self.symtab = {nm:self.symtab[nm]}

        if len(special_syms) > 0:
            self.symtab = dict(special_syms.items() + self.symtab.items())
        if nm and nm not in p.symtab: p.symtab.update({nm:self})
        if self not in p.childrenNodes: p.childrenNodes.append(self)
        self.parentNode = p
        if p.symtab and self.symtab:
            self.symtab = dict(p.symtab.items() + self.symtab.items())
        elif p.symtab:
            self.symtab = copy.copy(p.symtab)

        if recurse:
            for c in self.childrenNodes:
                if c: c.add_parent_post(self, True)

    def accept(self, v, **kwargs): v.visit(self, **kwargs)

    def gen(self): return set([])
    def kill(self): return set([])

    def sanitize_ty(self, tname): return tname.replace('$','_').replace('.','_').replace('?', u'Object')

    def get_coid(self):
        from .body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
        if self.parentNode:
            if isinstance(self.parentNode, ClassOrInterfaceDeclaration):
                # print("\t"+str(self.parentNode))
                return self.parentNode            
            else:
                return self.parentNode.get_coid()
        else: return None

    def add_as_parent(self, kids):
        if kids:
            for k in kids:
                if k:
                    if not k.parentNode:
                        k.parentNode = self
                        self.childrenNodes.append(k)

    def axiomParameter(self):
        if type(self).__name__ == 'AxiomParameter': return True
        if self.parentNode: return self.parentNode.axiomParameter()
        else: return False
