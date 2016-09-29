#! /usr/bin/env python
import sys

from ast.utils import utils
from parser.parser import parse
from encoder import Encoder

import util

import os
pwd = os.path.dirname(__file__)
root_dir = os.path.join(pwd, "..")
res_dir = os.path.join(root_dir, "result")

def translate(**kwargs):
  # this will be stuff to use when matching 
  tmpl = kwargs.get('tmpl', None)
  prg = kwargs.get('prg', None)
  out_dir = kwargs.get('out_dir', res_dir)
  if tmpl:
    tmpl_ast = parse(tmpl)
    util.add_object(prg)
    # demo_name = encoder.main_cls(tmpl_ast).name
    print demo_name
  if prg:
    prg_ast = parse(prg)
    util.add_object(prg_ast)
    utils.build_subs(prg_ast)
    encoder = Encoder(prg_ast)
    demo_name = encoder.main_cls().name
    print 'demo_name:', demo_name
    encoder.sk_dir = os.path.join(out_dir, '_'.join(["sk", demo_name]))
    encoder.to_sk()
  elif not tmpl and not prg:
    parser.error("need to pass in some file")
  # TODO: rewrite holes -- ignoring for now

  return 0

if __name__ == "__main__":
  if len(sys.argv) < 1:
    sys.exit("incorrect number of arguments")

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
    help="print intermediate messages verbosely")
  parser.add_option("-m", "--model",
    action="store_true", dest="model", default=False,
    help="use models of Java libraries")

  (OPT, argv) = parser.parse_args()
  
  if OPT.tmpl: sys.exit(translate(tmpl=OPT.tmpl, prg=argv))
  sys.exit(translate(prg=argv))
