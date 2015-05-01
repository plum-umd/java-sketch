import os
import unittest

import java_sk.main
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

class TestErroneous(TestCommon):

  def test_no_main(self):
    f = os.path.join(benchmarks, "t001-no-main.java")
    with self.assertRaises(Exception) as cm:
      java_sk.main.main([f])
    msg = str(cm.exception.args)
    self.assertIn("main()", msg)
    self.assertIn("None", msg)

  def test_mains(self):
    f = os.path.join(benchmarks, "t002-mains.java")
    with self.assertRaises(Exception) as cm:
      java_sk.main.main([f])
    msg = str(cm.exception.args)
    self.assertIn("main()", msg)
    self.assertIn("multiple", msg)

  def __test(self, fs):
    append_b = lambda f: os.path.join(benchmarks, f)
    _fs = map(append_b, fs)
    ret = java_sk.main.main(_fs)
    self.assertNotEqual(ret, 0)

  def test_unsat(self):
    self.__test(["t003-unsat.java"])

  def test_no_return(self):
    self.__test(["t004-no-return.java"])


if __name__ == '__main__':
  unittest.main()

