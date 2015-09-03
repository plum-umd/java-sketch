#! /usr/bin/env python

import logging
import logging.config
import os
import sys

from lib.typecheck import *

import util
from meta.program import Program
import rewrite
import encoder
import sketch
import decode

pwd = os.path.dirname(__file__)
root_dir = os.path.join(pwd, "..")
res_dir = os.path.join(root_dir, "result")

conf = {
  "encoding": True,
  "sketch": True,
  "timeout": None,
  "randassign": False,
  "randdegree": None,
  "parallel": False,
  "p_cpus": None,
  "ntimes": None,
  "verbose": False
}

def configure(opt):
  conf["encoding"] = opt.encoding
  conf["sketch"] = opt.sketch
  conf["timeout"] = opt.timeout
  conf["randassign"] = opt.randassign
  conf["randdegree"] = opt.randdegree
  conf["parallel"] = opt.parallel
  conf["p_cpus"] = opt.p_cpus
  conf["ntimes"] = opt.ntimes
  conf["verbose"] = opt.verbose


@takes(list_of(str), optional(str), optional(str))
@returns(int)
def main(jsk_paths, out_dir=res_dir, log_lv=logging.DEBUG):
  ## check custom codegen was built
  codegen_jar = os.path.join(root_dir, "codegen", "lib", "codegen.jar")
  if not os.path.isfile(codegen_jar):
    raise Exception("can't find " + codegen_jar)

  ## logging configuration
  logging.config.fileConfig(os.path.join(pwd, "logging.conf"))
  logging.getLogger().setLevel(log_lv)

  ast = util.toAST(jsk_paths)
  pgr = Program(ast)
  main_cls = pgr.main_cls
  demo_name = str(main_cls.name)

  ## rewrite field/method holes
  rewrite.visit(pgr)

  ## encode the program into sketch files
  sk_dir = os.path.join(out_dir, '_'.join(["sk", demo_name]))
  if conf["encoding"]:
    encoder.to_sk(pgr, sk_dir)
  else: # not encoding
    logging.info("pass the encoding phase; rather use previous files")

  opts = [] ## sketch options
  if conf["verbose"]:
    opts.extend(["-V", "10"])
  if conf["timeout"]:
    opts.extend(["--fe-timeout", str(conf["timeout"])])
    opts.extend(["--slv-timeout", str(conf["timeout"])])
  # place to keep sketch's temporary files
  opts.extend(["--fe-tempdir", out_dir])
  opts.append("--fe-keep-tmp")
  # custom codegen
  opts.extend(["--fe-custom-codegen", codegen_jar])

  ## run Sketch
  output_path = os.path.join(out_dir, "output", "{}.txt".format(demo_name))
  if conf["sketch"]:
    if os.path.exists(output_path): os.remove(output_path)

    if conf["randassign"] or conf["parallel"]:
      opts.append("--slv-randassign")
      opts.extend(["--bnd-dag-size", "16000000"]) # 16M ~> 8G memory

    sketch.set_default_option(opts)

    if conf["parallel"]:
      ## Python implementation as a CEGIS (sketch-backend) wrapper
      #_, r = sketch.be_p_run(sk_dir, output_path)
      # Java implementation inside sketch-frontend
      opts.append("--slv-parallel")
      if conf["p_cpus"]:
        opts.extend(["--slv-p-cpus", str(conf["p_cpus"])])
      if conf["ntimes"]:
        opts.extend(["--slv-ntimes", str(conf["ntimes"])])
      if conf["randdegree"]: # assume FIXED strategy
        opts.extend(["--slv-randdegree", str(conf["randdegree"])])
      else: # adaptive concretization
        opts.extend(["--slv-strategy", "WILCOXON"])
      _, r = sketch.run(sk_dir, output_path)
    else:
      _, r = sketch.run(sk_dir, output_path)
    # if sketch fails, halt the process here
    if not r: return 1

  else: # not running Sketch
    logging.info("pass sketch; rather read: {}".format(output_path))

  ## generate Java code
  java_dir = os.path.join(out_dir, "java")
  decode.to_java(java_dir, pgr, output_path)
  logging.info("synthesis done")

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
    help="proceed the whole process without running Sketch")
  parser.add_option("--timeout",
    action="store", dest="timeout", default=None, type="int",
    help="Sketch timeout")
  parser.add_option("--randassign",
    action="store_true", dest="randassign", default=False,
    help="run Sketch with the concretization feature (not parallel)")
  parser.add_option("--randdegree",
    action="store", dest="randdegree", default=None, type="int",
    help="use Sketch's concretization feature, along with the given degree")
  parser.add_option("--parallel",
    action="store_true", dest="parallel", default=False,
    help="run Sketch in parallel until it finds a solution")
  parser.add_option("--p_cpus",
    action="store", dest="p_cpus", default=None, type="int",
    help="the number of cores to use for parallel running")
  parser.add_option("--ntimes",
    action="store", dest="ntimes", default=None, type="int",
    help="number of rounds on a single sketch-backend invocation")
  parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose", default=False,
    help="print intermediate messages verbosely")
  parser.add_option("-m", "--model",
    action="store_true", dest="model", default=False,
    help="use models of Java libraries")

  (opt, argv) = parser.parse_args()

  if len(argv) < 1:
    parser.error("incorrect number of arguments")

  configure(opt)

  pgr_files = []
  if opt.model:
    model_dir = os.path.join(root_dir, "model")
    pgr_files.extend(util.get_files_from_path(model_dir, "java"))

  for arg in argv:
    pgr_files.extend(util.get_files_from_path(arg, "java"))

  sys.exit(main(pgr_files, opt.output))

