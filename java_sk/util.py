import datetime
import logging
import operator as op
import os
import re
import shutil
from functools import partial
from itertools import chain, islice, ifilter, ifilterfalse

import antlr3
from antlr3.tree import CommonTree as AST
from grammar.JavaLexer import JavaLexer as Lexer
from grammar.JavaParser import JavaParser as Parser

import lib.glob2 as glob2
from lib.typecheck import *
import lib.const as C

"""
regarding paths and files
"""

# clean all the contents in the designated path, excluding that path
@takes(str)
@returns(nothing)
def clean_dir(path):
  for root, dirs, files in os.walk(path):
    for f in files:
      try: os.unlink(os.path.join(root, f))
      except OSError: pass # maybe .swp file
    for d in dirs:
      shutil.rmtree(os.path.join(root, d))


# get the *sorted* list of file names in the designated path
# template/gui/awt -> [.../AWTEvent.java, .../BorderLayout.java, ...]
@takes(str, str)
@returns(list_of(str))
def get_files_from_path(path, ext):
  if os.path.isfile(path): return [path]
  else: # i.e., folder
    files = glob2.glob(os.path.join(path, "**/*.{}".format(ext)))
    return sorted(files) # to guarantee the order of files read


# base name without extension
# result/button_demo.txt -> button_demo
@takes(str)
@returns(str)
def pure_base(path):
  base = os.path.basename(path)
  return os.path.splitext(base)[0]


"""
regarding Java features
"""

# extract parameterized types
# Map<K, V> -> [K, V]
# List<T> -> [T]
# Map<K, List<T>> -> [K, List<T>]
@takes(unicode, optional(unicode))
@returns(list_of(unicode))
def extract_generics(tname, base=u"\S+"):
  regex = r"^({})<(.+)>$".format(base)
  m = re.match(regex, tname.strip())
  if m: # m.group(1) = collection name
    typs = [m.group(1)] + m.group(2).split(',')
    return map(op.methodcaller("strip"), typs)
  else: return []


# Map<K,V> / List<T> / ... -> [Map, K, V] / [List, T] / ...
@takes(unicode)
@returns(list_of(unicode))
def of_collection(tname):
  for collection in C.collections:
    if collection in tname:
      typs = extract_generics(tname, u'|'.join(C.collections))
      if any(typs): return typs
  return []


# check whether the given type name is kind of Java collections
@takes(unicode)
@returns(bool)
def is_collection(tname):
  return any(of_collection(tname))


# check whether the given type name has bounded type parameter(s)
@takes(unicode)
@returns(bool)
def is_generic(tname):
  return any(extract_generics(tname))


# ArrayAdapter<?> -> [ArrayAdapter, ?]
@takes(unicode)
@returns(list_of(unicode))
def explode_generics(tname):
  if is_generic(tname):
    return extract_generics(tname)
  else: return [tname]


# extrace base type out of array
# e.g., X[] -> X
@takes(unicode)
@returns(optional(unicode))
def componentType(tname):
  if tname.endswith("[]"): return tname[:-2]
  else: return None


# check whether the given type name is kind of array
@takes(unicode)
@returns(bool)
def is_array(tname):
  return '[' in tname and ']' in tname


# check whether the given type name is a possible class name or not
@takes(unicode)
@returns(bool)
def is_class_name(tname):
  return tname[0].isupper()


# sanitize type name
# e.g., Demo$1 -> Demo_1, Outer.Inner -> Outer_Inner
# ArrayAdapter<?> (-> ArrayAdapter_?) -> ArrayAdapter_Object
@takes(unicode)
@returns(unicode)
def sanitize_ty(tname):
  #repl_map = {"$": "_", ".": "_"}
  #repl_dic = dict((re.escape(k), v) for k, v in repl_map.iteritems())
  #pattern = re.compile(" | ".join(repl_dic.keys()))
  #return pattern.sub(lambda m: repl_dic[re.escape(m.group(0))], tname)
  _tname = tname.replace('$','_').replace('.','_')
  if is_generic(_tname):
    _tname = u'_'.join(explode_generics(_tname))
  return _tname.replace('?', C.J.OBJ)


# convert type name to JVM notation
# e.g., x.y.Z -> Lx/y/Z;
@takes(unicode)
@returns(unicode)
def toJVM(tname):
  if is_class_name(tname.split('.')[-1]):
    return u'L' + tname.replace('.','/') + u';'
  elif is_array(tname):
    return u'[' + toJVM(componentType(tname))
  else: return tname


