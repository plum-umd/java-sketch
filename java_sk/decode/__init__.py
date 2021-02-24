
from ast.body.classorinterfacedeclaration import ClassOrInterfaceDeclaration
from ast.visit.generic import GenericVisitor

import os
from .. import util
from finder import HFinder, EGFinder

def to_java(java_output_dir, output_class_names, pgr, sk_output_path):
    ## clean up result directory
    if os.path.isdir(java_output_dir): util.clean_dir(java_output_dir)
    else: os.makedirs(java_output_dir)

    ## find holes
    hfinder = HFinder()
    pgr.accept(hfinder)
    holes = hfinder.holes

    ## replace holes with resolved answers
    #logging.info("replacing holes")
    #hreplacer = HReplacer(output_path, holes)
    #pgr.accept(hreplacer)

    ## find generators
    gfinder = EGFinder()
    pgr.accept(gfinder)
    egens = gfinder.egens


    ### replace regex generators with resolved answers
    #logging.info("replacing regex generators")
    #egreplacer = EGReplacer(output_path, egens)
    #pgr.accept(egreplacer)

    ## replace method generators with resolved body
    #logging.info("replace method generators")
    #mgreplacer = MGReplacer(output_path)
    #pgr.accept(mgreplacer)

    ## final semantic checking
    #logging.info("semantics checking")
    #_visitors = []
    ## replace collections of interface types with actual classes, if any
    #_visitors.append(Collection())
    #_visitors.append(SemanticChecker())
    #map(lambda vis: pgr.accept(vis), _visitors)

    ### trimming of the program
    classes = get_classes(pgr, output_class_names)
    return (holes, egens, classes)

    #dump(java_dir, pgr, "decoding")

def get_classes(comp_unit, output_class_names):
    classes = {}
    def find_classes(node):
        if type(node) == ClassOrInterfaceDeclaration:
            classes[node.fullname] = node
    class_finder = GenericVisitor(find_classes)
    comp_unit.accept(class_finder)
    return list(map(lambda name: classes[name], output_class_names))



