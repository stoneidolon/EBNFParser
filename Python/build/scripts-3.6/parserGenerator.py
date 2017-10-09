#!/home/misakawa/Software/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:48:35 2017

@author: misakawa
"""

testLangFile = \
"""
from Misakawa.ErrorFamily import handle_error
from parser import *
import argparse

cmdparser = argparse.ArgumentParser(description='Test Parser Generated by EBNFParser.')
cmdparser.add_argument("Parser", type = str,
                       help='What kind of parser do you want to test with?(e.g Stmt, Expr, ...)')
cmdparser.add_argument("Codes",  metavar = 'lispCodes', type = str,
                       help='Input some codes in your language here.')
cmdparser.add_argument("-testTk",  default = False, type = bool)
cmdparser.add_argument("-o",  default = "", type = str)

args = cmdparser.parse_args()

parser = handle_error(eval(args.Parser).match)

tokenized = token(args.Codes)
if args.testTk:
    print(tokenized)
result = parser(tokenized,partial=False)
print(result)
if args.o:
    import json
    with open(f"{args.o}.json", 'w', encoding = 'utf8') as JSONFile:
        json.dump(result.dumpToJSON(), JSONFile, indent = 4)
    with open(f"{args.o}Ast", 'w', encoding = 'utf8') as OriginAstFile:
        OriginAstFile.write(result.dump())
"""
from Misakawa.Bootstrap.Compile import compile as bootstrap_comp
import argparse
import re


_regexCommentRemove   = re.compile('#[\w\W]*?\n')
regexCommentRemove    = lambda string : _regexCommentRemove.sub('', string)
regexMultiLineSupport = lambda string : string.replace('\n','').replace('ENDL','\n')

cmdparser = argparse.ArgumentParser(description='using EBNFParser.')
cmdparser.add_argument("InputFile",  metavar = 'in_filename', type = str,
                       help='EBNF file which defines your grammar.')
cmdparser.add_argument("OutputFile", metavar = 'out_filename', type= str,
                       help='generated python file(s) that makes a parser for your language.')
cmdparser.add_argument("-test", default = True, type=bool, help="generate testLang.py?")
cmdparser.add_argument("-comment", default = False, type=bool, help="generate testLang.py?")
cmdparser.add_argument("-multiline", default = False, type=bool, help="generate testLang.py?")

args = cmdparser.parse_args()
inp, outp, is_test = args.InputFile, args.OutputFile, args.test

import sys,os   
head_from , _ = os.path.split(sys.argv[0])
head_to   , _ = os.path.split(outp)
with open(f'{head_to}/testLang.py','w', encoding='utf8') as testlang : testlang.write(testLangFile)
def getRaw(inp):
    with open(inp, 'r', encoding='utf8') as file: 
        ret = file.read()
    return ret

def selectMode(mode):
    toDo = []
    if 'comment' in mode:
        toDo.append(regexCommentRemove)
    if 'multiline' in mode:
        toDo.append(regexMultiLineSupport)
    return toDo
def transform(raw, mode):
    for f in selectMode(mode):
        raw = f(raw)
    return raw

mode = []
if args.comment:
    mode.append('comment')
if args.multiline:
    mode.append('multiline')

with open(outp,'w', encoding='utf8') as parserFile, open(  os.path.join(os.path.split(outp)[0],'token.py'), 
            'w', 
            encoding='utf8') as tokenFile: 
    parser, token = bootstrap_comp(
        transform(getRaw(inp), mode)
        , 'Unnamed')
    parserFile.write(parser)
    tokenFile.write(token)


