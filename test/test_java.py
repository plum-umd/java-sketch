import os
import unittest

import java_sk.main
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

class TestJava(TestCommon):

  def __test(self, fs):
    append_b = lambda f: os.path.join(benchmarks, f)
    _fs = map(append_b, fs)
    ret = java_sk.main.main(_fs)
    self.assertEqual(ret, 0)

  def test_java_201(self):
    self.__test(["t201-override.java"])

  def test_java_202(self):
    self.__test(["t202-interfaces.java"])


if __name__ == '__main__':
  unittest.main()

