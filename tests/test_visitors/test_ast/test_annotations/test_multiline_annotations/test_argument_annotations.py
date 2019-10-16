# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.annotations import (
    MultilineFunctionAnnotationViolation,
    WrongAnnotationVisitor,
)

# Correct:

correct_function_without_arguments = """
def function(): ...
"""

correct_function_without_annotations = """
def function(arg, arg1, arg2): ...
"""

correct_simple_argument = """
def function(arg: int): ...
"""

correct_compound_argument = """
def function(arg: Optional[int]): ...
"""

correct_multiline_arguments = """
def function(
    arg1: str,
    arg2: Optional[Union[int, str]],
): ...
"""

# Wrong:

wrong_multiline_arguments = """
def function(
    arg: Optional[
        int,
    ],
): ...
"""

wrong_multiline_tuple = """
def function(
    arg: Tuple[
        int,
        int,
    ],
): ...
"""


@pytest.mark.parametrize('code', [
    wrong_multiline_arguments,
    wrong_multiline_tuple,
])
def test_wrong_argument_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that using incorrect argument annotations is forbiden."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultilineFunctionAnnotationViolation])


@pytest.mark.parametrize('code', [
    correct_function_without_arguments,
    correct_function_without_annotations,
    correct_simple_argument,
    correct_compound_argument,
    correct_multiline_arguments,
])
def test_correct_argument_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that it is possible to use correct type annotations."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
