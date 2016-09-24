#! /usr/bin/env python
import sys

from parser.parser import parse
import encoder

import os
pwd = os.path.dirname(__file__)

def match(tmpl, api):
  tmp_ast = parse(tmpl)
  # api_ast = parse(api)
  demo_name = encoder.main_cls(tmp_ast).name
  print demo_name

  # TODO: rewrite holes -- ignoring for now
  
  # encoder.encode(tmp_ast)

  return 0

if __name__ == "__main__":
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
    help="print p_out messages or in/out sets")

  (OPT, argv) = parser.parse_args()
  
  if not OPT.tmpl: parser.error("incorrect arguments: missing template(s)")
  if len(argv) < 1: parser.error("incorrect number of arguments: missing APIs")

  sys.exit(match(OPT.tmpl, argv))
