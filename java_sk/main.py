#! /usr/bin/env python
import sys
import logging
import logging.config

from ast.utils import utils
from parser.parser import parse
from encoder import Encoder
import sketch

import util
import os

pwd = os.path.dirname(__file__)
root_dir = os.path.join(pwd, "..")
res_dir = os.path.join(root_dir, "result")

def translate(**kwargs):
  ## logging configuration
  log_lvl = kwargs.get('log_lvl', logging.DEBUG)
  logging.config.fileConfig(os.path.join(pwd, "logging.conf"))
  logging.getLogger().setLevel(log_lvl)

  prg = kwargs.get('prg', None)
  out = kwargs.get('out_dir')
  sk = kwargs.get('sketch')
  out_dir = out if out else res_dir
  sk_dir = ''
  codegen_jar = os.path.join(root_dir, "codegen", "lib", "codegen.jar")
  
  logging.info('parsing {}'.format(prg))
  prg_ast = parse(prg)
  util.add_object(prg_ast)
  utils.build_subs(prg_ast)
  encoder = Encoder(prg_ast)
  demo_name = encoder.main_cls().name
  sk_dir = os.path.join(out_dir, '_'.join(["sk", demo_name]))
  encoder.sk_dir = sk_dir
  logging.info('encoding to Sketch')
  encoder.to_sk()

  # Sketch options
  opts = []
  # place to keep sketch's temporary files
  opts.extend(["--fe-tempdir", out_dir])
  opts.append("--fe-keep-tmp")

  # custom codegen
  opts.extend(["--fe-custom-codegen", codegen_jar])

  #run Sketch
  output_path = os.path.join(out_dir, "output", "{}.txt".format(demo_name))
  if sk:
    if os.path.exists(output_path): os.remove(output_path)
    sketch.set_default_option(opts)

    logging.info('sk_dir: {}, output_path: {}'.format(sk_dir, output_path))
    _, r = sketch.run(sk_dir, output_path)

    # if sketch fails, halt the process here
    if not r: return 1

  elif not prg:
    parser.error("need to pass in some file")
  # TODO: rewrite holes -- ignoring for now

  return 0

if __name__ == "__main__":
  if len(sys.argv) < 1:
    sys.exit("incorrect number of arguments")

  from optparse import OptionParser
  parser = OptionParser(usage="%prog [options]* [-t tmp_path]* (api_path)")

  parser.add_option("-t", "--template",
    action="append", dest="tmpl", default=[],
    help="template folder")
  parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose", default=False,
    help="print intermediate messages verbosely")
  parser.add_option("-m", "--model",
    action="store_true", dest="model", default=False,
    help="use models of Java libraries")
  parser.add_option("-o", "--out_dir",
    dest="out_dir", default=None,
    help="use models of Java libraries")
  parser.add_option("--no-sketch",
    action="store_false", dest="sketch", default=True,
    help="proceed the whole process without running Sketch")

  (OPT, argv) = parser.parse_args()
  OPT.prg = argv

  if OPT.tmpl: sys.exit(translate(**vars(OPT)))
  sys.exit(translate(**vars(OPT)))
