# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    ConsecutiveUnderscoresInNameViolation,
    PrivateNameViolation,
)
from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'some.py',
    'my_module.py',
    '__init__.py',
    '_compat.py',
])
def test_correct_filename(assert_errors, filename, default_options):
    """Testing that correct file names are allowed."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('filename', [
    'compat__.py',
    'some__typo.py',
])
def test_underscore_filename(
    assert_errors,
    assert_error_text,
    filename,
    default_options,
):
    """Ensures incorrect underscores are caught."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [ConsecutiveUnderscoresInNameViolation])
    assert_error_text(visitor, filename.replace('.py', ''))


@pytest.mark.parametrize('filename', [
    '__private.py',
    '__compat_name.py',
])
def test_private_filename(
    assert_errors,
    assert_error_text,
    filename,
    default_options,
):
    """Ensures that names with private names are caught."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [PrivateNameViolation])
    assert_error_text(visitor, filename.replace('.py', ''))
