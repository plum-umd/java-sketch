#! /usr/bin/env python

from optparse import OptionParser

import os
import subprocess
import sys

def gen(grammar="Java.g", verbose=False):
  pwd = os.path.dirname(__file__)
  root_dir = os.path.join(pwd, "..")
  antlr_jar = os.path.join(root_dir, "lib", "antlr-3.1.3.jar")
  os.environ["CLASSPATH"] = antlr_jar
  antlr_opt = ["org.antlr.Tool", grammar, "-o", pwd]
  if verbose: antlr_opt.extend(["-verbose", "-report"])
  return subprocess.call(["java"] + antlr_opt)

if __name__ == "__main__":
  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option("-g", "--grammar",
    action="store", dest="grammar", default="Java.g",
    help="grammar description file")
  parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose", default=False,
    help="print intermediate messages verbosely")

  (opt, argv) = parser.parse_args()

  sys.exit(gen(opt.grammar, opt.verbose))

