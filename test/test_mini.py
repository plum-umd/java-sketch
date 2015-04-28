import os
import unittest
import subprocess

import java_sk.main

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

root_dir = os.path.join(pwd, "..")
out_dir = os.path.join(root_dir, "result")

class TestErroneous(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cwd = os.getcwd()
    os.chdir(out_dir)
    try:
      subprocess.check_call(["./clean.sh"])
    except subprocess.CalledProcessError:
      pass # result folder might be already clean
    os.chdir(cwd)


  def test_mini_101(self):
    f = os.path.join(benchmarks, "t101-miniTestb290.java")
    ret = java_sk.main.main([f])
    self.assertEqual(ret, 0)


if __name__ == '__main__':
  unittest.main()

