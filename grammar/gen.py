#! /usr/bin/env python

from optparse import OptionParser

import os
import subprocess
import sys

def gen(grammar="Java.g"):
  pwd = os.path.dirname(__file__)
  root_dir = os.path.join(pwd, "..")
  antlr_jar = os.path.join(root_dir, "lib", "antlr-3.1.3.jar")
  os.environ["CLASSPATH"] = antlr_jar
  antlr_opt = ["org.antlr.Tool", grammar, "-o", pwd]
  return subprocess.call(["java"] + antlr_opt)

if __name__ == "__main__":

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option("-g", "--grammar",
    action="store", dest="grammar", default="Java.g",
    help="grammar description file")

  (opt, argv) = parser.parse_args()

  sys.exit(gen(opt.grammar))

