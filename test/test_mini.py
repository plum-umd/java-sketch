import os
import unittest

import java_sk.main
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

class TestMini(TestCommon):

  def __test(self, fs):
    append_b = lambda f: os.path.join(benchmarks, f)
    _fs = map(append_b, fs)
    ret = java_sk.main.main(_fs)
    self.assertEqual(ret, 0)

  def test_mini_101(self):
    self.__test(["t101-miniTestb290.java"])

  def test_mini_102(self):
    self.__test(["t102-miniTestb294.java"])

  def test_mini_103(self):
    self.__test(["t103-miniTestb415.java"])

  def test_mini_104(self):
    self.__test(["t104-miniTestb586.java"])

  def test_mini_105(self):
    self.__test(["t105-miniTestb626.java"])

  def test_mini_106(self):
    self.__test(["t106-miniTestb644.java"])

  def test_mini_107(self):
    self.__test(["t107-miniTestb659.java"])


if __name__ == '__main__':
  unittest.main()

