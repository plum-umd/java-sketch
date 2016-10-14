import sys
import os


pwd = os.path.dirname(__file__)

javaAST = os.path.abspath(os.path.join(pwd,'../../javaAST'))
sys.path.insert(0, javaAST)

from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.body.methoddeclaration import MethodDeclaration

sk_d = {u'@t': u'ClassOrInterfaceDeclaration', u'name': u''}
sk_cls = ClassOrInterfaceDeclaration(sk_d)

minimize = {u'@t': u'MethodDeclaration', u'name': {u'name': u'minimize'}, u'type': {u'@t': u'VoidType'}, u'parentNode': sk_d}
sk_cls.members.append(minimize)

builtins = {u'minimize': MethodDeclaration(minimize)}
