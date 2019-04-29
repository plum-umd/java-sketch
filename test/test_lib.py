from __future__ import absolute_import
import os
import unittest

import java_sk.main
import java_sk.util
from . import TestCommon

pwd = os.path.dirname(__file__)
tests = os.path.join(pwd, "new_ast")

class TestJava(TestCommon):
    def __test(self, fs):
        _fs = [os.path.join(tests, f) for f in fs + ['../../model/']]
        ret = java_sk.main.main(_fs, '30')
        self.assertEqual(ret, 0)

    def test_ArrayList(self):
        self.__test(["ArrayList_test.java"])

    def test_HashMap(self):
        self.__test(["HashMap_test.java"])

    def test_String(self):
        self.__test(["String_test.java"])

    def test_Integer(self):
        self.__test(["Integer_test.java"])

    # something is wrong here i dont understand
    # def test_Float(self):
    #     self.__test(["Float_test.java", "../../model/"])

if __name__ == '__main__':
  unittest.main()
