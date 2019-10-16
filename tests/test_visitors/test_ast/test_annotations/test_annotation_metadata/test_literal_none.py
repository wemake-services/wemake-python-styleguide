# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.annotations import (
    LiteralNoneViolation,
)
from wemake_python_styleguide.visitors.ast.annotations import (
    SemanticAnnotationVisitor,
)


@pytest.mark.parametrize('code', [
    'Literal[None]',
    'typing.Literal[None]',
    'typing_extensions.Literal[None]',
])
def test_wrong_literal_none(
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

    assert_errors(visitor, [LiteralNoneViolation])


@pytest.mark.parametrize('code', [
    'Literal["a"]',
    'Literal[True]',
    'Literal[False]',
    'Literal[1]',

    'typing.Literal[1]',
    'typing_extensions.Literal[True]',
])
def test_correct_literal(
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
