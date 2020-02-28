# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ExecutableMismatchViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import ShebangVisitor

SHEBANG_RESOURCES_FOLDER = 'test_executable_mismatch_resources'
TESTS_FOLDER = Path(__file__).absolute().parent.parent.parent.parent
RESOURCES_FULL_PATH = TESTS_FOLDER / 'fixtures' / SHEBANG_RESOURCES_FOLDER


@pytest.mark.parametrize('error_code', [
    'exe001',
    'exe002',
    'exe003',
    'exe004',
    'exe005',
])
def test_exe_negative(
    assert_errors,
    parse_file_tokens,
    default_options,
    error_code,
):
    """Testing cases when no errors should be reported."""
    filename = RESOURCES_FULL_PATH / ''.join([error_code, '_neg.py'])
    file_tokens = parse_file_tokens(filename)
    visitor = ShebangVisitor(
        default_options,
        filename=filename,
        file_tokens=file_tokens,
    )
    assert_errors(visitor, [])


@pytest.mark.parametrize('error_code', [
    'exe001',
    'exe002',
    'exe003',
    'exe004',
    'exe005',
])
def test_exe_positive(
    assert_errors,
    parse_file_tokens,
    default_options,
    error_code,
):
    """Testing cases when errors should be reported."""
    filename = RESOURCES_FULL_PATH / ''.join([error_code, '_pos.py'])
    file_tokens = parse_file_tokens(filename)
    visitor = ShebangVisitor(
        default_options,
        filename=filename,
        file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [ExecutableMismatchViolation])
