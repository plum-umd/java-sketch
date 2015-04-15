import os
import unittest

import java_sk.main

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

class TestErroneous(unittest.TestCase):

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


if __name__ == '__main__':
  unittest.main()

