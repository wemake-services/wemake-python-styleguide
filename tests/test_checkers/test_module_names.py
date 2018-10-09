# -*- coding: utf-8 -*-

import ast

import pytest

from wemake_python_styleguide.checker import Checker
from wemake_python_styleguide.violations import naming


@pytest.mark.parametrize('filename, error', [
    ('__magic__.py', naming.WrongModuleMagicNameViolation),
    ('util.py', naming.WrongModuleNameViolation),
    ('x.py', naming.TooShortModuleNameViolation),
    ('test__name.py', naming.WrongModuleNameUnderscoresViolation),
    ('123py.py', naming.WrongModuleNamePatternViolation),
    ('version_1.py', naming.UnderScoredNumberNameViolation),
])
def test_module_names(filename, error):
    """Ensures that checker works with module names."""
    module = ast.parse('')
    checker = Checker(tree=module, file_tokens=[], filename=filename)
    _, _, error_text, _ = next(checker.run())
    error_code = int(error_text[1:4])

    assert error_code == error.code
