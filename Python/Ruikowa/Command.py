def main():
    # !/usr/bin/env python3
    # -*- coding: utf-8 -*-
    """
    Created on Mon Oct  2 13:48:35 2017

    @author: misakawa
    """

    testLangFile = lambda fileName: """
from Ruikowa.ErrorFamily import handle_error
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from """ + fileName.replace('.py', '') + """ import *
import argparse

cmdparser = argparse.ArgumentParser(description='Test Parser Generated by EBNFParser.')
cmdparser.add_argument("Parser", type = str,
                       help='What kind of parser do you want to test with?(e.g Stmt, Expr, ...)')
cmdparser.add_argument("Codes",  metavar = 'lispCodes', type = str,
                       help='Input some codes in your language here.')
cmdparser.add_argument("-testTk",  default = False, type = bool)
cmdparser.add_argument("-o",  default = "", type = str)

args   = cmdparser.parse_args()
meta   = MetaInfo()
parser = handle_error(eval(args.Parser))

tokenized = token(args.Codes)
if args.testTk:
    print(tokenized)
result = parser(tokenized,meta = meta, partial=False)
print(result)
if args.o:
    import json
    with open("{O}.json".format(O=args.o), 'w', encoding = 'utf8') as JSONFile:
        json.dump(result.dumpToJSON(), JSONFile, indent = 4)
    with open("{O}".format(O=args.o), 'w', encoding = 'utf8') as OriginAstFile:
        OriginAstFile.write(result.dump())
    """
    from .Bootstrap.Compile import compile as bootstrap_comp
    import argparse
    import re
    import warnings

    cmdparser = argparse.ArgumentParser(description='using EBNFParser.')
    cmdparser.add_argument("InputFile", metavar='in_filename', type=str,
                           help='EBNF file which defines your grammar.')
    cmdparser.add_argument("OutputFile", metavar='out_filename', type=str,
                           help='generated python file(s) that makes a parser for your language.')
    cmdparser.add_argument("-lang", default="Unnamed", type=str, help="Name your own language with this param.")

    args = cmdparser.parse_args()
    inp, outp = args.InputFile, args.OutputFile

    import sys, os

    head_from, _ = os.path.split(sys.argv[0])
    head_to, __ParserFile__ = os.path.split(outp)

    with open('{head_to}/testLang.py'.format(head_to=head_to), 'w', encoding='utf8') as testlang:
        testlang.write(testLangFile(__ParserFile__))
    bootstrap_comp(inp, args.lang)
    # with open(outp, 'w', encoding='utf8') as parserFile, \
    #         open(os.path.join(os.path.split(outp)[0], 'etoken.py'), 'w', encoding='utf8') as tokenFile:
    #     bootstrap_comp(inp, args.lang)
    #     parserFile.write(parser)
    #     tokenFile.write(token)


if __name__ == '__main__':
    main()
