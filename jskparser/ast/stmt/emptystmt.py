#!/usr/bin/env python

from .statement import Statement

class EmptyStmt(Statement):
    def __init__(self, kwargs={}):
        super(EmptyStmt, self).__init__(kwargs)
