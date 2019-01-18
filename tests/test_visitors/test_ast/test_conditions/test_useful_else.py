# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

correct_example1 = """
def function():
    if some_condition:
        return None
    return None
"""

correct_example2 = """
def function():
    if some_condition:
        return None
"""

correct_example3 = """
def function():
    if some_condition:
        return None
    elif other_condition:
        return None
    else:
        return None
"""

correct_example4 = """
def function():
    if some_condition:
        ...
    else:
        return None
"""

correct_example4 = """
if some_condition:
    ...
else:
    raise ValueError()
"""

correct_example5 = """
if some_condition:
    if other:
        raise TypeError()
else:
    raise ValueError()
"""

correct_example6 = """
def function():
    if some_condition:
        if other:
            raise TypeError()
        elif other is None:
            return None
        else:
            return other
    else:
        raise ValueError()
"""

correct_example7 = """
def function():
    if some_condition:
        with open() as file:
            return file
    else:
        raise ValueError()
"""


@pytest.mark.parametrize('code', [
    correct_example1,
    correct_example2,
    correct_example3,
    correct_example4,
    correct_example5,
    correct_example6,
    correct_example7,
])
def test_else_that_can_not_be_removed(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that extra ``else`` blocks can not be removed."""
    tree = parse_ast_tree(mode(code))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
