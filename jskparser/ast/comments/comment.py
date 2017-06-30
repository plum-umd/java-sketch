#!/usr/bin/env python

from ..node import Node

from . import _import

class Comment(Node):
    def __init__(self, kwargs={}):
        super(Comment, self).__init__(kwargs)
        locs = _import()
        # String content;
        self._content = kwargs.get(u'content', '')
        # Node commentedNode;
        c = kwargs.get(u'commentedNode') if kwargs.get(u'commentedNode') else {}
        self._commentedNode = locs[c[u'@t']] if u'@t' in c else {}

    @property
    def content(self): return self._content
    @content.setter
    def content(self, v): self._content = v

    @property
    def commentedNode(self): return self._commentedNode
    @commentedNode.setter
    def commentedNode(self, v): self._commentedNode = v
        
