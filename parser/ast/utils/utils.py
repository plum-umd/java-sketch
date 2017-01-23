# This is a bit silly having utils/utils.py but it's the only way I could
# make this an importable package.

import os
import logging
import subprocess

from functools import partial

from ast.importdeclaration import ImportDeclaration

from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.variabledeclarator import VariableDeclarator

from ast.expr.nameexpr import NameExpr
from ast.expr.castexpr import CastExpr
from ast.expr.enclosedexpr import EnclosedExpr
from ast.expr.thisexpr import ThisExpr
from ast.expr.fieldaccessexpr import FieldAccessExpr
from ast.expr.arrayaccessexpr import ArrayAccessExpr
from ast.expr.assignexpr import AssignExpr

from ast.type.classorinterfacetype import ClassOrInterfaceType

from ast.comments.comment import Comment

JAVA_HOME = None
RT_HAR = None

widen = {u'boolean':[],
         u'byte':[u'char',u'short',u'int',u'long',u'float',u'double'],
         u'short':[u'int',u'long',u'float',u'double'],
         u'char':[u'int',u'long',u'float',u'double'],
         u'int':[u'long',u'float',u'double'],
         u'long':[u'float',u'double'],
         u'float':[u'double'],
         # only necessary for subtype checking
         u'double':[u'double']}

narrow = {u'boolean':[],
          u'byte':[u'char'],
          u'short':[u'byte',u'char'],
          u'char':[u'byte',u'short'],
          u'int':[u'byte',u'short',u'char'],
          u'long':[u'byte',u'short',u'char',u'int'],
          u'float':[u'byte',u'short',u'char',u'int',u'long'],
          u'double':[u'byte',u'short',u'char',u'int',u'long',u'float']}

box = {u'boolean':u'Boolean',
       u'byte':u'Byte',
       u'short':u'Short',
       u'char':u'Char',
       u'int':u'Integer',
       u'long':u'Long',
       u'float':u'Float',
       u'double':u'Double',
       u'null':u'null'}

unbox = {u'Boolean':u'boolean',
         u'Byte':u'byte',
         u'Short':u'short',
         u'Char':u'char',
         u'Character':u'char',
         u'Integer':u'int',
         u'Long':u'long',
         u'Float':u'float',
         u'Double':u'double'}

def walk(f, n, *args):
    f(n, *args)
    for c in n.childrenNodes:
        walk(f, c, *args)

# takes a list and a list of types. extracts all nodes of any type in typ from program
def extract_nodes(typ, ast, istance=False, recurse=True):
    lst = []
    def f1(n, *args):
        if istance:
          if any(map(partial(isinstance, n),typ)): lst.append(n)
        elif type(n) in typ: lst.append(n)
    walk(f1, ast) if recurse else map(f1, [ast] + ast.childrenNodes)
    return lst

# check whether node is in AST
def in_ast(ast, node):
    for c in ast.childrenNodes:
        res = False
        if c == node: res = True
        else: res = in_ast(c, node)
        if res: return True

def dec_in_ast(ast, node):
    for c in ast.childrenNodes:
        res = False
        if type(c) == VariableDeclarator and c.name == node.name: res = True
        else: res = dec_in_ast(c, node)
        if res: return res

# takes in AST and populates subclass relationships
def build_subs(ast):
    clss = extract_nodes([ClassOrInterfaceDeclaration], ast)
    clss_dct = {c.name: c for c in clss}
    # updates class dict with subClasses, updates symtab
    def update(c, t):
        if t.name in clss_dct:
            sup = clss_dct[t.name]
            sup.subClasses.append(c)
            for k,v in sup.symtab.items():
                if k not in c.symtab: c.symtab.update({k:v})
    for c in clss:
        for e in c.extendsList: update(c, e)
        for i in c.implementsList: update(c, i)

def is_subtype(t1, t2):
    if type(t1) != type(t2): return False
    if t2.name == u'Object': return True
    # primitive type
    if t1.name in widen:
        return True if t2.name in widen[t1.name] else False

    cls1 = t1.symtab.get(t1.name)
    cls2 = t2.symtab.get(t2.name)
    if not cls1 or not cls2:
        raise Exception('Cant dereference {} or {}'.format(t1.name, t2.name))
    if cls1 in cls2.subClasses or cls1 == cls2: return True
    elif cls2.subClasses:
        return any(map(partial(is_subtype, cls1), cls2.subClasses))
    else: return False

def all_subClasses(n):
    acc = set([])
    def a(n):
        if n.subClasses:
            acc.update(n.subClasses)
            for s in n.subClasses: a(s)
            return acc
        else:
            return acc
    a(n)
    return list(acc)

def get_coid(n):
    if n.parentNode:
        if type(n.parentNode) == ClassOrInterfaceDeclaration:
            return n.parentNode
        else: return get_coid(n.parentNode)
    else: return None

def find_mtd(mname, cls):
    if mname in cls.symtab: return cls.symtab.get(mname)
    for s in cls.supers():
        if mname in s.symtab: return s.symtab.get(mname)
    raise Exception('Cant find method {} in cls {}'.format(mname, str(cls)))

def flatten(lst): return [j for i in lst for j in i]

