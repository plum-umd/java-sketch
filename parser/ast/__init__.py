# taken from http://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html#jvms-4.1
Modifiers = {
    u'PR':0x0002,
    u'PB':0x0001,
    u'PRO':0x000,
    u'AB':0x0400,
    u'ST':0x0008,
    u'FN':0x0010,
    u'GN':u"generator", # not sure -- remnant of the past
    # don't think there are any with these values
    u'OP':0x8000,   # optional
    u'HN':0x10000,   # harness
    u'GN':0x20000   # generator
}

Operators = {
    u'OR':u'||',
    u'AND':u'&&',
    u'BINOR':u'|',
    u'BINAND':u'&',
    u'XOR':u'^',
    u'EQUALS':u'==',
    u'NOTEQUALS':u'!=',
    u'LESS':u'<',
    u'GREATER':u'>',
    u'LESSEQUALS':u'<=',
    u'GREATEREQUALS':u'>=',
    u'LSHIFT':u'<<',
    u'RSIGNSHIFT':u'>>',
    u'RUNSINGNSHIFT':u'>>>',
    u'PLUS':u'+',
    u'MINUS':u'-',
    u'TIMES':u'*',
    u'DIVIDE':u'/',
    u'REMAINDER':u'%',
}

AssignOperators = {
    u'ASSIGN':u'=',
    u'STAR':u'*=',
    u'SLASH':u'/=',
    u'REM':u'%=',
    u'PLUS':u'+=',
    u'MINUS':u'-=',
    u'LSHIFT':u'<<=',
    u'RSIGNEDSHIFT':u'>>=',
    u'RUNSIGNEDSHIFT':u'>>>=',
    u'AND':u'&=',
    u'XOR':u'^=',
    u'OR':u'|='
}

field = {
    u"@t": u"FieldDeclaration",
    u"type": {
        u"@t": u"ReferenceType",
        u"type": {
            u"@t": u"ClassOrInterfaceType",
            u"name": u"A",
        },
    },
    u"variables": {
        u"@e": [
            {
                u"@t": u"VariableDeclarator",
                u"id": {
                    u"name": u"a",
                },
            }
        ]
    },
}

def _import():
    from .importdeclaration import ImportDeclaration

    from body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

    from expr.nameexpr import NameExpr
    from expr.qualifiednameexpr import QualifiedNameExpr

    from comments.javadoccomment import JavadocComment
    from comments.linecomment import LineComment
    from comments.blockcomment import BlockComment

    return locals()