# default value of the given time, depending on framework
_default_values = {
  C.J.i: u"0",
  C.J.z: C.J.FALSE,
  u"default": C.J.N
}
@takes(str, unicode, unicode)
@returns(unicode)
def default_value(cmd, ty, vname):
  if cmd == "android":
    if ty in C.primitives:
      if ty == C.J.z:
        v = u"SymUtil.new_sym_bit(\"{}\")".format(vname)
      else:
        v = u"SymUtil.new_sym_int(\"{}\")".format(vname)
    else:
      v = u"SymUtil.new_sym(\"{}\", \"{}\")".format(vname, ty)
  else:
    if ty in _default_values:
      v = _default_values[ty]
    else: v = _default_values[u"default"]
  return v


# autoboxing, e.g., int -> Integer
@takes(unicode)
@returns(unicode)
def autoboxing(tname):
  if tname in C.primitives:
    for i, v in enumerate(C.primitives):
      if tname == v: return C.autoboxing[i]

  return tname


# short form representation of type name
@takes(unicode)
@returns(optional(unicode))
def to_shorty(tname):
  # TODO: (multi-dimensional) array
  if tname in C.primitives:
    for key, value in C.J.__dict__.iteritems():
      if tname == value: return unicode(key)
  elif is_class_name(tname):
    return u'L'
  else: # erroneous
    return None


# Sketch-ish short form representation of type name
@takes(unicode)
@returns(unicode)
def to_shorty_sk(tname):
  shorty = to_shorty(tname)
  if shorty in [u'b', u's', u'i', u'j']: return u'i'
  elif shorty == u'z': return u'z'
  else: return u''


# check it is quoted
@takes(unicode)
@returns(bool)
def is_str(x):
  return len(x) >= 2 and (x[0] == '"' and x[-1] == '"')


# capitalize the first character only
# e.g., applicationContext -> ApplicationContext
@takes(unicode)
@returns(unicode)
def cap_1st_only(s):
  return s[:1].upper() + s[1:] if s else ''


# explode method name
# android.app.Activity.onCreate -> android.app, Activity, onCreate
@takes(unicode)
@returns(tuple_of(unicode))
def explode_mname(mname):
  mid = mname.split('.')
  mtd = mid[-1]
  if len(mid) > 1:
    cls = mid[-2]
    pkg = u'.'.join(mid[:-2])
  else:
    pkg = cls = u''
  return (pkg, cls, mtd)


"""
handling ANTLR AST
"""

@takes(list_of(str))
@returns(AST)
def toAST(files):
  ast = antlr3.tree.CommonTree(None)
  for fname in files:
    logging.debug("reading: " + os.path.normpath(fname))
    f_stream = antlr3.FileStream(fname)
    lexer = Lexer(f_stream)
    t_stream = antlr3.CommonTokenStream(lexer)
    parser = Parser(t_stream)
    try: _ast = parser.compilationUnit()
    except antlr3.RecognitionException:
      traceback.print_stack()
      sys.exit(1)
    ast.addChild(_ast.tree)
  return ast


# implode Ids
# KeyEvent . Callback -> KeyEvent.Callback
# Map < String, SharedPreferences > -> Map<String,SharedPreferences>
@takes(AST)
@returns(unicode)
def implode_id(node):
  def retrieve_info(node):
    t = node.getText()
    if node.getChildCount() <= 0: below = u''
    else: below = u''.join(map(retrieve_info, node.getChildren()))
    if not t or t in C.T.__dict__.values(): return below
    else: return t + below
  ids = map(retrieve_info, node.getChildren())
  return u''.join(ids)


# make a virtual node with the given children
# e.g., (uop id . id (ARGUMENT ...)) -> (None id . id (ARGUMENT ...))
@takes(list_of(AST))
@returns(AST)
def mk_v_node_w_children(nodes):
  v_node = AST(None)
  v_node.addChildren(nodes)
  return v_node


# implode and explode comma-separated elements
# [d , l . distance] -> [(None d), (None l . distance)]
@takes(list_of(AST))
@returns(list_of(AST))
def parse_comma_elems(nodes):
  def reduce_at_comma((res, acc), node):
    if node.getText() == ',':
      return res + [mk_v_node_w_children(acc)], []
    else:
      return res, acc + [node]
  res, acc = reduce(reduce_at_comma, nodes, ([], []))
  if not acc: return res
  else: return res + [mk_v_node_w_children(acc)]


"""
utilities whose names are inspired by OCaml
"""

# base class for exceptions regarding List
class ListError(Exception): pass


# ~ List.tl in OCaml
# remove the head of the list
@takes(list)
@returns(list)
def tl(lst):
  if len(lst) < 1: raise ListError("tl")
  return list(islice(lst, 1, None))


# ~ List.exists in OCaml
# checks if at least one element of the list satisfies the predicate
@takes(callable, list)
@returns(bool)
def exists(pred, lst):
  return any(filter(pred, lst))


# ~ List.find in OCaml
# find the first element of interest
@takes(callable, list)
@returns(anything)
def find(pred, lst):
  f_ed = filter(pred, lst)
  if not f_ed: raise ListError("Not_found")
  else: return f_ed[0]


