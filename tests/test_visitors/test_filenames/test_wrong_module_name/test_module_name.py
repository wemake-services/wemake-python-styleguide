# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import BAD_MODULE_NAMES
from wemake_python_styleguide.errors.naming import WrongModuleNameViolation
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'query.py',
    '/home/user/logics.py',
    'partial/views.py',
    'C:/path/package/module.py',
])
def test_simple_filename(assert_errors, filename, default_options):
    """Testing that simple file names works well."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('filename', BAD_MODULE_NAMES)
def test_restricted_filename(assert_errors, filename, default_options):
    """Testing that some file names are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename + '.py')
    visitor.run()

    assert_errors(visitor, [WrongModuleNameViolation])
