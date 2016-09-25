from lib.enum import enum
import lib.const as C

# Terminals used at AST
C.T = enum(ANNO="ANNOTATION", \
    PKG="package", CLS="class", ITF="interface", ENUM="enum", \
    EXT="extends", IMP="implements", THROWS="throws", \
    DECL="DECL", FLD="FIELD", MTD="METHOD", \
    TYPE="TYPE", NAME="NAME", PARA="PARAMS", ELT="ELEMS", \
    STM="STAT", EXP="EXPR", ARG="ARGV", CAST="CAST", INS_OF="instanceof", \
    HOLE=u"??", REG_L=u"{|", REG_R=u"|}", REGEN="REGEN")

# constants regarding Java
C.J = enum(MAIN=u"main", CLINIT=u"clinit", \
    TRUE=u"true", FALSE=u"false", N=u"null", \
    NEW="new", THIS=u"this", SUP=u"super", \
    v=u"void", z=u"boolean", b=u"byte", s=u"short", c=u"char", \
    i=u"int", j=u"long", f=u"float", d=u"double", \
    V=u"Void", Z=u"Boolean", B=u"Byte", S=u"Short", C=u"Character", \
    I=u"Integer", J=u"Long", F=u"Float", D=u"Double", \
    OBJ=u"Object", RUN=u"Runnable", \
    STR=u"String", SB=u"StringBuffer", \
    MAP=u"Map", LST=u"List", STK=u"Stack", QUE=u"Queue", ITER=u"Iterator", \
    TMAP=u"TreeMap", LNK=u"LinkedList", DEQ=u"ArrayDeque")

# Java primitive types
C.primitives = [C.J.z, C.J.b, C.J.s, C.J.c, C.J.i, C.J.j, C.J.f, C.J.d]

# Java autoboxing: should be in order!
C.autoboxing = [C.J.Z, C.J.B, C.J.S, C.J.C, C.J.I, C.J.J, C.J.F, C.J.D]

# Java collections
C.collections = [C.J.MAP, C.J.LST, C.J.STK, C.J.QUE, C.J.ITER] \
              + [C.J.TMAP, C.J.LNK, C.J.DEQ]

# type information encodings
C.typ = enum(argNum="argNum", argType="argType", retType="retType", \
    belongsTo="belongsTo", subcls="subcls")

C.typ_arrays = [C.typ.argNum, C.typ.argType, C.typ.retType] \
             + [C.typ.belongsTo, C.typ.subcls]

