import os
import unittest

import java_sk.main
import java_sk.util
from . import TestCommon

pwd = os.path.dirname(__file__)
benchmarks = os.path.join(pwd, "benchmarks")

root_dir = os.path.join(pwd, "..")
model_dir = os.path.join(root_dir, "model")

class TestJava(TestCommon):

  def __test(self, fs, using_model=False):
    append_b = lambda f: os.path.join(benchmarks, f)
    _fs = map(append_b, fs)
    if using_model:
      _fs.extend(java_sk.util.get_files_from_path(model_dir, "java"))
    ret = java_sk.main.main(_fs)
    self.assertEqual(ret, 0)

  def test_java_201(self):
    self.__test(["t201-override.java"])

  def test_java_202(self):
    self.__test(["t202-interfaces.java"])

  def test_java_203(self):
    self.__test(["t203-instances.java"])

  def test_java_204(self):
    self.__test(["t204-inner-classes.java"])

  def test_java_205(self):
    self.__test(["t205-const-interface.java"])

  def test_java_206(self):
    self.__test(["t206-anonymous.java"])

  def test_java_207(self):
    self.__test(["t207-super.java"])

  def test_java_208(self):
    self.__test(["t208-string.java"], True)

  def test_java_209(self):
    self.__test(["t209-list.java"], True)

  def test_java_210(self):
    self.__test(["t210-map.java"], True)

  def test_java_211(self):
    self.__test(["t211-stack.java"], True)

  def test_java_212(self):
    self.__test(["t212-queue.java"], True)

  def test_java_213(self):
    self.__test(["t213-overload.java"])

  def test_java_214(self):
    self.__test(["t214-instanceof.java"], True)

  def test_java_215(self):
    self.__test(["t215-optional-exp.java"])

  def test_java_216(self):
    self.__test(["t216-iterator.java"], True)

if __name__ == '__main__':
  unittest.main()

