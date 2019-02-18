from __future__ import absolute_import
import os
import re
import sys

import lib.const as C
from lib.enum import enum
from lib.rlock import FLockFileHandler

from . import util

C.log_caller = enum(JAVASK="jsk", PSKETCH="psketch")

def find_demo_name(argv):
  for i, arg in enumerate(argv):
    # main pasket: -p demo_name
    if arg == "-p":
      return (argv[i+1], C.log_caller.JAVASK)

    # psketch: -o 
    if arg == "-o":
      m = re.match(r".*/sk_([^/]*)/.*", argv[i+1])
      if m:
        demo = m.group(1)
        return (demo, C.log_caller.PSKETCH)

  return (None, None)


class JskFileHandler(FLockFileHandler):

  def __init__(self, fileName, mode):
    pwd = os.path.dirname(os.path.realpath(__file__))
    log_dir = os.path.join(pwd, "..", "result", "log")
    demo, whom = find_demo_name(sys.argv)

    f = fileName
    _mode = mode

    if whom:
      suffix = util.get_datetime()
      f = u'.'.join([demo, suffix, "txt"])

    if whom == C.log_caller.PSKETCH:
      _mode = 'a' # append, not overwrite

    path = os.path.join(log_dir, f)
    super(JskFileHandler, self).__init__(path, _mode)

