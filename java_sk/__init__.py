import sys
import os

pwd = os.path.dirname(__file__)

ast = os.path.abspath(os.path.join(pwd,'../parser'))
sys.path.insert(0, ast)

from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.methoddeclaration import MethodDeclaration

from ast import DESCRIPTOR_TYPES

def convert(t):
    d = DESCRIPTOR_TYPES[t] if t in DESCRIPTOR_TYPES else t
    return CONVERSION_TYPES[d] if d in CONVERSION_TYPES else t

CONVERSION_TYPES = {
    u'void':u'void',
    u'bit':u'bit',
    u'boolean':u'bit',
    u'this':u'self',
    u'char':u'char',
    u'byte':u'char',
    u'short':u'char',
    u'int':u'int',
    u'long':u'double',
    u'float':u'float',
    u'double':u'double',
    # u'Byte':'char',
    # u'Character':'char',
    # u'Short':u'char',
    # u'Integer':u'int',
    # u'Long':u'long',
    # u'Float':u'float',
    # u'Double':u'double',
}

sk_d = {u'@t': u'ClassOrInterfaceDeclaration', u'name': u''}
sk_cls = ClassOrInterfaceDeclaration(sk_d)

minimize = {u'@t': u'MethodDeclaration', u'name': {u'name': u'minimize'}, u'type': {u'@t': u'VoidType'}, u'parentNode': sk_d}
sk_cls.members.append(minimize)

builtins = {u'minimize': MethodDeclaration(minimize)}
