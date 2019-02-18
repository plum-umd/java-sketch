# This is a bit silly having utils/utils.py but it's the only way I could
# make this an importable package.

from __future__ import absolute_import
from __future__ import print_function
import os
import logging
import subprocess

from functools import partial

from .. import Modifiers

from ast import DESCRIPTOR_TYPES

from ast.importdeclaration import ImportDeclaration

from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.fielddeclaration import FieldDeclaration
from ast.body.variabledeclarator import VariableDeclarator
from ast.body.parameter import Parameter

from ast.expr.nameexpr import NameExpr
from ast.expr.castexpr import CastExpr
from ast.expr.enclosedexpr import EnclosedExpr
from ast.expr.thisexpr import ThisExpr
from ast.expr.fieldaccessexpr import FieldAccessExpr
from ast.expr.arrayaccessexpr import ArrayAccessExpr
from ast.expr.assignexpr import AssignExpr
from ast.expr.binaryexpr import BinaryExpr
from ast.expr.conditionalexpr import ConditionalExpr
from ast.expr.objectcreationexpr import ObjectCreationExpr

from ast.stmt.returnstmt import ReturnStmt

from ast.type.primitivetype import PrimitiveType
from ast.type.referencetype import ReferenceType
from ast.type.classorinterfacetype import ClassOrInterfaceType

from ast.comments.comment import Comment

JAVA_HOME = None
RT_HAR = None
ACCESS_MODS = ['public', 'private', 'protected', 'final', 'super', 'interface', 'abstract', \
               'synthetic', 'annotation', 'enum', 'static']

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

# applies f to n and all children to n
#    updates n's fields with new children
def walk_changeState(f, n, *args):
    prevChildren = n.childrenNodes
    n = f(n, *args)
    children = []
    if n != None:
        for c in prevChildren:
            children.append(walk_changeState(f, c, *args))
        n.childrenNodes = children
        if isinstance(n, BinaryExpr):
            n.left = children[0]
            n.right = children[1]
        if isinstance(n, ReturnStmt):
            n.expr = children[0]
        if isinstance(n, ConditionalExpr):
            n.thenExpr = children[1]
            n.elseExpr = children[2]
    return n

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
    imps = extract_nodes([ImportDeclaration], ast)
    clss_dct = {c.name: c for c in clss}
    imps_dct = {i.cname(): i for i in imps}

    # updates class dict with subClasses, updates symtab
    def update(c, t):
        if t.name in clss_dct:
            sup = clss_dct[t.name]
            sup.subClasses.append(c)
            for k,v in sup.symtab.items():
                if k not in c.symtab: c.symtab.update({k:v})
        elif t.name in imps_dct:
            sup = imps_dct[t.name]
            sup.subClasses.append(c)
            
    for c in clss:
        for e in c.extendsList: update(c, e)
        for i in c.implementsList: update(c, i)

def is_subtype(t1, t2):
    if t1.name == t2.name: return True
    if not isinstance(t1, PrimitiveType) and t2.name == u'null': return True
    if not isinstance(t2, PrimitiveType) and t1.name == u'null': return True

    if (type(t1) == ClassOrInterfaceType and type(t2) == ReferenceType) or \
       (type(t2) == ClassOrInterfaceType and type(t1) == ReferenceType):
        return True
    if type(t1) != type(t2): return False
    if t2.name == u'Object': return True
    # primitive type
    if t1.name in widen:
        return True if t2.name in widen[t1.name] else False

    # Catch instance of object wrapper param
    if t1.name == u'Object' and isinstance(t2, ClassOrInterfaceDeclaration) and t2.axiom:
        return True    
    
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

def get_parent(n, ptype):
    if n.parentNode:
        if isinstance(n.parentNode, ptype):
            return n.parentNode
        else: return get_parent(n.parentNode, ptype)
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
            cls = n.get_coid()
            if not cls: return obj
            for s in cls.supers():
                if n.name in s.symtab: return s.symtab.get(n.name)
            if type(cls.parentNode) == ClassOrInterfaceDeclaration:
                return find_obj(cls.parentNode)

    if isinstance(n, CastExpr): o = n.symtab.get(n.typee.name)
    elif isinstance(n, EnclosedExpr): o = node_to_obj(n.inner)
    elif isinstance(n, ThisExpr): o = n.get_coid()
    # TODO: None here is wrong, it will fail somewhere...
    elif isinstance(n, FieldAccessExpr): o = find_fld(n, None)
    else: o = find_obj(n)

    if not o:
        print('node_to_obj() -- Cant find {}.{}:{}'.format(str(n.name), n.get_coid(),n.beginLine))
        # n might be a static reference to an imported class
        for k, v in n.symtab.get(u'_cu_').symtab.items():
            nm = k.split('.')[-1]
            if n.name == nm: o = ClassOrInterfaceType({u'@t': u'ClassOrInterfaceType', u'name': nm,},)
        # raise Exception('Cant find {}.{}:{}'.format(str(n.name),get_coid(n),n.beginLine))
    return o

