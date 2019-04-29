#! /usr/bin/env python

from __future__ import absolute_import
try: xrange
except: xrange = range
import multiprocessing
import os
import logging
import logging.config
import shutil
import subprocess
import sys
import time

def find_output_path(argv):
  for i, arg in enumerate(argv):
    if arg == "-o": return argv[i+1]
  return None


def repl_output_path(argv, path):
  _argv = argv[:]
  for i, arg in enumerate(argv):
    if arg == "-o": _argv[i+1] = path
  return _argv


def run(cmd, argv, trial=-1):
  running = "cegis running..."
  if trial >= 0: running = running + " ({})".format(trial+1)

  output_path = find_output_path(argv)
  try:
    logging.info(running)
    subprocess.check_call([cmd] + argv)
    logging.info("cegis done: {}".format(output_path))
    return (output_path, True)
  except subprocess.CalledProcessError:
    logging.error("cegis fail: {}".format(output_path))
    return (output_path, False)


def p_run(cmd, argv):
  logging.debug("{} {}".format(cmd, ' '.join(argv)))
  output_path = find_output_path(argv)

  n_cpu = multiprocessing.cpu_count()
  pool = multiprocessing.Pool(max(1, int(n_cpu * 0.75)))

  def found(cegis_result):
    (fname, r) = cegis_result
    if r: # found, copy that output file
      shutil.copyfile(fname, output_path)
      pool.close()
      pool.terminate() # other running processes will become zombies here

  trials = n_cpu * 32
  results = []
  temps = []
  try:
    for i in xrange(trials):
      _output_path = output_path + str(i)
      temps.append(_output_path)
      _argv = repl_output_path(argv, _output_path)
      r = pool.apply_async(run, (cmd, _argv, i), callback=found)
      results.append(r)
      time.sleep(1)
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


if __name__ == "__main__":
  pwd = os.path.dirname(__file__)
  root_dir = os.path.join(pwd, "..")
  sys.path.append(root_dir) # to load logging conf correctly

  ## logging configuration
  logging.config.fileConfig(os.path.join(pwd, "logging.conf"))
  logging.getLogger().setLevel(logging.DEBUG)

  sketch_home = os.environ["SKETCH_HOME"]
  if "runtime" in sketch_home: # using tar ball
    sketch_root = os.path.join(sketch_home, "..", "..")
  else: # from source
    sketch_root = os.path.join(sketch_home, "..")
  cegis = os.path.join(sketch_root, "sketch-backend", "src", "SketchSolver", "cegis")

  # double-check that cegis is running with -randassign
  # which could be set via --be:randassign or --slv-randassign
  if "-randassign" in sys.argv:
    _, res = p_run(cegis, sys.argv[1:])
  else:
    _, res = run(cegis, sys.argv[1:])

  if res: sys.exit(0)
  else: sys.exit(1)

