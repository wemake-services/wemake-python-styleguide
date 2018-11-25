# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.statements import (
    ParametersIndentationViolation,
    WrongParametersIndentationVisitor,
)

# Correct:

correct_single_line_class = 'class Test(First, Second, Third): ...'
correct_multi_line_class = """
class Test(
    First,
    Second,
    Third,
): ...
"""

correct_multi_line_class_with_keywords = """
class Test(
    First,
    Second,
    Third,
    keyword=True,
): ...
"""

correct_next_line_class = """
class Test(
    First, Second, Third,
): ...
"""


# Wrong:

wrong_class_indentation1 = """
class Test(First,
           Second, Third): ...
"""

wrong_class_indentation2 = """
class Test(First, Second,
           Third): ...
"""

wrong_class_indentation3 = """
class Test(
    First, Second,
    Third,
): ...
"""

wrong_class_indentation4 = """
class Test(
    First,
    Second, Third,
): ...
"""

wrong_class_indentation5 = """
class Test(
    First,
    Second,
    Third, keyword=True,
): ...
"""

wrong_class_indentation6 = """
class Test(
    First,
    Second, Third, keyword=True,
): ...
"""


@pytest.mark.parametrize('code', [
    correct_single_line_class,
    correct_multi_line_class,
    correct_multi_line_class_with_keywords,
    correct_next_line_class,
])
def test_correct_class_indentation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correctly indented base classes work."""
    tree = parse_ast_tree(code)

    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_class_indentation1,
    wrong_class_indentation2,
    wrong_class_indentation3,
    wrong_class_indentation4,
    wrong_class_indentation5,
    wrong_class_indentation6,
])
def test_wrong_class_indentation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that poorly indented classes do not work."""
    tree = parse_ast_tree(code)

    visitor = WrongParametersIndentationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ParametersIndentationViolation])
