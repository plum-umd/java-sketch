import os

import java_sk.main
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

root_dir = os.path.join(pwd, "..")
out_dir = os.path.join(root_dir, "result")

class TestErroneous(TestCommon):

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


if __name__ == '__main__':
  unittest.main()

