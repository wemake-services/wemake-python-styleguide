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

correct_literal_annotation = """
def function(arg: Literal[True]) -> Literal["foo"]: ...
"""

correct_arg_none_annotation = """
def function(empty_arg: None): ...
"""

correct_unnested_literal_annotation = """
def function(arg: Literal[1, 2, 3]): ...
"""

correct_unnested_union_annotation = """
def function(arg: Union[int, str, float]): ...
"""

correct_unnested_combined_annotation = """
def function(arg: Union[str, Literal[1]]): ...
"""

correct_unnested_annotated_annotation = """
def function(arg: Annotated[int]): ...
"""

correct_unnested_prefixed_literal_annotation = """
def function(arg: typing.Literal[1, 2, 3]): ...
"""

correct_unnested_combined_prefixed_annotation = """
def function(arg: typing.Union[Literal[1]]): ...
"""

correct_arg_union_none_annotation = """
def function(empty_arg: Union[int, float, None]): ...
"""

correct_arg_embedded_union_none_annotation = """
def function(empty_arg: Union[Union[int, float, None], float]): ...
"""

correct_arg_union_annotation = """
def function(empty_arg: Union[True, float]): ...
"""

correct_arg_union_annotation_one_argument = """
def function(empty_arg: Union[float]): ...
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

wrong_arg_none_annotation = """
def function(empty_arg: Literal[None]): ...
"""

wrong_embedded_arg_none_annotation = """
def function(empty_arg: Union[Literal[None], Optional[int]]): ...
"""

wrong_nested_literal_annotation = """
def function(arg: Literal[Literal[1, 2], 3]): ...
"""

wrong_nested_union_annotation = """
def function(arg: Union[Union[int, str], float]): ...
"""

wrong_nested_annotated_annotation = """
def function(arg: Annotated[Annotated[int, str], float]): ...
"""

wrong_deep_nested_literal_annotation = """
def function(arg: Literal[Literal[Literal[1]]]): ...
"""

wrong_deep_nested_union_annotation = """
def function(arg: Union[Union[Union[int]]]): ...
"""

wrong_deep_nested_annotated_annotation = """
def function(arg: Annotated[Annotated[Annotated[int]]]): ...
"""

wrong_nested_prefixed_literal_annotation = """
def function(arg: typing.Literal[typing.Literal[1]]): ...
"""

wrong_deep_nested_prefixed_literal_annotation = """
def function(arg: typing.Literal[typing.Literal[typing.Literal[1]]]): ...
"""

wrong_nested_combined_annotation = """
def function(arg: typing.Union[Union[int], str]): ...
"""

wrong_arg_union_with_none_annotation = """
def function(empty_arg: Union[int, None]): ...
"""

wrong_embedded_arg_union_with_none_annotation = """
def function(empty_arg: Union[Union[int, None], Optional[int]]): ...
"""


@pytest.mark.parametrize('code', [
    wrong_nested_literal_annotation,
    wrong_nested_union_annotation,
    wrong_nested_annotated_annotation,
    wrong_nested_combined_annotation,
    wrong_nested_prefixed_literal_annotation,
])
def test_forbidden_nested_annotations(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that using nested ``Literal`` and ``Union`` is forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongNestedAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedAnnotationsViolation])


@pytest.mark.parametrize('code', [
    wrong_deep_nested_literal_annotation,
    wrong_deep_nested_union_annotation,
    wrong_deep_nested_annotated_annotation,
    wrong_deep_nested_prefixed_literal_annotation,
])
def test_forbidden_deep_nested_annotations(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that using nested ``Literal`` and ``Union`` is forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongNestedAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        NestedAnnotationsViolation,
        NestedAnnotationsViolation,
    ])


@pytest.mark.parametrize('code', [
    wrong_arg_none_annotation,
    wrong_embedded_arg_none_annotation,
])
def test_forbidden_literal_none_annotation(
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

    assert_errors(visitor, [LiteralNoneViolation])


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
    correct_arg_none_annotation,
    correct_literal_annotation,
    correct_arg_union_none_annotation,
    correct_arg_embedded_union_none_annotation,
    correct_arg_union_annotation,
    correct_arg_union_annotation_one_argument,
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


@pytest.mark.parametrize('code', [
    correct_unnested_union_annotation,
    correct_unnested_literal_annotation,
    correct_unnested_annotated_annotation,
    correct_unnested_combined_annotation,
    correct_unnested_prefixed_literal_annotation,
    correct_unnested_combined_prefixed_annotation,
])
def test_correct_unnested_argument_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that it is possible to use correct type annotations."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongNestedAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_arg_union_with_none_annotation,
    wrong_embedded_arg_union_with_none_annotation,
])
def test_wrong_union_none_annotation(
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

    assert_errors(visitor, [UnionNoneViolation])
