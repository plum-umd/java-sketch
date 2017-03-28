import os

from itertools import ifilter, ifilterfalse

from ast.utils import utils
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

import glob2

"""
regarding paths and files
"""
# clean all the contents in the designated path, excluding that path
def clean_dir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            try: os.unlink(os.path.join(root, f))
            except OSError: pass # maybe .swp file

# # autoboxing, e.g., int -> Integer
# def autoboxing(tname):
#   if tname in C.primitives:
#     for i, v in enumerate(C.primitives):
#       if tname == v: return C.autoboxing[i]

#   return tname


# # unboxking, e.g., Character -> char
# def unboxing(tname):
#   if tname in C.autoboxing:
#     for i, v in enumerate(C.autoboxing):
#       if tname == v: return C.primitives[i]

#   return tname
  
def add_object(ast):
    clss = utils.extract_nodes([ClassOrInterfaceDeclaration], ast)
    clss = filter(lambda c: c.name != u'Object', clss)
    obj = ast.symtab.get(u'Object')
    def obj_subs(n):
      if not n.extendsList:
          n.extendsList = [obj]
          obj.subClasses.append(n)
    map(obj_subs, clss)
    ast.types.append(obj)
  
def rm_subs(clss):
    return filter(lambda c: not c.extendsList and not c.implementsList, clss)

def sanitize_mname(mname):
    return mname.replace("[]",'s')

# ~ List.partition in OCaml
# divide the given list into two lists:
# one satisfying the conditoin and the other not satisfying the condition
# e.g., \x . x > 0, [1, -2, -3, 4] -> [1, 4], [-2, -3]
def partition(pred, lst):
    return list(ifilter(pred, lst)), list(ifilterfalse(pred, lst))

# get the contets of buf, close it, return contents
def get_and_close(buf):
    v = buf.getvalue()
    buf.close()
    return v

# get the *sorted* list of file names in the designated path
# template/gui/awt -> [.../AWTEvent.java, .../BorderLayout.java, ...]
def get_files_from_path(path, ext):
    if os.path.isfile(path):
        return [path]
    else: # i.e., folder
        files = glob2.glob(os.path.join(path, "**/*.{}".format(ext)))
    return sorted(files) # to guarantee the order of files read
    
def flatten(lst): return [j for i in lst for j in i]
