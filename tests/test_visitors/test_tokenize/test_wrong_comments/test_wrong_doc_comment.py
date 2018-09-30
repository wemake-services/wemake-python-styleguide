# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.errors.best_practices import (
    WrongDocCommentViolation,
)
from wemake_python_styleguide.visitors.tokenize.wrong_comments import (
    WrongCommentVisitor,
)

constant_doc = """
#: {0}
SOME_CONSTANT = 12
"""

attribute_doc = """
class SomeClass(object):
    #: {0}
    some_field = 'text'
"""


@pytest.mark.parametrize('code', [
    constant_doc,
    attribute_doc,
])
@pytest.mark.parametrize('comment', [
    'non empty text',
    'text with :',
])
def test_correct_comments(
    parse_tokens,
    assert_errors,
    default_options,
    code,
    comment,
):
    """Ensures that correct comments do not raise a warning."""
    file_tokens = parse_tokens(code.format(comment))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    constant_doc,
    attribute_doc,
])
@pytest.mark.parametrize('comment', [
    '',
    ' ',
    '    ',
])
def test_incorrect_doc_comment(
    parse_tokens,
    assert_errors,
    default_options,
    code,
    comment,
):
    """Ensures that incorrect doc comments raise a warning."""
    file_tokens = parse_tokens(code.format(comment))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongDocCommentViolation])
