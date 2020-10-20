import pytest

from wemake_python_styleguide.violations.consistency import (
    FormattedStringViolation,
    ModuloStringFormatViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import WrongStringVisitor

_PREFIXES = (
    '',
    'b',
    'u',
    'r',
    'rb',
    'f',
    'fr',
)

# Docstring samples:

docstring_module = "'docstring with %s'"
docstring_function = """
def test():
    '''Docstring with %f.'''
"""

docstring_class = """
class Test(object):
    '''Docstring with %d.'''
"""

docstring_method = """
class Test(object):
    def method(self):
        '''Docstring with %(named)s.'''
"""


@pytest.mark.parametrize('code', [
    # All examples are copied from https://pyformat.info/
    '%10s',
    '%-10s',
    '%.5s',
    '%-10.5s',
    '%4d',
    '%06.2f',
    '%04d',
    '%+d',
    '%.*s',
    '%*.*f',

    # Our own examples:
    '%%',
    '%#d',
    '%0d',
    '%0*d',
    '%0*hd',
    '%0*Li',
    '%0*li',

    '%(first)s',
    '%(f1_abc)+d',
    '%d-%m-%Y (%H:%M:%S)',

    '%d',
    '%i',
    '%o',
    '%u',
    '%x',
    '%X',
    '%e',
    '%E',
    '%f',
    '%F',
    '%g',
    '%G',
    '%c',
    '%r',
    '%s',
    '%a',
])
@pytest.mark.parametrize('prefix', _PREFIXES)
def test_modulo_formatting(
    assert_errors,
    parse_ast_tree,
    code,
    prefix,
    default_options,
):
    """Testing that the strings violate the rules."""
    tree = parse_ast_tree('x = {0}"{1}"'.format(prefix, code))

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ModuloStringFormatViolation], (
        FormattedStringViolation,
    ))


@pytest.mark.parametrize('code', [
    '% d',  # technically it is a format string, however we allow ` ` inside
    '99.9% of cases',  # spaces should not cause errors
    '%10',
    '10%',
    '1%0',
    'some % name',
    '%l',
    '%@',
    '%.',
    '%+',
    '%_%',
    '\%\%',  # noqa: W605
    '%\d',  # noqa: W605
    '%[prefix]s',
    '%(invalid@name)s',
    '%(also-invalid)d',
    '',
    'regular string',
    'some%value',
    'some % value',
    'some %value',
    'some% value',
    'to format: {0}',
    'named {format}',
    '%t',
    '%y',
    '%m-%Y (%H:%M:%S)',
])
@pytest.mark.parametrize('prefix', _PREFIXES)
def test_regular_modulo_string(
    assert_errors,
    parse_ast_tree,
    code,
    prefix,
    default_options,
):
    """Testing that the strings violate the rules."""
    tree = parse_ast_tree('x = {0}"{1}"'.format(prefix, code))

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], (FormattedStringViolation,))


@pytest.mark.parametrize('code', [
    'x % 1',
    '"str" % 1',
    'name % value',
    '1 % name',
    '"a" % "b"',
])
def test_modulo_operations(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that the modulo operations are not affected."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    docstring_module,
    docstring_function,
    docstring_class,
    docstring_method,
])
def test_docstring_modulo_operations(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that the docstrings are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