# ~ List.assoc in OCaml
# return the value associated with the given key
# e.g., assoc(a, [..., (a, b), ...]) == b
@takes(anything, list_of(tuple_of(anything)))
@returns(anything)
def assoc(a, lst):
  for x, y in lst:
    if a == x: return y
  raise ListError("Not_found")


# ~ List.partition in OCaml
# divide the given list into two lists:
# one satisfying the conditoin and the other not satisfying the condition
# e.g., \x . x > 0, [1, -2, -3, 4] -> [1, 4], [-2, -3]
@takes(callable, list)
@returns(tuple_of(list))
def partition(pred, lst):
  return list(ifilter(pred, lst)), list(ifilterfalse(pred, lst))


# ~ List.split in OCaml
# transform a list of pairs into a pair of lists
# e.g., [ (1, 'a'), (2, 'b'), (3, 'c') ] -> ([1, 2, 3], ['a', 'b', 'c'])
@takes(list_of(tuple_of(anything)))
@returns(tuple_of(list_of(anything)))
def split(lst):
  if not lst: return ([], [])
  else: 
    a, b = zip(*lst) # zip doesn't handle an empty list
    return (list(a), list(b))


# ~ List.flatten in OCaml
# e.g., [ [1], [2, 3], [4] ] -> [1, 2, 3, 4]
@takes(list_of(list_of(anything)))
@returns(list_of(anything))
def flatten(lstlst):
  return list(chain.from_iterable(lstlst))


# flatten class declarations or hierarchy
# "inners": class A { class Inner { class InnerMost }} -> [A, Inner, InnerMost]
# "subs": ActA, ActB, ... < Act < Cxt -> [Cxt, Act, ActA, ActB, ...]
@takes(list_of("Clazz"), str)
@returns(list_of("Clazz"))
def flatten_classes(clss, attr):
  mapped = map(op.attrgetter(attr), clss)
  if not mapped: return clss
  else:
    flattened = flatten(mapped)
    diff = list(set(flattened) - set(clss))
    if not diff: return clss
    else: return flatten_classes(clss + diff, attr)


"""
More utilities
"""

# intersection: common elements in both lists
# e.g., [a, b, c] & [a, b, d] -> [a, b]
@takes(list_of(anything))
@returns(list_of(anything))
def intersection(lst1, lst2):
  return list(set(lst1) & set(lst2))


# remove duplicates in the given list
# e.g., [1, 2, 2] -> [1, 2]
@takes(list_of(anything))
@returns(list_of(anything))
def rm_dup(lst):
  return list(set(lst))


# remove None in the given list
# e.g., [1, 2, None, 3] -> [1, 2, 3]
@takes(list_of(anything))
@returns(list_of(anything))
def rm_none(lst):
  return filter(partial(op.is_not, None), lst)


# remove anything that is evaluated to False, such as None or empty string
# e.g., [1, 2, None, 3] -> [1, 2, 3]
#       ["a", "", "z"] => ["a", "z"]
@takes(list_of(anything))
@returns(list_of(anything))
def ffilter(lst):
  return filter(None, lst)


# make a new entry of list type or append the given item
# e.g., {x: [1]}, x, 2 => {x: [1,2]}
#       {x: [1]}, y, 2 => {x: [1], y: [2]}
@takes(dict_of(anything, list_of(anything)), anything, anything, optional(bool))
@returns(nothing)
def mk_or_append(dic, k, v, uniq=True):
  if k in dic: # already bound key
    if not uniq or v not in dic[k]: # uniq => value v not recorded
      dic[k].append(v)
  else: # new occurence of key k
    dic[k] = [v]


@takes(list_of(dict_of(anything, list_of(anything))))
@returns(dict_of(anything, list_of(anything)))
def merge_dict(lst):
  def reducer(acc, dic):
    keys = set(acc.keys() + dic.keys())
    return dict((k, rm_dup(acc.get(k, []) + dic.get(k, []))) for k in keys)
  return reduce(reducer, lst, {})


@takes(nothing)
@returns(str)
def get_datetime():
  return datetime.datetime.now().strftime("%y%m%d_%H%M%S")


"""
Yale Sparse Matrix Format
http://www.cs.yale.edu/publications/techreports/tr112.pdf
"""

@takes(list_of(list_of(int)))
@returns(tuple_of(list_of(int)))
def yale_format(mat):
  if not mat: return [], [], []

  # assume rows are of the same size
  m, n = len(mat), len(mat[0])
  A = []
  IA = []
  JA = []
  ja_idx = 0
  IA.append(ja_idx)

  for i in xrange(0, m):
    for j in xrange(0, n):
      itm = mat[i][j]
      if itm:
        A.append(itm)
        JA.append(j)
        ja_idx = ja_idx + 1
    IA.append(ja_idx)

  return A, IA, JA

