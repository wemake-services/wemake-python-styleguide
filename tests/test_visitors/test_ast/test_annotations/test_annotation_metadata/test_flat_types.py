# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.annotations import (
    NestedAnnotationsViolation,
)
from wemake_python_styleguide.visitors.ast.annotations import (
    SemanticAnnotationVisitor,
    UnionNestedInOptionalViolation,
)


@pytest.mark.parametrize('code', [
    # Literal:
    'Literal[Literal[1]]',
    'Literal[typing.Literal[1]]',
    'Literal[typing_extensions.Literal[1]]',

    'typing.Literal[Literal[1]]',
    'typing.Literal[typing.Literal[1]]',
    'typing.Literal[typing_extensions.Literal[1]]',

    'typing_extensions.Literal[Literal[1]]',
    'typing_extensions.Literal[typing.Literal[1]]',
    'typing_extensions.Literal[typing_extensions.Literal[1]]',

    # Union:
    'Union[Union[str, int], bool]',
    'Union[typing.Union[str, int], bool]',
    'Union[typing_extensions.Union[str, int], bool]',

    'typing.Union[Union[str, int], bool]',
    'typing.Union[typing.Union[str, int], bool]',
    'typing.Union[typing_extensions.Union[str, int], bool]',

    'typing_extensions.Union[Union[str, int], bool]',
    'typing_extensions.Union[typing.Union[str, int], bool]',
    'typing_extensions.Union[typing_extensions.Union[str, int], bool]',

    # Annotated:
    'Annotated[Annotated[int], ...]',
    'Annotated[typing.Annotated[int], ...]',
    'Annotated[typing_extensions.Annotated[int], ...]',

    'typing.Annotated[Annotated[int], ...]',
    'typing.Annotated[typing.Annotated[int], ...]',
    'typing.Annotated[typing_extensions.Annotated[int], ...]',

    'typing_extensions.Annotated[Annotated[int], ...]',
    'typing_extensions.Annotated[typing.Annotated[int], ...]',
    'typing_extensions.Annotated[typing_extensions.Annotated[int], ...]',
])
def test_wrong_nested_annotation(
    assert_errors,
    parse_ast_tree,
    code,
    annotation_template,
    default_options,
    mode,
):
    """Ensures that using incorrect annotations is forbiden."""
    tree = parse_ast_tree(mode(annotation_template.format(code)))

    visitor = SemanticAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedAnnotationsViolation])


@pytest.mark.parametrize('code', [
    # Literal:
    'Literal["a"]',
    'List[Literal["a"]]',
    'typing.Literal["a"]',
    'List[typing.Literal["a"]]',
    'typing_extensions.Literal["a"]',
    'List[typing_extensions.Literal["a"]]',

    # Union:
    'Union[str, int, bool]',
    'typing.Union[List[str], int, bool]',
    'typing_extensions.Union[str, int]',

    # Annotated:
    'Annotated[int, ...]',
    'typing.Annotated[int, str]',
    'typing_extensions.Annotated[int, "Metadata"]',
])
def test_correct_nested_annotations(
    assert_errors,
    parse_ast_tree,
    code,
    annotation_template,
    default_options,
    mode,
):
    """Ensures that using correct annotations is ok."""
    tree = parse_ast_tree(mode(annotation_template.format(code)))

    visitor = SemanticAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'Optional[Union[int, str]]',
    'Optional[Optional[Optional[Union[int, str]]]]',
    'typing.Optional[typing.Union[int, float]]',
    'typing.Optional[typing.Optional[typing.Optional[typing.Union[int, str]]]]',
])
def test_wrong_union_nested_in_optional(
    assert_errors,
    parse_ast_tree,
    code,
    annotation_template,
    default_options,
    mode,
):
    """Ensures that `Union` nested in `Optional` annotations are forbidden."""
    tree = parse_ast_tree(mode(annotation_template.format(code)))

    visitor = SemanticAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnionNestedInOptionalViolation])


@pytest.mark.parametrize('code', [
    'Optional[str]',
    'typing.Optional[int]',
    'Union[int, str, None]',
    'typing.Union[int, float, None]',
    'Optional[Any]',
])
def test_correct_optional_without_nested_union(
    assert_errors,
    parse_ast_tree,
    code,
    annotation_template,
    default_options,
    mode,
):
    """Ensures that `Optional` without nested `Union` is ok."""
    tree = parse_ast_tree(mode(annotation_template.format(code)))

    visitor = SemanticAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
