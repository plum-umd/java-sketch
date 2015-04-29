import os

import java_sk.main
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

root_dir = os.path.join(pwd, "..")
out_dir = os.path.join(root_dir, "result")

class TestErroneous(TestCommon):

  def __test(self, b):
    f = os.path.join(benchmarks, b)
    ret = java_sk.main.main([f])
    self.assertEqual(ret, 0)

  def test_mini_101(self):
    self.__test("t101-miniTestb290.java")

  def test_mini_102(self):
    self.__test("t102-miniTestb294.java")


if __name__ == '__main__':
  unittest.main()

