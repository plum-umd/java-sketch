from __future__ import absolute_import
import os
import unittest

import java_sk.main
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

class TestMini(TestCommon):

  def __test(self, fs):
    _fs = [os.path.join(benchmarks, f) for f in fs]
    ret = java_sk.main.main(_fs, '30')
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

  def test_mini_108(self):
    self.__test(["t108-miniTestb459.java"])

  def test_mini_109(self):
    self.__test(["t109-mult2.java"])

  def test_mini_110(self):
    self.__test(["t110-miniTestb156.java"])


if __name__ == '__main__':
  unittest.main()

