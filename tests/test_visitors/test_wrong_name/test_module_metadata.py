# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_name import (
    BAD_MODULE_METADATA_VARIABLES,
    WrongModuleMetadataViolation,
    WrongModuleMetadataVisitor,
)

module_test = """
{0} = 'Nikita'
"""

nested_test = """
class ORM:
    {0} = None
"""


@pytest.mark.parametrize('bad_name', BAD_MODULE_METADATA_VARIABLES)
@pytest.mark.parametrize('code', [
    module_test,
])
def test_wrong_metadata(
    assert_errors, parse_ast_tree, bad_name, code,
):
    """Testing that metadata can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visiter = WrongModuleMetadataVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [WrongModuleMetadataViolation])


@pytest.mark.parametrize('correct_name', ['correct_name', 'xy', '_value'])
@pytest.mark.parametrize('code', [
    module_test,
    nested_test,
])
def test_correct_metadata(
    assert_errors, parse_ast_tree, code, correct_name,
):
    """Testing that metadata can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visiter = WrongModuleMetadataVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])