def node_to_obj(n):
    # helper functions
    o = None
    def find_obj(obj):
        if n.name in obj.symtab: return obj.symtab.get(n.name)
        else:
            cls = get_coid(obj)
            if not cls: return obj
            for s in cls.supers():
                if n.name in s.symtab: return s.symtab.get(n.name)
            if type(cls.parentNode) == ClassOrInterfaceDeclaration:
                return find_obj(cls.parentNode)

    if type(n) == CastExpr: o = n.symtab[n.typee.name]
    elif type(n) == EnclosedExpr: o = node_to_obj(n.inner)
    elif type(n) == ThisExpr: o = get_coid(n)
    elif type(n) == FieldAccessExpr: o = find_fld(n)
    else: o = find_obj(n)

    if not o:
        print 'node_to_obj() -- Cant find {}.{}:{}'.format(str(n.name),get_coid(n),n.beginLine)
        # n might be a static reference to an imported class
        for k, v in n.symtab.get(u'_cu_').symtab.items():
            nm = k.split('.')[-1]
            if n.name == nm: o = ClassOrInterfaceType({u'@t': u'ClassOrInterfaceType', u'name': nm,},)
        # raise Exception('Cant find {}.{}:{}'.format(str(n.name),get_coid(n),n.beginLine))
    return o

def find_fld(n):
    scope = n.scope
    def top(s):
        if type(s.scope) == ArrayAccessExpr:
            if type(s.scope.nameExpr) == NameExpr: return n.symtab.get(s.scope.nameExpr.name)
            else: return top(s.scope.nameExpr)
        elif type(s.scope) == NameExpr: return n.symtab.get(s.scope.name)
        else: return top(s.scope)
    def scopes(s, a):
        if type(s.scope) == ArrayAccessExpr:
            if type(s.scope.nameExpr) == NameExpr: return a
            else: return scopes(s.scope.nameExpr, [s.scope.nameExpr.name] + a)
        elif type(s.scope) == NameExpr: return a
        else: return scopes(s.scope, [s.scope.name] + a)
    if type(n.scope) == FieldAccessExpr or type(n.scope) == ArrayAccessExpr:
        # top level variable of field access
        v = top(n)
        # print 'v:', v.name
        cls = v.symtab.get(v.typee.name)
        # print 'cls:', cls
        # name of all the scope variables
        scps = scopes(n, [])
        # print 'scps', scps
        for s in scps:
            fld = cls.symtab.get(s)
            cls = cls.symtab.get(fld.typee.name)
        fld = cls.symtab.get(n.field.name)
        return fld

    # look up n's scope in symtab
    # print 'finding field: n.scope.name={}, type(n.scope)={}, n.field.name={}'.format(n.scope.name, type(n.scope), n.field.name)
    scope = node_to_obj(n.scope)
    # print 'scope type(scope.typee)={}, type(scope)={}, scope.name={}'.format(type(scope.typee), type(scope), scope.name)
    if not scope:
        print 'Cant find {}.{}:{}'.format(n.scope.name, n.name, n.beginLine)
        return None
    # n's scope might be a class (if static field)
    cls = scope.symtab.get(scope.typee.name) if type(scope) != ClassOrInterfaceDeclaration \
        else scope
    fld = cls.symtab.get(n.name)

    if not fld:
        raise Exception('fld {} not found in class {} or super classes.'.
                        format(n.field.name, cls.name))
    return fld

def anon_nm(a):
    if type(a.parentNode) == AssignExpr: return a.parentNode.target
    else: return anon_nm(a.parentNode)

def rm_comments(node):
    node.childrenNodes = filter(lambda n: not isinstance(n, Comment), node.childrenNodes)


def unpack_class_file(nm):
    global JAVA_HOME, RT_JAR

    if not JAVA_HOME:
        JAVA_HOME = os.environ['JAVA_HOME']
        if not JAVA_HOME: raise Exception('Unable to find $JAVA_HOME')
        RT_JAR = os.path.join(JAVA_HOME, 'jre','lib', 'rt.jar')

    # extract class file from jar
    cmd = ['jar', 'xf', RT_JAR, nm]
    logging.debug(' '.join(cmd))
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logging.error('Unable to extract "{}" from RT_JAR "{}": {}'.format(nm, RT_JAR, e.output))

def get_descriptors(nm):
    unpack_class_file(nm)
    # Disassemble class file to get method types
    cmd = ['javap', '-s', nm]
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
    print 'path:', path, 'method name:', name, 'num_params:', num_params
    descriptors = get_descriptors(path)
    candidates = [d[1][d[1].find(':')+2:] for d in descriptors if name+'(' in d[0]]
    print 'candidates:', candidates
    ptypes = []
    def filter_by_params(c):
        params = c[c.find('(')+1:c.rfind(')')]
        if len(params) == 0 and num_params == 0:
            semi = c.find(';')
            if semi >= 0: ptypes.append([c[c.rfind('/')+1:semi]])
            else: ptypes.append(list(c[-1]))
            return True
        i = 0
        typs = []
        while i < len(params):
            ch = params[i]
            if ch == 'L':
                semi = params.find(';', i)
                typs.append(params[params.rfind('/', i)+1:semi])
                i = semi + 1
            else:
                typs.append(ch)
                i += 1
            print 'typs:', typs
        if len(typs) == num_params:
            ptypes.append(list(typs + [c[-1]]))
            return True
        return False
    print 'filtered:', filter(filter_by_params, candidates)
    print 'ptypes:', ptypes
    return ptypes

def mtd_type_from_callexpr(callexpr):
    if not callexpr.scope:
        raise Exception('Uninterpreted function with no scope? {}'.format(callexpr))
    scope = node_to_obj(callexpr.scope)
    typ = scope.typee
    cu = callexpr.symtab[u'_cu_'].symtab
    ftypes = []
    for key, val in cu.items():
        if isinstance(val, ImportDeclaration):
            nm = key.split('.')
            if str(typ) == nm[-1]:
                types = get_mtd_types(os.path.join(*nm), callexpr.name, len(callexpr.args))
                if not types:
                    raise Exception('Somethign went wrong: {} {}'.format(key, callexpr.name))
                ftypes.extend(types)
    if not ftypes: raise Exception('Somethign went wrong (ftypes): {}'.format(callexpr.name))
    return (ftypes, scope)
