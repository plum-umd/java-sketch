import logging

from desugar import Desugar
from generator import CGenerator, MGenerator
# from hole import EHole
# from semantic_checker import SemanticChecker


def visit(pgr):

    # Desugaring is for minrepeat
    # Not implemented currently
    # desugar'ing syntax sugar
    logging.info("rewriting syntax sugar")
    desugar = Desugar()
    pgr.accept(desugar)

    # # specializing class-level generator
    # logging.info("specializing class-level generator")
    # cgen = CGenerator()
    # pgr.accept(cgen)

    # # specializing method-level generator
    # logging.info("specializing method-level generator")
    # mgen = MGenerator()
    # pgr.accept(mgen)

    # # rewriters
    # rws = {}

    # # expression hole
    # eh = EHole()
    # rws["exp hole"] = eh

    # for rw in rws:
    #     logging.info("rewriting {}".format(rw))
    #     pgr.accept(rws[rw])

    # # final semantic checking
    # logging.info("semantics checking")
    # chker = SemanticChecker()
    # pgr.accept(chker)
