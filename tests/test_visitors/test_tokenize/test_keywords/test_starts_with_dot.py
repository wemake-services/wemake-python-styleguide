# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    LineStartsWithDotViolation,
)
from wemake_python_styleguide.visitors.tokenize.keywords import (
    WrongKeywordTokenVisitor,
)

# Correct:

correct_dot_attr = """
some_line = some.attr(
    some.other,
)
"""

correct_elipsis = """
first[
    1,
    ...,
]
"""

correct_string_dot = '".start!"'

# Wrong:

wrong_dot_start1 = """
some = (
    MyModel.objects.filter(some=1)
        .exclude(other=2)
)
"""

wrong_dot_start2 = """
some = (
    MyModel.objects.filter(some=1)
.exclude(other=2)
)
"""


@pytest.mark.parametrize('code', [
    wrong_dot_start1,
    wrong_dot_start2,
])
def test_wrong_dot_start(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that lines cannot be started with ``.`` char."""
    file_tokens = parse_tokens(code)

    visitor = WrongKeywordTokenVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [LineStartsWithDotViolation])


@pytest.mark.parametrize('code', [
    correct_dot_attr,
    correct_elipsis,
    correct_string_dot,
])
def test_correct_dot_start(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that lines can be started with other chars."""
    file_tokens = parse_tokens(code)

    visitor = WrongKeywordTokenVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])
