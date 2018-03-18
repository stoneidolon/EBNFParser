#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:00:43 2017

@author: misakawa
"""

from .Ast import Compiler
from .Parser import Stmts
from ..ObjectRegex.Node import MetaInfo
from ..ErrorHandler import ErrorHandler
from .Token import token_func
from ..io import grace_open

parser = ErrorHandler(Stmts.match, token_func)

include = (
    "from Ruikowa.ObjectRegex.Tokenizer import unique_literal_cache_pool, regex_matcher, char_matcher, str_matcher, Tokenizer\n"
    "from Ruikowa.ObjectRegex.Node import AstParser, Ref, SeqParser, LiteralValueParser, LiteralNameParser, Undef\n"
    "namespace = globals()\n"
    "recur_searcher = set()")


def compile(src_path):
    src_code = grace_open(src_path).read()
    stmts = parser.from_file(src_path, MetaInfo(fileName=src_path))
    compiler = Compiler(filename=src_path, src_code=src_code)
    compiler.ast_for_stmts(stmts)

    if compiler.token_func_src:
        token_func_src = compiler.token_func_src
    else:
        token_func_src = ("token_table = {}\n{}\n"
                          "token_func = lambda _: "
                          "Tokenizer.from_raw_strings(_, token_table, ({}, {}))"
                          ).format(compiler.token_spec.to_token_table(),
                                   compiler.token_spec.to_name_enum(),
                                   compiler.token_ignores[0],
                                   compiler.token_ignores[1])

    literal_parsers = '\n'.join(compiler.literal_parser_definitions)

    combined_parsers = '\n'.join(compiler.combined_parsers)

    compiling = '\n'.join(
        map(lambda _: '{}.compile(namespace, recur_searcher)'.format(_), compiler.compile_helper.alone))

    return '{}\n{}\n{}\n{}\n{}'.format(include, token_func_src, literal_parsers, combined_parsers, compiling)