def get_scopes_list(n):
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
    # top level variable of field access
    v = top(n)
    typ = v.typee.name
    primToBox = {
        u'int':u'Integer',
        u'byte':u'Byte',
        u'boolean':u'Boolean',
        u'short':u'Short',
        u'long':u'Long',
        u'float':u'Float',
        u'double':u'Double',
        u'char':u'Character'
    }
    if typ in primToBox:
        typ = primToBox[typ]
    cls = v.symtab.get(typ)
    # name of all the scope variables
    return (cls, scopes(n, []))
        
def find_fld(n, obj_struct):
    if isinstance(n.scope, (FieldAccessExpr, ArrayAccessExpr)):
        (cls, scps) = get_scopes_list(n)
        for s in scps:
            fld0 = cls.symtab.get(s)
            cls = cls.symtab.get(fld0.typee.name)
        fld = cls.symtab.get(n.field.name)
        if not fld:
            if fld0:
                return fld0.symtab.get(n.field.name)
            else: raise Exception('Cant find field: {}'.format(n.name))

        return fld

    # look up n's scope in symtab
    scope = node_to_obj(n.scope)

    if isinstance(scope, Parameter): scope = scope.idd
    
    if not scope:
        print('Cant find {}.{}:{}'.format(n.scope.name, n.name, n.beginLine))
        return None

    # n's scope might be a class (if static field)
    cls = scope.symtab.get(scope.typee.name) if type(scope) != ClassOrInterfaceDeclaration \
        else scope
    if not cls: # something went wrong.
        if isinstance(scope, ImportDeclaration): # maybe scope is an import?
            nm = str(scope).split('.')
            fdescriptors = get_fld_descriptors(os.path.join(*nm))
            fld = fld_from_descriptor(fdescriptors, n.field.name, nm[-1])
            obj_struct.members.append(fld)
            return fld
        if isinstance(scope.typee, ReferenceType): # maybe this is built-in field (e.g., array.length)
            return scope.symtab.get(n.field.name)
        raise Exception('utils - not cls...')

    fld = cls.symtab.get(n.name)
    # print 'n.name:', n.name, 'cls:', cls, type(n)
    # print cls.symtab
    if not fld: # didn't find field in this cls, look in imported supers
        supers = cls.extendsList
        for e in supers:
            if e.scope and str(e.scope) in cls.symtab:
                impdec = cls.symtab[str(e.scope)]
                nm = '{}${}'.format(impdec, e.name)
                fdescriptors = get_fld_descriptors(os.path.join(*nm.split('.')))
                fld = fld_from_descriptor(fdescriptors, n.field.name, sanitize_ty(nm))
                obj_struct.members.append(fld)
                return fld

    if not fld:
        if n.name in scope.symtab: return scope.symtab.get(n.name)
        raise Exception('fld {} not found in class {} or super classes.'.
                        format(n.field.name, cls.name))
    return fld

def fld_from_descriptor(fdescriptors, name, nm):
    d = [d for d in fdescriptors if d[1] == name][0]
    if not d: raise Exception('Couldnt find field {} in import {}.'.format(name, str(scope)))
    d[0] = DESCRIPTOR_TYPES[d[0]] if d[0] in DESCRIPTOR_TYPES else d[0]
    # make a field to return
    if d[0] in widen:
        typ = {u'@t':u'PrimitiveType', u'type':{u'name':d[0]}}
    else:
        typ = {u'@t':u'ClassOrInterfaceType', u'type':{u'name':d[0]}}
    vardec = {u'@t':u'VariableDeclarator',u'id':{u'@t':u'VariableDeclaratorId', u'name':unicode(d[1])}}
    fd = FieldDeclaration({u'@t':u'FieldDeclaration', u'modifiers':d[2], u'type':typ,
                           u'variables':{u'@e':[vardec]}})
    fd.parentNode = ClassOrInterfaceDeclaration({u'@t':u'ClassOrInterfaceDeclaration', u'name':nm})
    return fd
    
def anon_nm(a):
    if type(a.parentNode) == AssignExpr: return a.parentNode.target
    else: return anon_nm(a.parentNode)

def rm_comments(node):
    node.childrenNodes = filter(lambda n: not isinstance(n, Comment), node.childrenNodes)

