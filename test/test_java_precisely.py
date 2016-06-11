import os
import unittest

import java_sk.main
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")
jp = os.path.join(benchmarks, "java-precisely")

class TestMini(TestCommon):

  def __test(self, fs):
    append_b = lambda f: os.path.join(jp, f)
    _fs = map(append_b, fs)
    ret = java_sk.main.main(_fs)
    self.assertEqual(ret, 0)

  def test_mini_101(self):
    self.__test(["Example1.java"])

  def test_mini_102(self):
    self.__test(["Example2.java"])

  def test_mini_103(self):
    self.__test(["Example3.java"])

  def test_mini_104(self):
    self.__test(["Example4.java"])

if __name__ == '__main__':
  unittest.main()

