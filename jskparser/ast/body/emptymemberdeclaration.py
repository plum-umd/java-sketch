#!/usr/bin/env python

from .bodydeclaration import BodyDeclaration

class EmptyMemberDeclaration(BodyDeclaration):
    def __init__(self, kwargs={}):
        super(EmptyMemberDeclaration, self).__init__(kwargs)
