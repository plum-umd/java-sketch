import os
import unittest

import java_sk.main
import java_sk.util
from . import TestCommon

pwd = os.path.dirname(__file__)
tests = os.path.join(pwd, "new_ast")

class TestJava(TestCommon):
    def __test(self, fs):
        _fs = map(lambda f: os.path.join(tests, f), fs)
        ret = java_sk.main.translate(prg=_fs)
        self.assertEqual(ret, 0)
        
    def test_Array(self):
        self.__test(["Array.java"])

    def test_BooMoo(self):
        self.__test(["BooMoo.java"])

    def test_Calls(self):
        self.__test(["Calls.java"])

    def test_Construct(self):
        self.__test(["Construct.java"])

    def test_Creation(self):
        self.__test(["Creation.java"])

    def test_Fields(self):
        self.__test(["Fields.java"])
        
    def test_Generators(self):
        self.__test(["Generators.java"])
        
    def test_Hole(self):
        self.__test(["Hole.java"])
        
    def test_Iface(self):
        self.__test(["Iface.java"])
        
    def test_Inners(self):
        self.__test(["Inners.java"])
        
    def test_Static(self):
        self.__test(["Static.java"])
        
    def test_Switch(self):
        self.__test(["Switch.java"])
        
    def test_This(self):
        self.__test(["This.java"])
        
if __name__ == '__main__':
  unittest.main()

