# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from wemake_python_styleguide.violations.best_practices import (
    ExecutableMismatchViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import ShebangVisitor

RESOURCES_FOLDER = 'test_valid_shebang_resources'
_python_files_folder = Path(__file__).absolute().parent / RESOURCES_FOLDER


@pytest.mark.parametrize('error_code', [
    'exe001',
    'exe002',
    'exe003',
    'exe004',
    'exe005',
])
def test_exe_negative(
    assert_errors,
    parse_tokens,
    default_options,
    error_code,
):
    """Testing cases when no errors should be reported."""
    filename = _python_files_folder / ''.join([error_code, '_neg.py'])
    with open(filename, 'r', encoding='utf-8') as test_file:
        file_content = test_file.read()
        file_tokens = parse_tokens(file_content)
        visitor = ShebangVisitor(
            default_options,
            filename=filename,
            file_tokens=file_tokens,
        )
        visitor.run()
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
    parse_tokens,
    default_options,
    error_code,
):
    """Testing cases when errors should be reported."""
    filename = _python_files_folder / ''.join([error_code, '_pos.py'])
    with open(filename, 'r', encoding='utf-8') as test_file:
        file_content = test_file.read()
        file_tokens = parse_tokens(file_content)
        visitor = ShebangVisitor(
            default_options,
            filename=filename,
            file_tokens=file_tokens,
        )
        visitor.run()
        assert_errors(visitor, [ExecutableMismatchViolation])
