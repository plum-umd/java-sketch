#!/usr/bin/env python

def _import():
    from .classorinterfacetype import ClassOrInterfaceType
    from .primitivetype import PrimitiveType

    from ..expr.integerliteralexpr import IntegerLiteralExpr
    from ..expr.nameexpr import NameExpr
    from ..expr.annotationexpr import AnnotationExpr

    return locals()
