# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.constants import MODULE_NAMES_BLACKLIST
from wemake_python_styleguide.violations.naming import WrongModuleNameViolation
from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'query.py',
    '/home/user/logic.py',
    'partial/views.py',
    'C:/path/package/module.py',
])
def test_simple_filename(assert_errors, filename, default_options):
    """Testing that simple file names works well."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('filename', MODULE_NAMES_BLACKLIST)
def test_restricted_filename(
    assert_errors,
    filename,
    default_options,
):
    """Testing that some file names are restricted."""
    visitor = WrongModuleNameVisitor(
        default_options,
        filename='{0}.py'.format(filename),
    )
    visitor.run()

    assert_errors(visitor, [WrongModuleNameViolation])
