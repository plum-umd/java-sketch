#!/usr/bin/env python

from .stringliteralexpr import StringLiteralExpr

class LongLiteralExpr(StringLiteralExpr):
    def __init__(self, kwargs={}):
        super(LongLiteralExpr, self).__init__(kwargs)

        # private static final String UNSIGNED_MIN_VALUE = "9223372036854775808";
        self._UNSIGNED_MIN_VALUE = "9223372036854775808"

        # protected static final String MIN_VALUE = "-" + UNSIGNED_MIN_VALUE + "L";
        self._MIN_VALUE = "-" + self._UNSIGNED_MIN_VALUE + "L"

        self.add_as_parent([self.typee])
    
    @property
    def UNSIGNED_MIN_VALUE(self): return self._UNSIGNED_MIN_VALUE
    @UNSIGNED_MIN_VALUE.setter
    def UNSIGNED_MIN_VALUE(self, v): self._UNSIGNED_MIN_VALUE = v
    
    @property
    def MIN_VALUE(self):return self._MIN_VALUE
    @MIN_VALUE.setter
    def MIN_VALUE(self, v): pass
