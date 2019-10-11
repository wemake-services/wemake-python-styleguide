# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.annotations import (
    LiteralNoneViolation,
    MultilineFunctionAnnotationViolation,
    NestedAnnotationsViolation,
    UnionNoneViolation,
    WrongAnnotationVisitor,
    WrongNestedAnnotationVisitor,
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
def function(arg) -> Union[None, Optional[int], Optional[float]]: ...
"""

correct_unnested_literal_return = """
def function() -> Literal[1, 2, 3]: ...
"""

correct_unnested_union_return = """
def function() -> Union[int, str, float]: ...
"""

correct_unnested_annotated_return = """
def function() -> Annotated[int, str, float]: ...
"""

correct_unnested_prefixed_literal_return = """
def function() -> typing.Literal[1, 2, 3]: ...
"""

correct_unnested_combined_literal_return = """
def function() -> Union[typing.Literal[2, 3], int]: ...
"""

correct_union_with_none_return = """
def function() -> Union[int, float, None]: ...
"""

correct_embedded_union_with_none_return = """
def function() -> Union[Union[int, float, None], float]: ...
"""

correct_union_return = """
def function() -> Union[True, float]: ...
"""

correct_union_return_one_argument = """
def function() -> Union[int]: ...
"""

# Wrong:

wrong_nested_literal_return = """
def function() -> Literal[Literal[1, 2], 3]: ...
"""

wrong_nested_union_return = """
def function() -> Union[Union[int, str], float]: ...
"""

wrong_nested_annotated_return = """
def function() -> Annotated[Annotated[int, str], float]: ...
"""

wrong_deep_nested_annotated_return = """
def function() -> Annotated[Annotated[Annotated[int]]]: ...
"""

wrong_deep_nested_literal_return = """
def function() -> Literal[Literal[Literal[1]]]: ...
"""

wrong_deep_nested_union_return = """
def function() -> Union[Union[Union[int]]]: ...
"""

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

wrong_nested_prefixed_literal_return = """
def function() -> typing.Literal[typing.Literal[1]]: ...
"""

wrong_deep_nested_prefixed_literal_return = """
def function() -> typing.Literal[typing.Literal[typing.Literal[1]]]: ...
"""

wrong_nested_combined_union_return = """
def function() -> typing.Union[Union[1]]: ...
"""

wrong_union_with_none_return = """
def function() -> Union[None, int]: ...
"""

wrong_embedded_union_with_none_return = """
def function() -> Union[Union[None, int], float]: ...
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
    wrong_nested_literal_return,
    wrong_nested_union_return,
    wrong_nested_prefixed_literal_return,
    wrong_nested_combined_union_return,
    wrong_nested_annotated_return,
])
def test_wrong_nested_return_annotations(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that nested return ``Literal`` and ``Union`` is forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongNestedAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedAnnotationsViolation])


@pytest.mark.parametrize('code', [
    wrong_deep_nested_literal_return,
    wrong_deep_nested_union_return,
    wrong_deep_nested_annotated_return,
    wrong_deep_nested_prefixed_literal_return,
])
def test_wrong_deep_nested_return_annotations(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that nested return ``Literal`` and ``Union`` is forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongNestedAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        NestedAnnotationsViolation,
        NestedAnnotationsViolation,
    ])


@pytest.mark.parametrize('code', [
    correct_function_without_annotations,
    correct_simple_return,
    correct_compound_return,
    correct_multiline_return,
    correct_embedded_return_none_annotation,
    correct_return_none_annotation,
    correct_union_with_none_return,
    correct_embedded_union_with_none_return,
    correct_union_return,
    correct_union_return_one_argument,
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


@pytest.mark.parametrize('code', [
    correct_unnested_literal_return,
    correct_unnested_union_return,
    correct_unnested_annotated_return,
    correct_unnested_prefixed_literal_return,
])
def test_correct_unnested_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that it is possible to use correct unnested annotations."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongNestedAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_union_with_none_return,
    wrong_embedded_union_with_none_return,
])
def test_wrong_union_with_none_return_annotation(
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

    assert_errors(visitor, [UnionNoneViolation])
