#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
try: unicode
except: unicode = u"".__class__
from ..utils import utils

from ..body.methoddeclaration import MethodDeclaration
from ..body.parameter import Parameter
from ..body.variabledeclarator import VariableDeclarator
from ..stmt.blockstmt import BlockStmt
from ..stmt.expressionstmt import ExpressionStmt
from ..stmt.ifstmt import IfStmt
from ..stmt.forstmt import ForStmt
from ..stmt.returnstmt import ReturnStmt
from ..expr.nameexpr import NameExpr
from ..expr.assignexpr import AssignExpr
from ..expr.variabledeclarationexpr import VariableDeclarationExpr

import copy as cp

from ..visit import visit

v = visit

# if parent is one of these keep the same in_set
FLOWSTHRU = [ExpressionStmt, IfStmt, VariableDeclarationExpr, ReturnStmt,
             AssignExpr, MethodDeclaration, VariableDeclarator, ForStmt]
# if parent is one of these make parent's out_set the out_set of the child
FLOWSUP = [ExpressionStmt, VariableDeclarationExpr]
# out_sets are handled specifically
NO_OUT = [BlockStmt, MethodDeclaration, IfStmt, ForStmt]
          
class DataFlow(object):
    def __init__(self):
        pass
        
    # this kwargs isnt **kwargs b/c its an actual dict, not list of named params
    def analyze(self, program, gsymtab, kwargs):
        self._walk(utils.rm_comments, program)
        
        e = kwargs['e'] if kwargs['e'] else [-1, -1]
        self._estart = int(e[0])
        self._estop = int(e[1])
        self._gsymtab = gsymtab

        self._program = program
        self._debug = kwargs.get('debug', False)

        # ret_types = kwargs.get('types', False)
        inputs = kwargs.get('inputs', False)
        verbose = kwargs.get('verbose', False)
        reach = kwargs.get('reach', False)

        ins, outs = [], []
        if reach:
            self._doreach()
        elif inputs:
            if self._estart < 0 or self._estop < 0: return None, None
            for m in utils.extract_nodes([MethodDeclaration], self._program):
                if m.body and m.body.childrenNodes:
                    ins, outs = self._gen_inputs(m)
                else:
                    return None, None
        if verbose:
            def f1(node):
                print('node:', type(node), 'name:', node.name, \
                    '\n\tin:', node.in_set, \
                    '\n\tout:', node.out_set, \
                    '\n\tinputs:', node.inputs, \
                    '\n\toutputs:', node.outputs)
                print()
            self._walk(f1, self._program)
            if inputs: print(ins, outs)
        return ins, outs

    def _doreach(self, program=None):
        if not program: program = self._program
        self._worklist = []
        self._walk(self._wappend, self._program)

        while self._worklist:
            n = self._worklist.pop(0)
            self._reach(n)

    def _reach(self, n):
        self._compute_in_out(n)
        if type(n) == BlockStmt:
            num = len(n.childrenNodes)
            # # this replaces the regular input flow
            if num > 0:
                n.childrenNodes[0].in_set = n.childrenNodes[0].in_set.union(n.in_set)
            # each node's output flows to the next node's inset
            for i in xrange(num):
                if i > 0 and i < num:
                    t = n.childrenNodes[i].in_set.union(n.childrenNodes[i - 1].out_set)
                    if t != n.childrenNodes[i].in_set:
                        # previous node's outset has changed
                        n.childrenNodes[i].in_set = t
                        self._walk(self._wappend, n.childrenNodes[i])
            # the outset from the last node flows to the outset of this node
            n.out_set = n.childrenNodes[-1].out_set
            if type(n.parentNode) == MethodDeclaration:
                n.parentNode.out_set = n.out_set

    def _compute_in_out(self, n):
        if not n.parentNode or type(n) == Parameter: return
        # the inset here comes from the analysing the blockstmt
        if type(n.parentNode) != BlockStmt:
            n.in_set = n.parentNode.out_set.union(n.in_set)
        # in_set from these nodes flow through to childrenNodes
        if type(n.parentNode) in FLOWSTHRU or type(n) == NameExpr:
            n.in_set = n.parentNode.in_set
        if type(n.parentNode) == AssignExpr and n == n.parentNode.target:
            n.in_set = set([])

        if type(n) == ForStmt:
            t = set(n.in_set.union(n.out_set))
            if t != n.out_set:
                n.out_set = t
                self._worklist.append(n.parentNode)

        # in_set from parentNode flows to outset of IfStmt
        if type(n) == IfStmt:
            outs = []
            returns = False
            # if there is an else clause we need to check if any variable is
            # defined in all branches so it can be removed from the out_set
            if n.elseStmt:
                if utils.extract_nodes([ReturnStmt], n.thenStmt) and \
                   utils.extract_nodes([ReturnStmt], n.elseStmt):
                    n.out_set = set([])
                    returns = True
                else:
                    outs = self._intersection(n.thenStmt.out_set, n.elseStmt.out_set)
                    # in + out - any defs in all branches (w/else)
            t = set(self._minus(n.in_set.union(n.out_set), outs))
            if t != n.out_set and not returns:
                n.out_set = t
                self._worklist.append(n.parentNode)

        t = n.gen().union((self._minus(n.in_set, n.kill())))
        if self._debug:
            print('n:', n, 'in:', n.in_set, 'gen:', n.gen(), 'kill:', n.kill(), \
                'in-kill', self._minus(n.in_set, n.kill()), 't:', t, \
                'out_set:', n.out_set)

        if type(n.parentNode) == ForStmt:
            inits = set(utils.flatten([e.out_set for e in n.parentNode.init])) \
                      if n.parentNode.init else set([])
            tt = n.parentNode.body.in_set.union(inits)
            if tt != n.parentNode.body.in_set:
                n.parentNode.body.in_set = tt
            tt = n.parentNode.out_set.union(n.parentNode.body.out_set)
            if tt != n.parentNode.body.in_set:
                n.parentNode.out_set = tt

        if type(n.parentNode) == IfStmt:
            n.parentNode.out_set = n.parentNode.out_set.union(n.out_set)

        # not too crazy about this. get all the names in the return expr and
        # filter out the defs from the in_set. need this for computing inputs
        if type(n) == ReturnStmt:
            names = utils.extract_nodes([NameExpr], n)
            names = [nm.name for nm in names]
            # TODO: can return more than one name, don't know if that makes sense
            n.out_set = set([x for x in n.in_set if x[0] in names])

        # out_set has changed. out_set of these are handled above
        elif t != n.out_set and type(n) not in NO_OUT:
            if type(n) not in FLOWSUP: n.out_set = t
            if type(n.parentNode) == BlockStmt:
                self._worklist.append(n.parentNode)
            if type(n) != BlockStmt and type(n) not in FLOWSUP:
                self._worklist.extend(n.childrenNodes)
        if type(n.parentNode) in FLOWSUP:
            n.parentNode.out_set = n.parentNode.out_set.union(n.out_set)
            self._worklist.append(n.parentNode)

    def _inputs(self, n, c_defs):
        for ch in n.childrenNodes:
            self._inputs(ch, c_defs)
            reach_x = [x for x in ch.in_set if x[0] == ch.lbl[0]]
            ins = self._rm_dups([x for x in reach_x if x in c_defs])
            if self._debug:
                print('ch:', ch, 'ch.in_set:', ch.in_set, \
                    'reach_x:', reach_x, \
                    'c_defs:', c_defs, 'ins:', ins)
            if ins: ch.inputs = list(ins)
            # all this crap is to remove duplicate var defs from in/out sets
            if ch.inputs:
                n.inputs = list(self._rm_dups(n.inputs + ch.inputs))

    def _gen_inputs(self, method):
        self._doreach()
        # methods = utils.extract_nodes([MethodDeclaration], program)
        # methods is now a list of method nodes
        body = method.body.childrenNodes
        # compute inputs for expr e
        ctx = BlockStmt()
        ctx.childrenNodes = body[:self._estart]
        e = BlockStmt()
        e.childrenNodes = body[self._estart:self._estop + 1]
        if self._debug: print('*******inputs*******')

        # need to add this to the initial context if it is at the start of method
        params = [x.lbl for x in method.parameters]
        # c_defs are all the defs leaving the context. defs in e will have to
        # be part of this set to be valid inputs
        c_defs = ctx.childrenNodes[-1].out_set.union(set(params)) if ctx.childrenNodes else set(params)
        self._inputs(e, c_defs)

        # change the context to be the remainder of the body, compute
        # inputs to context, which are outputs from e
        ctx.childrenNodes = body[self._estop + 1:]
        if ctx.childrenNodes:
            if self._debug: print('*******outputs******')

            c_defs = e.childrenNodes[-1].out_set.difference(e.childrenNodes[0].in_set)
            self._inputs(ctx, c_defs)

            e.childrenNodes[-1].outputs = []
            ins = set([])
            for x in ctx.childrenNodes:
                ins.update(x.inputs)
            if ins:
                e.childrenNodes[-1].outputs = [[self.get_typ(i).name for i in list(self._rm_dups(ins))][0]]
        else:
            if utils.extract_nodes([ReturnStmt], e):
                e.childrenNodes[-1].outputs = [unicode(method.typee)]
                    
        # we need all the inputs for all the childrenNodes of e
        # TODO: can we assume we can just smash all the inputs together?
        ins = set([])
        for x in e.childrenNodes:
            ins.update(x.inputs)
        def to_nm(n):
            n.inputs = [self.get_typ(i).name for i in n.inputs]
        self._walk(to_nm, e)
        e.childrenNodes[0].inputs = [self.get_typ(i).name for i in ins]
        return e.childrenNodes[0].inputs, e.childrenNodes[-1].outputs
        
    def get_typ(self, lbl):
        return self._gsymtab[lbl[1]].symtab[lbl[0]].typee
    
    def _walk(self, f, n, *args):
        f(n, *args)
        for c in n.childrenNodes:
            self._walk(f, c, *args)

    def _rm_dups(self, s):
        ret = set([])
        added = []
        for ss in s:
            if ss[0] not in added:
                ret.add(ss)
                added.append(ss[0])
        return ret

    def _minus(self, inn, kill):
        if not inn: return set([])
        elif not kill: return set(inn)
        s = cp.copy(inn)
        for k in kill:
            s = [x for x in s if x[0] != k[0]]
        return s

    def _intersection(self, s0, s1):
        names = [x[0] for x in list(s0)]
        return set([x for x in list(s1) if x[0] in names])

    def _wappend(self, n, *args):
        self._worklist.append(n)
