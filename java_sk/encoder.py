from ast.utils import utils
from ast.body.methoddeclaration import MethodDeclaration
from ast.body.typedeclaration import TypeDeclaration as td
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
    
def find_main(ast):
  clss = []
  utils.extract_nodes(clss, ClassOrInterfaceDeclaration, ast)

  mtds = []
  for c in clss:
    utils.extract_nodes(mtds, MethodDeclaration, c)
    mtds = filter(lambda m: td.isStatic(m.modifiers) and m.name == u'main', mtds)
  lenn = len(mtds)
  if lenn > 1:
    raise Exception("multiple main()s", mtds)
  return mtds[0] if lenn == 1 else None

def find_harness(ast):
  # TODO: these can also be specified with annotations -- we don't support those yet
  mtds = []
  utils.extract_nodes(mtds, MethodDeclaration, ast)
  mtds = filter(lambda m: td.isHarness(m.modifiers), mtds)
  return mtds[0] if mtds else None

def main_cls(ast):
  # get the main method and pull it's corresponding class out of the symtab.
  main = find_main(ast)
  main = ast.symtab[main.atr] if main else None
  harness = find_harness(ast)
  harness = ast.symtab[harness.atr] if harness else None
  if main:
    return main
  elif harness:
    return harness
  else: raise Exception("None of main() and @Harness is found")
