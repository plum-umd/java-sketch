import os
import unittest

import java_sk.main

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

class TestErroneous(unittest.TestCase):

  def test_mini_101(self):
    f = os.path.join(benchmarks, "t101-miniTestb290.java")
    ret = java_sk.main.main([f])
    self.assertEqual(ret, 0)


if __name__ == '__main__':
  unittest.main()

