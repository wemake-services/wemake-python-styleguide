import pytest

from wemake_python_styleguide.constants import (
    MODULE_METADATA_VARIABLES_BLACKLIST,
)
from wemake_python_styleguide.violations.best_practices import (
    WrongModuleMetadataViolation,
)
from wemake_python_styleguide.visitors.ast.naming.variables import (
    WrongModuleMetadataVisitor,
)

module_metadata = """
{0} = 'Nikita'
"""

module_type_metadata = """
{0}: str = 'Nikita'
"""

nested_metadata = """
class ORM:
    {0} = None
"""

startup_metadata = """
if __name__ == '__main__':
    main()
"""


@pytest.mark.parametrize('bad_name', MODULE_METADATA_VARIABLES_BLACKLIST)
@pytest.mark.parametrize(
    'code',
    [
        module_metadata,
        module_type_metadata,
    ],
)
def test_wrong_metadata(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    bad_name,
    code,
    default_options,
):
    """Testing that metadata cannot have blacklisted names."""
    tree = parse_ast_tree(code.format(bad_name))

    visitor = WrongModuleMetadataVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongModuleMetadataViolation])
    assert_error_text(visitor, bad_name)


@pytest.mark.parametrize(
    'correct_name',
    [
        'correct_name',
        'xy',
        '_value',
    ],
)
@pytest.mark.parametrize(
    'code',
    [
        module_metadata,
        module_type_metadata,
        nested_metadata,
    ],
)
def test_correct_metadata(
    assert_errors,
    parse_ast_tree,
    code,
    correct_name,
    default_options,
):
    """Testing that metadata can have normal names."""
    tree = parse_ast_tree(code.format(correct_name))

    visitor = WrongModuleMetadataVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


def test_correct_startup_metadata(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that startup hook is allowed."""
    tree = parse_ast_tree(startup_metadata)

    visitor = WrongModuleMetadataVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        module_metadata,
        module_type_metadata,
    ],
)
def test_module_metadata_allowed_list(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that configuration with allowed module has the priority."""
    option_values = options(
        forbidden_module_metadata=('__all__', '__author__'),
        allowed_module_metadata=('__all__',),
    )
    tree = parse_ast_tree(code.format('__all__'))

    visitor = WrongModuleMetadataVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        module_metadata,
        module_type_metadata,
    ],
)
def test_module_metadata_forbidden_list(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that startup hook is allowed."""
    option_values = options(forbidden_module_metadata=('custom',))
    for metadata_value in ('__all__', 'custom'):
        tree = parse_ast_tree(code.format(metadata_value))

        visitor = WrongModuleMetadataVisitor(option_values, tree=tree)
        visitor.run()

        assert_errors(visitor, [WrongModuleMetadataViolation])
