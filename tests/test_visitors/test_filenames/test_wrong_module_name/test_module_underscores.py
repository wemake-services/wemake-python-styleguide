# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    WrongModuleNameUnderscoresViolation,
)
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
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
    '__compat.py',
    'some__typo.py',
])
def test_length_option(assert_errors, filename, default_options):
    """Ensures incorrect underscores are caught."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [WrongModuleNameUnderscoresViolation])
