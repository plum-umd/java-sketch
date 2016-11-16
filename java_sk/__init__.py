import sys
import os

pwd = os.path.dirname(__file__)

javaAST = os.path.abspath(os.path.join(pwd,'../../javaAST'))
sys.path.insert(0, javaAST)

from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.methoddeclaration import MethodDeclaration


JAVA_TYPES = {u'int':u'int',u'byte':u'byte',u'short':u'short',u'long':u'long',u'double':u'double',
            u'Byte':'Byte',u'Short':u'Short',u'Long':u'Long',u'Int':u'Integer'}
SKETCH_TYPES = {u'boolean':u'bit', u'this':'self'}

sk_d = {u'@t': u'ClassOrInterfaceDeclaration', u'name': u''}
sk_cls = ClassOrInterfaceDeclaration(sk_d)

minimize = {u'@t': u'MethodDeclaration', u'name': {u'name': u'minimize'}, u'type': {u'@t': u'VoidType'}, u'parentNode': sk_d}
sk_cls.members.append(minimize)

builtins = {u'minimize': MethodDeclaration(minimize)}
