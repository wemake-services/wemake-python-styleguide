# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.annotations import (
    LiteralNoneViolation,
    MultilineFunctionAnnotationViolation,
    WrongAnnotationVisitor,
)

# Correct:

correct_function_without_annotations = """
def function(): ...
"""

correct_simple_return = """
def function() -> int: ...
"""

correct_compound_return = """
def function() -> Optional[int]: ...
"""

correct_multiline_return = """
def function(
    arg1,
) -> Optional[Union[int, str]]: ...
"""

correct_return_none_annotation = """
def function(arg) -> None: ...
"""

correct_embedded_return_none_annotation = """
def function(arg) -> Union[None, Optional[int]]: ...
"""

# Wrong:

wrong_embedded_return_none_annotation = """
def function(arg) -> Union[Literal[None], Optional[int]]: ...
"""

wrong_return_none_annotation = """
def function(arg) -> Literal[None]: ...
"""

wrong_multiline_return1 = """
def function(
    arg
) -> Optional[
    Union[int, str]
]: ...
"""

wrong_multiline_return2 = """
def function(
    arg
) -> Optional[
    Union[
        int, str,
    ]
]: ...
"""

wrong_multiline_return3 = """
def function(
    arg
) -> Optional[
    Union[
        int,
        str,
    ]
]: ...
"""


@pytest.mark.parametrize('code', [
    wrong_multiline_return1,
    wrong_multiline_return2,
    wrong_multiline_return3,
])
def test_wrong_return_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that using incorrect return annotations is forbiden."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultilineFunctionAnnotationViolation])


@pytest.mark.parametrize('code', [
    wrong_embedded_return_none_annotation,
    wrong_return_none_annotation,
])
def test_wrong_literal_none_return_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that using incorrect return annotations is forbiden."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LiteralNoneViolation])


@pytest.mark.parametrize('code', [
    correct_function_without_annotations,
    correct_simple_return,
    correct_compound_return,
    correct_multiline_return,
    correct_embedded_return_none_annotation,
    correct_return_none_annotation,
])
def test_correct_return_annotation(
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
