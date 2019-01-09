# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    EmptyLineAfterCodingViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import (
    FileMagicCommentsVisitor,
)

# Correct:

empty_module = ''
empty_module_with_coding = """# -*- coding: utf-8 -*-

"""

nonempty_module_with_coding = """# -*- coding: utf-8 -*-

SOME_VAR = 1
"""

nonempty_module = 'SOME_VAR = 1'

nonempty_module_with_multiple_comments = """#!/usr/bin/python
# -*- coding: utf-8 -*-
# This comment is for testing

SOME_VAR = 1
"""

# Wrong:

wrong_module_with_coding = """# -*- coding: utf-8 -*-
SOME_VAR = 1
"""


@pytest.mark.parametrize('code', [
    empty_module,
    empty_module_with_coding,
    nonempty_module_with_coding,
    nonempty_module,
    nonempty_module_with_multiple_comments,
])
def test_correct_comments(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct comments do not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = FileMagicCommentsVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_module_with_coding,
])
def test_incorrect_coding_comment(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that incorrect `coding` comments raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = FileMagicCommentsVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [EmptyLineAfterCodingViolation])
