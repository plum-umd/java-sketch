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
        ret = java_sk.main.main(_fs, '30')
        self.assertEqual(ret, 0)

    def test_ArrayList(self):
        self.__test(["ArrayList_test.java", "../../model"])

    def test_HashMap(self):
        self.__test(["HashMap_test.java", "../../model/"])

    def test_String(self):
        self.__test(["String_test.java", "../../model/"])

    def test_Integer(self):
        self.__test(["Integer_test.java", "../../model/"])

    # something is wrong here i dont understand
    # def test_Float(self):
    #     self.__test(["Float_test.java", "../../model/"])

if __name__ == '__main__':
  unittest.main()
