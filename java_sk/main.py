#! /usr/bin/env python
import os
import sys
import logging
import logging.config

import sketch
import util
from encoder import Encoder

from jskparser.jskparser import parse
import rewrite, decode

pwd = os.path.dirname(__file__)
root_dir = os.path.join(pwd, "..")
res_dir = os.path.join(root_dir, "result")
log_lvls = {'0':logging.NOTSET, '10':logging.DEBUG, '20':logging.INFO, '30':logging.WARNING,
            '40':logging.ERROR, '50':logging.CRITICAL}

def translate(**kwargs):
    ## logging configuration
    log_lvl = log_lvls.get(kwargs.get('log_lvl', '10'))
    logging.config.fileConfig(os.path.join(pwd, "logging.conf"))
    logging.getLogger().setLevel(log_lvl)
    
    prg = kwargs.get('prg', None)
    out_dir = kwargs.get('out_dir', res_dir)
    sk = kwargs.get('sketch', True)
    fs = kwargs.get('fs', False)
    cgen = kwargs.get('custom_gen', False)
    cntr = kwargs.get('cntr', False)
    skv = kwargs.get('skv', 0)
    lib = kwargs.get('lib', True)
    inline = kwargs.get('inline', None)
    unroll = kwargs.get('unroll', None)
    parallel = kwargs.get('parallel', None)
    jgen = kwargs.get('jgen', False)
    cgen = True if jgen else cgen
    
    codegen_jar = os.path.join(root_dir, "codegen", "lib", "codegen.jar")
    
    logging.info('parsing {}'.format(prg))
    prg_ast = parse(prg,lib=lib)
    if jgen:
        logging.info('rewriting {}'.format(prg))
        rewrite.visit(prg_ast)
    util.add_object(prg_ast)
 
    encoder = Encoder(prg_ast, out_dir, fs)
    logging.info('encoding to Sketch')
    encoder.to_sk()
    
    # Sketch options
    opts = kwargs.get('opts', [])

    # Sketch inlining and unrolling
    if inline: opts.extend(['--bnd-inline-amnt', inline])
    if unroll: opts.extend(['--bnd-unroll-amnt', unroll])
    if parallel: opts.append("--slv-parallel")

    # print counter examples
    if cntr: opts.extend(['-V3', '--debug-cex'])
    if skv != 0: opts.extend(['-V{}'.format(skv)])

    # place to keep sketch's temporary files
    opts.extend(["--fe-tempdir", out_dir])
    opts.append("--fe-keep-tmp")
 
    # custom codegen
    if cgen: opts.extend(["--fe-custom-codegen", codegen_jar])

    # run Sketch
    output_path = os.path.join(out_dir, "output", "{}.txt".format(encoder.demo_name))
    if sk:
        if os.path.exists(output_path): os.remove(output_path)
        sketch.set_default_option(opts)
 
        logging.info('sk_dir: {}, output_path: {}'.format(encoder.sk_dir, output_path))
        _, r = sketch.run(encoder.sk_dir, output_path)
        
        if jgen:
            java_output_dir = os.path.join(out_dir, "java")

            # Due to Encoder changing the AST, we have to re-parse here
            # TODO: Find another way to preserve the AST
            prg_ast = parse(prg,lib=lib)
            rewrite.visit(prg_ast)

            decode.to_java(java_output_dir, prg_ast, output_path)
            
        # if sketch fails, halt the process here
        if not r: return 1
    elif not prg:
        jskparser.error("need to pass in some file")
 
    return 0
       
def main(prg, log_lvl='20'):
    return translate(prg=prg, log_lvl=log_lvl)
  
if __name__ == "__main__":
    # print 'booleanValue:'
    # descriptors = util.get_mtd_types('java/lang/Byte', 'parseByte', 2)
    # print
    # descriptors = util.get_mtd_types('java/lang/Byte', 'compare', 2)
    # exit()
    if len(sys.argv) < 1:
        sys.exit("incorrect number of arguments")
  
    from optparse import OptionParser
    jskparser = OptionParser(usage="%prog [options]* [-t tmp_path]* (api_path)")
  
    jskparser.add_option("-t", "--template",
                         action="append", dest="tmpl", default=[],
                         help="template folder")
    jskparser.add_option("-l", "--log_lvl",
                         action="store", dest="log_lvl", default='10',
                         help="level of logging")
    jskparser.add_option("-v", "--verbose",
                         action="store_true", dest="verbose", default=False,
                         help="print intermediate messages verbosely")
    jskparser.add_option("-m", "--model",
                         action="store_true", dest="model", default=False,
                         help="use models of Java libraries")
    jskparser.add_option("-o", "--out_dir",
                         dest="out_dir", default=None,
                         help="use models of Java libraries")
    jskparser.add_option("-f", "--file-system",
                         action="store_true", dest="fs", default=False,
                         help="model filesytem with HashMap")
    jskparser.add_option("--no-sketch",
                         action="store_false", dest="sketch", default=True,
                         help="proceed the whole process without running Sketch")
    jskparser.add_option("-c", "--custom-codegen",
                         action="store_true", dest="custom_gen", default=False,
                         help="use custom code generator")
    jskparser.add_option("--cntr",
                         action="store_true", dest="cntr", default=False,
                         help="print out counter examples")
    jskparser.add_option("--skv",
                         action="store", dest="skv", default=0,
                         help="set verbosity level for Sketch")
    jskparser.add_option("--no-lib",
                         action="store_false", dest="lib", default=True,
                         help="compile without linking default Java libraries")
    jskparser.add_option("--inline",
                         action="store", dest="inline", default=None,
                         help="change inlining amount for Sketch")
    jskparser.add_option("--unroll",
                         action="store", dest="unroll", default=None,
                         help="change unrolling amount for Sketch")
    jskparser.add_option("--parallel",
                         action="store_true", dest="parallel", default=None,
                         help="run Sketch in parallel mode")
    jskparser.add_option("--java_codegen",
                         action="store_true", dest="jgen", default=False,
                         help="Enable rewrite-based Java code generation")
    (OPT, argv) = jskparser.parse_args()
    OPT.prg = argv
  
    sys.exit(translate(**vars(OPT)))
