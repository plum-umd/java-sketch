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
    u'GN':0x20000,   # generator
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
    u'OR':u'|=',
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

JAVA_LANG = [
    # interfaces
    u'java.lang.Appendable',
    u'java.lang.AutoCloseable',
    u'java.lang.CharSequence',
    u'java.lang.Cloneable',
    u'java.lang.Comparable',
    u'java.lang.Iterable',
    u'java.lang.Readable',
    u'java.lang.Runnable',
    # u'java.lang.Thread$UncaughtExceptionHandler',

    # classes
    u'java.lang.Boolean',
    u'java.lang.Byte',
    u'java.lang.Character',
    # u'java.lang.Character$Subset',
    # u'java.lang.Character$UnicodeBlock'
    u'java.lang.Class',
    u'java.lang.ClassLoader',
    u'java.lang.ClassValue',
    u'java.lang.Compiler',
    u'java.lang.Double',
    u'java.lang.Enum',
    u'java.lang.Float',
    u'java.lang.InheritableThreadLocal',
    u'java.lang.Integer',
    u'java.lang.Long',
    u'java.lang.Math',
    u'java.lang.Number',
    u'java.lang.Object',
    u'java.lang.Package',
    u'java.lang.Process',
    u'java.lang.ProcessBuilder',
    # u'java.lang.ProcessBuilder$Redirect',
    u'java.lang.Runtime',
    u'java.lang.RuntimePermission',
    u'java.lang.SecurityManager',
    u'java.lang.Short',
    u'java.lang.StackTraceElement',
    u'java.lang.StrictMath',
    u'java.lang.String',
    u'java.lang.StringBuffer',
    u'java.lang.StringBuilder',
    u'java.lang.System',
    u'java.lang.Thread',
    u'java.lang.ThreadGroup',
    u'java.lang.ThreadLocal',
    u'java.lang.Throwable',
    u'java.lang.Void',
]

DESCRIPTOR_TYPES = {
    u'B': u'byte',   # signed byte
    u'C': u'char',   # Unicode character code point in the Basic Multilingual Plane, encoded with UTF-16
    u'D': u'double', # double-precision floating-point value
    u'F': u'float',  # single-precision floating-point value
    u'I': u'int',    # integer
    u'J': u'long',   # long integer
    u'L': u'ClassName', # ;referencean instance of class ClassName
    u'S': u'short',  # signed short
    u'V': u'void',   # void
    u'Z': u'boolean', # true or false
    u'[': u'reference', # one array dimension
} 

def _import():
    from .importdeclaration import ImportDeclaration

    from .body.classorinterfacedeclaration import ClassOrInterfaceDeclaration

    from .expr.nameexpr import NameExpr
    from .expr.qualifiednameexpr import QualifiedNameExpr

    from .type.referencetype import ReferenceType

    from .comments.javadoccomment import JavadocComment
    from .comments.linecomment import LineComment
    from .comments.blockcomment import BlockComment

    return locals()
