# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.wrong_keyword import (
    WrongKeywordViolation,
    WrongKeywordVisitor,
)


def test_del_keyword(assert_errors, parse_ast_tree):
    """Testing that `del` keyword is restricted."""
    tree = parse_ast_tree("""
    def check_del():
        s = {'key': 'value'}
        del s['key']
        del s
    """)

    visiter = WrongKeywordVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [
        WrongKeywordViolation,
        WrongKeywordViolation,
    ])
