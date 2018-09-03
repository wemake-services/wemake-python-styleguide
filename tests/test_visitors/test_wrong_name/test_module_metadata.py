# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_name import (
    BAD_MODULE_METADATA_VARIABLES,
    WrongModuleMetadataViolation,
    WrongModuleMetadataVisitor,
)

module_metadata = """
{0} = 'Nikita'
"""

nested_metadata = """
class ORM:
    {0} = None
"""

startup_metadata = """
if __name__ == '__main__':
    main()
"""


@pytest.mark.parametrize('bad_name', BAD_MODULE_METADATA_VARIABLES)
@pytest.mark.parametrize('code', [
    module_metadata,
])
def test_wrong_metadata(
    assert_errors, parse_ast_tree, bad_name, code, default_options,
):
    """Testing that metadata can not have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visiter = WrongModuleMetadataVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [WrongModuleMetadataViolation])


@pytest.mark.parametrize('correct_name', [
    'correct_name',
    'xy',
    '_value',
])
@pytest.mark.parametrize('code', [
    module_metadata,
    nested_metadata,
])
def test_correct_metadata(
    assert_errors, parse_ast_tree, code, correct_name, default_options,
):
    """Testing that metadata can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visiter = WrongModuleMetadataVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])


def test_correct_startup_metadata(
    assert_errors, parse_ast_tree, default_options,
):
    """Testing that startup hook is allowed."""
    tree = parse_ast_tree(startup_metadata)

    visiter = WrongModuleMetadataVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])
