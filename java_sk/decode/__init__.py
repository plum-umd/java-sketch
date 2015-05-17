import os
import logging

from lib.typecheck import *
import lib.const as C

from .. import util
from ..meta.program import Program

from hole_finder import HFinder
from replacer import Replacer

from collection import Collection
from semantic_checker import SemanticChecker


# white-list checking
@takes(unicode, list_of(unicode))
@returns(bool)
def check_pkg(pname, lst):
  return util.exists(lambda pkg: pname.startswith(pkg), lst)


# trimming
@takes(Program)
@returns(nothing)
def trim(pgr):
  pkgs_java = [u"java.lang", u"java.util"]

  for cls in pgr.classes[:]:
    if cls.pkg and check_pkg(cls.pkg, pkgs_java):
      logging.debug("trimming: {}".format(cls.name))
      pgr.classes.remove(cls)


# build folders for the given package name
# e.g., for x.y, generate x and then y under x if not exist
@takes(str, unicode)
@returns(nothing)
def build_pkg_folders(java_dir, pkg):
  p = java_dir
  for elt in pkg.split('.'):
    p = os.path.join(p, elt)
    if not os.path.exists(p):
      os.makedirs(p)


# find appropriate import statements, generally
@takes(str, unicode, list_of(unicode))
@returns(list_of(unicode))
def find_imports(body, pkg, clss):
  def appear(cls): return cls in body
  return [ '.'.join([pkg, cls]) for cls in filter(appear, clss) ]


@takes(str, Program, str, str)
@returns(nothing)
def to_java(java_dir, pgr, output_path):
  ## clean up result directory
  if os.path.isdir(java_dir): util.clean_dir(java_dir)
  else: os.makedirs(java_dir)

  ## find holes
  hfinder = HFinder()
  pgr.accept(hfinder)
  holes = hfinder.holes

  ## replace holes with resolved answers
  replacer = Replacer(output_path, holes)
  pgr.accept(replacer)

  # final semantic checking
  logging.info("semantics checking")
  _visitors = []
  # replace collections of interface types with actual classes, if any
  _visitors.append(Collection())
  _visitors.append(SemanticChecker())
  map(lambda vis: pgr.accept(vis), _visitors)

  ## trimming of the program
  trim(pgr)

  dump(java_dir, pgr, "decoding")


# dump out the given program, which might be
# either an intermediate AST or the final result
@takes(str, Program, optional(str))
@returns(nothing)
def dump(dst_dir, pgr, msg=None):
  def write_imports(imports):
    def write_import(i): return "import {};".format(i)
    return '\n'.join(map(write_import, imports)) + '\n'

  ios = [u"File", u"InputStream", u"FileInputStream", \
      u"InputStreamReader", u"BufferedReader", \
      u"FileNotFoundException", u"IOException"]

  decl_pkgs = set([])
  for cls in pgr.classes:
    if not cls.pkg: continue
    decl_pkgs.add(cls.pkg)

  for cls in pgr.classes:
    ## generate folders according to package hierarchy
    fname = cls.name + ".java"
    if cls.pkg:
      build_pkg_folders(dst_dir, cls.pkg)
      folders = [dst_dir] + cls.pkg.split('.') + [fname]
      java_path = os.path.join(*folders)
    else: java_path = os.path.join(dst_dir, fname)

    ## figure out import statements
    imports = []

    cls_body = str(cls)
    imports.extend(find_imports(cls_body, u"java.util", C.collections))
    imports.extend(find_imports(cls_body, u"java.io", ios))

    for pkg in decl_pkgs:
      if not cls.pkg or cls.pkg != pkg: imports.append(pkg+".*")

    ## generate Java files
    with open(java_path, 'w') as f:
      if cls.pkg: f.write(C.T.PKG + ' ' + cls.pkg + ";\n")
      f.write(write_imports(imports))
      f.write(cls_body)
      if msg: logging.info(" ".join([msg, f.name]))
      else: logging.debug("dumping " + f.name)

