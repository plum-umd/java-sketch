from . import convert

import os
import shutil
import logging
import subprocess
from itertools import ifilter, ifilterfalse

from ast.utils import utils
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

import glob2

JAVA_HOME = None
RT_HAR = None

"""
regarding paths and files
"""
# clean all the contents in the designated path, excluding that path
def clean_dir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            try: os.unlink(os.path.join(root, f))
            except OSError: pass # maybe .swp file
        # for d in shutil:
        #     dirs.rmtree(os.path.join(root, d))
  
def add_object(ast):
    clss = utils.extract_nodes([ClassOrInterfaceDeclaration], ast)
    obj = ClassOrInterfaceDeclaration({u'name':u'Object',u'parentNode':{u'@r':ast.ati},u'atr':ast.ati,u'@i':0})
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

def unpack_class_file(nm):
    global JAVA_HOME, RT_JAR

    if not JAVA_HOME:
        JAVA_HOME = os.environ['JAVA_HOME']
        if not JAVA_HOME: raise Exception('Unable to find $JAVA_HOME')
        RT_JAR = os.path.join(JAVA_HOME, 'jre','lib', 'rt.jar')

    # extract class file from jar
    cmd = ['jar', 'xf', RT_JAR, nm]
    print cmd
    logging.debug(' '.join(cmd))
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logging.error('Unable to extract "{}" from RT_JAR "{}": {}'.format(nm, RT_JAR, e.output))

def get_descriptors(nm):
    unpack_class_file(nm)
    # Disassemble class file to get method types
    cmd = ['javap', '-s', nm]
    print cmd
    logging.debug(' '.join(cmd))
    try:
        cls = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logging.error('Unable to dissassemble "{}": {}'.format(nm, e.output))

    # only need method stuff (inside brackets)
    cls = cls[cls.find('{')+2:cls.rfind('}')]
    cls = [x.strip() for x in cls.split('\n') if x]

    # this is a cool bit of sorcery to pair method types with their descriptors
    cls = zip(*[iter(cls)]*2)
    return cls

def get_mtd_types(path, name, num_params):
    # [(method signature, JVM descriptor)]
    print 'method name:', name, 'num_params:', num_params
    descriptors = get_descriptors(path)
    candidates = [d[1][d[1].find(':')+2:] for d in descriptors if name+'(' in d[0]]
    print 'candidates:', candidates
    ptypes = []
    def filter_by_params(c):
        params = c[c.find('(')+1:c.rfind(')')]
        if len(params) == 0 and num_params == 0: return True
        i = 0
        typs = []
        while i < len(params):
            ch = params[i]
            if ch == 'L':
                semi = params.find(';', i)
                typs.append(params[params.rfind('/', i)+1:semi])
                i = semi + 1
            else:
                typs.append(convert(ch))
                i += 1
        if len(typs) == num_params:
            ptypes.append(tuple(typs + [convert(c[-1])]))
            return True
        return False
    print 'filtered:', filter(filter_by_params, candidates)
    print 'types:', ptypes
