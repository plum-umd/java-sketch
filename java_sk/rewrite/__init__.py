import logging

from lib.typecheck import *

from ..meta.program import Program

from semantic_checker import SemanticChecker

@takes(Program)
@returns(nothing)
def visit(pgr):

  # final semantic checking
  logging.info("semantics checking")
  chker = SemanticChecker()
  pgr.accept(chker)

