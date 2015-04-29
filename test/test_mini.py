import os

import java_sk.main
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

root_dir = os.path.join(pwd, "..")
out_dir = os.path.join(root_dir, "result")

class TestErroneous(TestCommon):

  def test_mini_101(self):
    f = os.path.join(benchmarks, "t101-miniTestb290.java")
    ret = java_sk.main.main([f])
    self.assertEqual(ret, 0)


if __name__ == '__main__':
  unittest.main()

