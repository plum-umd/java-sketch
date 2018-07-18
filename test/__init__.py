import os
import subprocess
import unittest

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

root_dir = os.path.join(pwd, "..")
out_dir = os.path.join(root_dir, "result")

class TestCommon(unittest.TestCase):

  @classmethod
  def clean(cls):
    cwd = os.getcwd()
    os.chdir(out_dir)
    # try:
    #   subprocess.check_call(["./clean.sh"])
    # except subprocess.CalledProcessError:
    #   pass # result folder might be already clean
    os.chdir(cwd)

  def setUp(self):
    TestCommon.clean()

  def tearDown(self):
    TestCommon.clean()

