#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:16:02 2017

@author: misakawa
"""

bootstrap = True
from ..ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser
lit = LiteralParser 

Str    = lit("[R]{0,1}'[\w|\W]*?'", name = 'Str')
Name   = lit('[a-zA-Z_][a-zA-Z0-9]*', name = 'Name')
Number = lit('\d+',name = 'Number')

NEWLINE= lit('\n', name = 'NEWLINE')

LBB = lit.Eliteral('{', name = 'LBB')
LB  = lit.Eliteral('[', name = 'LB')
LP  = lit.Eliteral('(', name = 'LP')
RBB = lit.Eliteral('}', name = 'RBB')
RB  = lit.Eliteral(']', name = 'RB')
RP  = lit.Eliteral(')', name = 'RP')

SeqStar = lit.Eliteral('*', name = 'SeqStar')
SeqPlus = lit.Eliteral('+', name = 'SeqPlus')

Def     = lit.Eliteral('::=', name = 'Def')
OrSign  = lit.Eliteral("|",   name = 'OrSign')

namespace     = globals()
recurSearcher = set()

Expr = AstParser(
    [Ref('Or'),
     SeqParser([OrSign, Ref('Or')],
               atleast=0)
     ],
    name = 'Expr')
Or = AstParser(
    [SeqParser([Ref('AtomExpr')],
               atleast=1)
     ],
    name = 'Or')

AtomExpr =  AstParser(
    [Ref('Atom'), SeqParser([Ref('Trailer')])],
    name = 'AtomExpr'
)

Atom = AstParser(
    [Name],
    [Str],
    [LP, Ref("Expr"), RP],
    [LB, Ref("Expr"), RB],
    name = 'Atom')


Equals = AstParser(
    [Name, Def, Ref("Expr")],
    name = 'Equals')

Trailer = AstParser(
    [SeqStar],
    [SeqPlus],
    [LBB, SeqParser(
        [Number],
        atleast=1,
        atmost =2
        ),           RBB],
    name = 'Trailer')

Stmt  = AstParser(
            [SeqParser([
                        SeqParser([NEWLINE]),
                        SeqParser([Ref('Equals')]),
                        SeqParser([NEWLINE])
                       ]),
            ],
            name = 'Stmt')

Stmt.compile(namespace, recurSearcher)

def _genToken():
    namespace['aStr'] = namespace['Str']
    import re
    tk_reg = []
    tk_raw = []  
    for var in list(namespace.keys()):
        val = namespace[var]
        if isinstance(val, LiteralParser):
            if val.isRegex:
                tk_reg.append(val.token_rule)
            else:
                tk_raw.append(val.token_rule)

    token = re.compile("[R]{0,1}'[\w|\W]*?'"+ '|'+'|'.join(sorted(tk_raw)[::-1]+tk_reg) )
    return token
token = _genToken()






