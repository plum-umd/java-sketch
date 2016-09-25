#! /usr/bin/env python
import sys

from parser.parser import parse
import encoder

import os
pwd = os.path.dirname(__file__)
root_dir = os.path.join(pwd, "..")
res_dir = os.path.join(root_dir, "result")

def match(**kwargs):
  # this will be stuff to use when matching 
  tmpl = kwargs.get('tmpl', None)
  prg = kwargs.get('prg', None)
  out_dir = kwargs.get('out_dir', res_dir)
  if tmpl:
    tmpl_ast = parse(tmpl)
    demo_name = encoder.main_cls(tmpl_ast).name
    print demo_name
  if prg:
    prg_ast = parse(prg)
    demo_name = encoder.main_cls(prg_ast).name
    print demo_name
    sk_dir = os.path.join(out_dir, '_'.join(["sk", demo_name]))
    print sk_dir
    encoder.to_sk(prg_ast, sk_dir)
  elif not tmpl and not prg:
    parser.error("need to pass in some file")
  # TODO: rewrite holes -- ignoring for now
  

  return 0

if __name__ == "__main__":
  if len(argv) < 1:
    parser.error("incorrect number of arguments")


  from optparse import OptionParser
  parser = OptionParser(usage="%prog [options]* [-t tmp_path]* (api_path)")

  # parser.add_option("-o", "--output",
  #   action="store", dest="output", default=jsk_dir,
  #   help="output folder")
  parser.add_option("-t", "--template",
    action="append", dest="tmpl", default=[],
    help="template folder")
  parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose", default=False,
<<<<<<< HEAD
    help="print p_out messages or in/out sets")
=======
    help="print intermediate messages verbosely")
  parser.add_option("-m", "--model",
    action="store_true", dest="model", default=False,
    help="use models of Java libraries")

  (opt, argv) = parser.parse_args()

  configure(opt)

  pgr_files = []
  if opt.model:
    model_dir = os.path.join(root_dir, "model")
    pgr_files.extend(util.get_files_from_path(model_dir, "java"))

  for arg in argv:
    pgr_files.extend(util.get_files_from_path(arg, "java"))

  sys.exit(main(pgr_files, opt.output))
>>>>>>> 19ced4a2213b0317dc2ca270e55f2c5a37366747

  (OPT, argv) = parser.parse_args()
  
  if OPT.tmpl: sys.exit(match(tmpl=OPT.tmpl, prg=argv))
  if len(argv) < 1: parser.error("incorrect number of arguments: missing APIs")
  sys.exit(match(prg=argv))