def unpack_class_file(nm):
    global JAVA_HOME, RT_JAR

    if not JAVA_HOME:
        try:
            JAVA_HOME = os.environ['JAVA_HOME']
        except:
            cmd = ['/usr/libexec/java_home']
            try:
                JAVA_HOME = subprocess.check_output(cmd).strip(' \n')
            except (OSError, subprocess.CalledProcessError) as e:
                logging.error('Unable to set JAVA_HOME: {} {}'.format(e, getattr(e, 'output', '')))
                raise Exception('Unable to set JAVA_HOME')
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

    # this is a cool bit of sorcery to pair names with their descriptors
    cls = zip(*[iter(cls)]*2)
    flds = filter(lambda d: '(' not in d[0] and 'static {};' not in d[0], cls)
    # print 'flds:', flds

    cls_nm_full = nm.replace('/', '.') # [nm.rfind('/')+1:]
    cls_nm = nm[nm.rfind('/')+1:]
    # print 'cls:', cls

    cons = []
    for d in cls:
        t = d[0].split(' ')[-1].strip(';')
        if '(' in t and t[:t.find('(')] == cls_nm or t[:t.find('(')] == cls_nm_full:
            cons.append(d)
    # print 'cons:', cons

    mtds = []
    for d in cls:
        t = d[0].split(' ')[-1].strip(';')
        if '(' in t and t[:t.find('(')] != cls_nm and t[:t.find('(')] != cls_nm_full:
            mtds.append(d)
    # print 'mtds:', mtds

    return (flds, cons, mtds)

# for now this is going to return [[fld_type1, fld_name1], ...]
def get_fld_descriptors(path):
    (flds, _, _) = get_descriptors(path)
    # print 'fld_descriptors', flds
    descriptors = []
    for d in flds:
        nm = filter(lambda n: n not in ACCESS_MODS, d[0].split(' '))[1].strip(';')
        typ = d[1].split(' ')[1].strip('[L;')
        if typ[0] == '[': typ = typ[1:]
        if '/' in typ: typ = typ[typ.rfind('/')+1:]
        descriptors.append([typ, nm, Modifiers[u'ST'] if 'static' in d[0] else 0x0])
    return descriptors

def get_mtd_types(path, name, num_params):
    # [(method signature, JVM descriptor)]
    # print 'path:', path, 'method name:', name, 'num_params:', num_params
    (_, _, mtds) = get_descriptors(path)
    candidates = [d[1][d[1].find(':')+2:] for d in mtds if name+'(' in d[0]]
    ptypes = []
    def filter_by_params(c):
        params = c[c.find('(')+1:c.rfind(')')]
        if len(params) == 0 and num_params == 0:
            ret = c.strip('();[L')
            if '/' in ret: ret = ret[ret.rfind('/')+1:]
            ptypes.append([ret])
            return True
        i = 0
        typs = []
        while i < len(params):
            ch = params[i]
            # deal with arrays later
            if ch == '[': i += 1
            elif ch == 'L':
                semi = params.find(';', i)
                p = params[i:semi].strip('[L')
                if '/' in p: p = p[p.rfind('/')+1:]
                typs.append(p)
                i = semi + 1
            else:
                typs.append(ch)
                i += 1
            # print 'typs:', typs
        if len(typs) == num_params:
            ptypes.append(list(typs + [c[-1]]))
            return True
        return False
    filter(filter_by_params, candidates)
    # print 'filtered:', filter(filter_by_params, candidates)
    # print 'ptypes:', ptypes
    return ptypes

def mtd_type_from_callexpr(callexpr):
    if not callexpr.scope:
        raise Exception('Uninterpreted function with no scope? {}'.format(callexpr))
    scope = node_to_obj(callexpr.scope)
    typ = scope.typee
    # cls = scope.symtab.get(str(typ))
    cu = callexpr.symtab[u'_cu_'].symtab
    ftypes = []
    for key, val in cu.items():
        if isinstance(val, ImportDeclaration):
            nm = key.split('.')
            if str(typ) == nm[-1]:
                types = get_mtd_types(os.path.join(*nm), callexpr.name, len(callexpr.args))
                if not types:
                    raise Exception('Somethign went wrong: {} {}, {}:{}'.format(key, callexpr.name, str(callexpr.get_coid()), callexpr.beginLine))
                ftypes.extend(types)
    if not ftypes: raise Exception('Somethign went wrong (ftypes): {}, {}:{}'.format(callexpr.name, str(callexpr.get_coid()), callexpr.beginLine))
    return (ftypes, scope)

# this is also in ast.node...
def sanitize_ty(tname):
    return tname.replace('$','_').replace('.','_').replace('?', u'Object')
    
