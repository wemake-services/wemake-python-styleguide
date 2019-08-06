# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.logic import prop_access


def test_accesses():
    """
    Testing completeness of ``accesses`` function's an inner loop.

    The inner loop iterates over all parts of an expression, but
    the function breaks the loop, when it encounters non ``AnyAccess`` type.
    Therefore, code coverage complains on the incomplete inner loop, so we
    have to prove that the loop can be completed.

    We can't create the test using a visitor, because the AST for the test
    can't be compiled due it is invalid syntax.
    """
    subscript = ast.Subscript(value=None)
    node = ast.Attribute(value=subscript)
    assert list(prop_access.accesses(node)) == [node, subscript]
