# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast.general.wrong_keyword import (
    WrongKeywordViolation,
    WrongKeywordVisitor,
)


def test_del_keyword(assert_errors, parse_ast_tree, default_options):
    """Testing that `del` keyword is restricted."""
    tree = parse_ast_tree("""
    def check_del():
        s = {'key': 'value'}
        del s['key']
        del s
    """)

    visitor = WrongKeywordVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        WrongKeywordViolation,
        WrongKeywordViolation,
    ])
