#! /usr/bin/env python

from functools import partial
import multiprocessing
import os
import logging
import logging.config
import subprocess
import shutil
import sys
import time

default_opts = []

def set_default_option(opts):
  global default_opts
  default_opts = opts


# single sketch run, as a standalone tool
def run(sk_dir, output_path, trial=-1):
  global default_opts
  _opt = default_opts[:]
  _opt.extend(["--fe-output", os.path.basename(sk_dir)])
  _opt.extend(["--fe-inc", sk_dir])

  sk = os.path.join(sk_dir, "main.sk")

  running = "sketch running..."
  if trial >= 0: running = running + " ({})".format(trial+1)

  res = False 
  with open(output_path, 'a') as f:
    logging.info(running)
    cmd = ["sketch"] + _opt + [sk]
    logging.debug(' '.join(cmd))
    try:
      subprocess.check_call(cmd, stdout=f)
      logging.info("sketch done: {}".format(output_path))
      res = True
    except subprocess.CalledProcessError:
      logging.error("semantic errors due to wrong encoding or UNSATISFIABLE")

  return (output_path, res)


# run sketch as a whole, in parallel, until one trial finds a solution
def p_run(sk_dir, output_path):
  n_cpu = multiprocessing.cpu_count()
  pool = multiprocessing.Pool(max(1, int(n_cpu * 0.75)))

  def found( (fname, r) ):
    if r: # found, copy that output file
      shutil.copyfile(fname, output_path)
      pool.close()
      pool.terminate() # other running processes will become zombies here

  trials = n_cpu * 32
  results = []
  temps = []
  try:
    for i in xrange(trials):
      suffix = util.get_datetime()
      _output_path = u'.'.join([output_path, suffix, "txt"])
      temps.append(_output_path)
      r = pool.apply_async(run, (sk_dir, _output_path, i), callback=found)
      results.append(r)
      time.sleep(6)
    pool.close()
  except KeyboardInterrupt:
    pool.close()
    pool.terminate()
  except AssertionError: # apply_async is called after pool was terminated
    pass
  finally:
    pool.join()

  # clean up temporary files, while merging synthesis result
  res = False
  logging.debug("# of processes: {}".format(len(results)))
  for i, fname in enumerate(temps):
    try:
      _fname, r = results[i].get(1) # very short timeout to kill zombies
      res = res or r
      assert fname == _fname
    except IndexError:
      pass # in case where temps.append happens but the loop finishes just before pool.apply_async
    except multiprocessing.TimeoutError: # zombie case
      pass
    finally:
      if os.path.exists(fname):
        os.remove(fname)
        logging.debug("deleting {}".format(fname))

  return (output_path, res)


# run backend in parallel
def be_p_run(sk_dir, output_path):
  pwd = os.path.dirname(os.path.realpath(__file__))
  cegis = os.path.join(pwd, "psketch.py")

  # custom CEGIS 
  global default_opts
  default_opts.extend(["--fe-cegis-path", cegis])

  return run(sk_dir, output_path)


"""
  $ python -m java_sk.sketch -p demo [--parallel]
  $ ./java_sk/sketch.py -p demo [...]
"""
if __name__ == "__main__":
  from optparse import OptionParser
  usage = "usage: python -m java_sk.sketch [opt]"
  parser = OptionParser(usage=usage)
  parser.add_option("-p", "--pattern", # same as run.py at the top level
    action="store", dest="demo", default=None,
    help="demo name")
  parser.add_option("--timeout",
    action="store", dest="timeout", default=None, type="int",
    help="Sketch timeout")
  parser.add_option("--parallel",
    action="store_true", dest="parallel", default=False,
    help="run sketch in parallel")
  parser.add_option("--p_cpus",
    action="store", dest="p_cpus", default=None, type="int",
    help="the number of cores to use for parallel running")
  parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose", default=False,
    help="print intermediate messages verbosely")

  (opt, argv) = parser.parse_args()

  if not opt.demo:
    parser.error("no demo name given")

  pwd = os.path.dirname(__file__)
  root_dir = os.path.join(pwd, "..")
  sys.path.append(root_dir) # to load logging conf correctly

  ## logging configuration
  logging.config.fileConfig(os.path.join(pwd, "logging.conf"))
  logging.getLogger().setLevel(logging.DEBUG)

  codegen_jar = os.path.join(root_dir, "codegen", "lib", "codegen.jar")

  res_dir = os.path.join(root_dir, "result")

  _opts = [] ## sketch options
  # place to keep sketch's temporary files
  _opts.extend(["--fe-tempdir", res_dir])
  _opts.append("--fe-keep-tmp")

  if opt.verbose: _opts.extend(["-V", "10"])
  if opt.timeout:
    _opts.extend(["--fe-timeout", str(opt.timeout)])
    _opts.extend(["--slv-timeout", str(opt.timeout)])

  if opt.parallel:
    _opts.append("--slv-randassign")
    _opts.extend(["--bnd-dag-size", "16000000"]) # 16M ~> 8G memory
    if opt.p_cpus:
      _opts.extend(["--slv-p-cpus", str(opt.p_cpus)])

  # custom codegen
  _opts.extend(["--fe-custom-codegen", codegen_jar])
  set_default_option(_opts)

  sk_dir = os.path.join(res_dir, "sk_" + opt.demo)
  output_path = os.path.join(res_dir, "output", "{}.txt".format(opt.demo))
  if os.path.exists(output_path): os.remove(output_path)

  if opt.parallel:
    be_p_run(sk_dir, output_path)
  else:
    run(sk_dir, output_path)

  sys.exit(0)

