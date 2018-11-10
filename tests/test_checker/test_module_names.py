# -*- coding: utf-8 -*-

import ast

import pytest

from wemake_python_styleguide.checker import Checker
from wemake_python_styleguide.violations import naming


@pytest.mark.parametrize('filename, error', [
    ('__magic__.py', naming.WrongModuleMagicNameViolation),
    ('util.py', naming.WrongModuleNameViolation),
    ('x.py', naming.TooShortNameViolation),
    ('test__name.py', naming.ConsecutiveUnderscoresInNameViolation),
    ('123py.py', naming.WrongModuleNamePatternViolation),
    ('version_1.py', naming.UnderscoredNumberNameViolation),
    ('__private.py', naming.PrivateNameViolation),
    (
        'oh_no_not_an_extremely_super_duper_unreasonably_long_name.py',
        naming.TooLongNameViolation,
    ),
    ('привет', naming.UnicodeNameViolation),
])
def test_module_names(filename, error, default_options):
    """Ensures that checker works with module names."""
    module = ast.parse('')
    Checker.parse_options(default_options)
    checker = Checker(tree=module, file_tokens=[], filename=filename)
    _, _, error_text, _ = next(checker.run())
    error_code = int(error_text[1:4])

    assert error_code == error.code
