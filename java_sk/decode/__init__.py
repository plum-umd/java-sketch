
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.visit.generic import GenericVisitor
from ast.visit.sourcevisitor import SourcePrinter

import os, logging
from .. import util
from finder import HFinder, EGFinder
from replacer import HReplacer
from cleaner import Cleaner

def to_java(java_output_dir, pgr, sk_output_path):
    ## clean up result directory
    if os.path.isdir(java_output_dir):
        util.clean_dir(java_output_dir)
    else:
        os.makedirs(java_output_dir)

    ## find holes
    hfinder = HFinder()
    pgr.accept(hfinder)
    holes = hfinder.holes

    ## replace holes with resolved answers
    logging.info("replacing holes")
    hreplacer = HReplacer(sk_output_path, holes)
    pgr.accept(hreplacer)

    ## find generators
    # gfinder = EGFinder()
    # pgr.accept(gfinder)
    # egens = gfinder.egens


    ### replace regex generators with resolved answers
    #logging.info("replacing regex generators")
    #egreplacer = EGReplacer(output_path, egens)
    #pgr.accept(egreplacer)

    ## replace method generators with resolved body
    #logging.info("replace method generators")
    #mgreplacer = MGReplacer(output_path)
    #pgr.accept(mgreplacer)

    ### get output classes
    classes = get_output_classes(pgr)

    ## final cleanup
    logging.info("clean up output Java code")
    cleaner = Cleaner()
    pgr.accept(cleaner)


    for cls in classes:
        logging.info("writing generated Java output for class {}".format(cls.fullname.encode()))
        printer = SourcePrinter()
        cls.accept(printer)
        with open(os.path.join(java_output_dir, "{}.java".format(cls.fullname.encode())), "w") as f:
            f.write(printer.buf.getvalue())

# Finding the class for output by looking for @JavaCodeGen annotations
# TODO: Alternatively, we could output all classes that does not have @JSketchStdLib
def get_output_classes(comp_unit):
    input_classes = []
    def find_output_classes(node):
        if type(node) == ClassOrInterfaceDeclaration:
            for anno in node.annotations:
                if anno.name.name == u'JavaCodeGen':
                    input_classes.append(node)
    class_finder = GenericVisitor(find_output_classes)
    comp_unit.accept(class_finder)
    return input_classes



