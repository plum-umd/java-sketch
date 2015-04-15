#! /usr/bin/env python

import logging
import logging.config
import os
import sys

from meta.program import Program

from lib.typecheck import *

import util

pwd = os.path.dirname(__file__)
root_dir = os.path.join(pwd, "..")
res_dir = os.path.join(root_dir, "result")

conf = {}

def configure(opt):
  conf["encoding"] = opt.encoding
  conf["sketch"] = opt.sketch
  conf["randassign"] = opt.randassign
  conf["randdegree"] = opt.randdegree
  conf["parallel"] = opt.parallel
  conf["p_cpus"] = opt.p_cpus
  conf["verbose"] = opt.verbose


@takes(list_of(str), str, optional(str))
@returns(int)
def main(jsk_paths, out_dir, log_lv=logging.DEBUG):

  ## check custom codegen was built
  codegen_jar = os.path.join(root_dir, "codegen", "lib", "codegen.jar")
  if not os.path.isfile(codegen_jar):
    raise Exception("can't find " + codegen_jar)

  ## logging configuration
  logging.config.fileConfig(os.path.join(pwd, "logging.conf"))
  logging.getLogger().setLevel(log_lv)

  ast = util.toAST(pgr_files)
  pgr = Program(ast)

  return 0


if __name__ == "__main__":
  from optparse import OptionParser
  parser = OptionParser(usage="usage: %prog (input.java | input_folder)+ [options]*")
  parser.add_option("-o", "--output",
    action="store", dest="output", default=res_dir,
    help="output folder")
  parser.add_option("--no-encoding",
    action="store_false", dest="encoding", default=True,
    help="proceed the whole process without the encoding phase")
  parser.add_option("--no-sketch",
    action="store_false", dest="sketch", default=True,
    help="proceed the whole process without running sketch")
  parser.add_option("--randassign",
    action="store_true", dest="randassign", default=False,
    help="run sketch with the concretization feature (not parallel)")
  parser.add_option("--randdegree",
    action="store", dest="randdegree", default=None, type="int",
    help="use sketch's concretization feature, along with the given degree")
  parser.add_option("--parallel",
    action="store_true", dest="parallel", default=False,
    help="run sketch in parallel until it finds a solution")
  parser.add_option("--p_cpus",
    action="store", dest="p_cpus", default=None, type="int",
    help="the number of cores to use for parallel running")
  parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose", default=False,
    help="print intermediate messages verbosely")

  (opt, argv) = parser.parse_args()

  if len(argv) < 1:
    parser.error("incorrect number of arguments")

  configure(opt)

  pgr_files = []
  for arg in argv:
    pgr_files.extend(util.get_files_from_path(arg, "java"))

  sys.exit(main(pgr_files, opt.output))

