# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.statements import (
    ParametersIndentationViolation,
    WrongParametersIndentationVisitor,
)

# Correct:

correct_single_line_call = 'print(1, 2, 3)'
correct_multi_line_call = """
print(
    1,
    2,
    3,
)
"""

correct_multi_line_call_with_keywords = """
print(
    1,
    2,
    3,
    end='',
)
"""

correct_next_line_call = """
print([
    1, 2, 3,
])
"""

correct_next_line_call_with_keywords = """
print(
    [1, 2, 3],
    end='',
)
"""

correct_call_with_multi_line_tuple = """
print((
    1,
    2,
    3,
))
"""

correct_call_with_next_line_parameter = """
print(0, [
    1, 2, 3,
])
"""

correct_call_with_multi_line_parameter = """
print(0, [
    1,
    2,
    3,
])
"""

correct_call_all_multi_line = """
print(
    0,
    [
        1,
        2,
        3,
    ],
    end='',
)
"""

# Wrong:

wrong_call_indentation1 = """
print(1,
      2, 3)
"""

wrong_call_indentation2 = """
print(1, 2,
      3)
"""

wrong_call_indentation3 = """
print(
    1,
    2, 3,
)
"""

wrong_call_indentation4 = """
print(
    1, 2,
    3,
)
"""

wrong_call_indentation5 = """
print(
    1,
    2,
    3, end='',
)
"""

wrong_call_indentation6 = """
print(
    1,
    2, 3, end='',
)
"""

wrong_call_indentation7 = """
print(0, [
    1,
    2,
    3,
], end='')
"""


@pytest.mark.parametrize('code', [
    correct_single_line_call,
    correct_multi_line_call,
    correct_multi_line_call_with_keywords,
    correct_next_line_call,
    correct_next_line_call_with_keywords,
    correct_call_with_multi_line_tuple,
    correct_call_with_next_line_parameter,
    correct_call_with_multi_line_parameter,
    correct_call_all_multi_line,
])
def test_correct_call_indentation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correctly indented function calls work."""
    tree = parse_ast_tree(code)

    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_call_indentation1,
    wrong_call_indentation2,
    wrong_call_indentation3,
    wrong_call_indentation4,
    wrong_call_indentation5,
    wrong_call_indentation6,
    wrong_call_indentation7,
])
def test_wrong_call_indentation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that poorly indented function calls do not work."""
    tree = parse_ast_tree(code)

    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ParametersIndentationViolation])
