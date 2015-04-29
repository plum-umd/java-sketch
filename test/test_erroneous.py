import os

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

  def test_unsat(self):
    f = os.path.join(benchmarks, "t003-unsat.java")
    ret = java_sk.main.main([f])
    self.assertNotEqual(ret, 0)


if __name__ == '__main__':
  unittest.main()

