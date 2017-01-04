import sys
import os

pwd = os.path.dirname(__file__)

ast = os.path.abspath(os.path.join(pwd,'../parser'))
sys.path.insert(0, ast)

from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.methoddeclaration import MethodDeclaration

def convert(ch): return CONVERSION_TYPES[DESCRIPTOR_TYPES[ch]]

CONVERSION_TYPES = {u'boolean':u'bit',
                    u'this':u'self',
                    u'char':u'char',
                    u'byte':u'char',
                    u'short':u'char',
                    u'int':u'int',
                    u'long':u'double',
                    u'float':u'float',
                    u'double':u'double',
                    u'Byte':'char',
                    u'Character':'char',
                    u'Short':u'char',
                    u'Integer':u'int',
                    u'Long':u'long',
                    u'Float':u'float',
                    u'Double':u'double'}

DESCRIPTOR_TYPES = {u'B': u'byte', # signed byte
                    u'C': u'char', # Unicode character code point in the Basic Multilingual Plane, encoded with UTF-16
                    u'D': u'double', # double-precision floating-point value
                    u'F': u'float', # single-precision floating-point value
                    u'I': u'int', # integer
                    u'J': u'long', # long integer
                    u'L': u'ClassName', # ;referencean instance of class ClassName
                    u'S': u'short', # signed short
                    u'Z': u'boolean', # true or false
                    u'[': u'reference'} # one array dimension

sk_d = {u'@t': u'ClassOrInterfaceDeclaration', u'name': u''}
sk_cls = ClassOrInterfaceDeclaration(sk_d)

minimize = {u'@t': u'MethodDeclaration', u'name': {u'name': u'minimize'}, u'type': {u'@t': u'VoidType'}, u'parentNode': sk_d}
sk_cls.members.append(minimize)

builtins = {u'minimize': MethodDeclaration(minimize)}
