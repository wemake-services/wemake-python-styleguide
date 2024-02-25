"""Test method contain only allowed empty lines count."""
import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongEmptyLinesCountViolation,
)
from wemake_python_styleguide.visitors.ast.function_empty_lines import (
    WrongEmptyLinesCountVisitor,
)

class_with_wrong_method = """
class WrongClass(object):

    def wrong_method(self):
        foo()

        bar()

        baz()

        lighter()
"""

class_with_valid_method = """
class WrongClass(object):

    def wrong_method(self):
        foo()
        bar()
        baz()
"""

file_with_few_class = """
class ValidClass(object):

    def valid_method(self):
        foo()
        bar()
        baz()

    def very_valid_method(self):
        foo()
        bar()


class EmptyError(Exception):

    message = 'fail'
"""

wrong_function = """
def func():
    foo()

    a = 1 + 4

    bar()

    baz()
"""

wrong_function_with_loop = """
def func():
    for x in range(10):

        requests.get(


            'https://github.com/wemake-services/wemake-python-styleguide'
        )
"""

allow_function = """
def func():
    foo()
    if name == 'Moonflower':
        print('Love')

    baz()
"""

allow_function_with_comments = """
def test_func():
   # This function
   #
   # has lots
   #
   # of empty
   #
   # lines
   #
   # in comments
   return 0
"""

function_with_docstring = """
def test_func():
   \"""
   Its docstring

   has many new lines

   but this is

   totally fine

   we don't raise a violation for this
   \"""
   return
"""

function_with_docstring_and_comments = """
def test_func():
   \"""
   Its docstring

   has many new lines

   but this is

   totally fine

   we don't raise a violation for this
   \"""
   # This function
   #
   # has lots
   #
   # of empty
   #
   # lines
   #
   # in comments
   return 0
"""


class_with_attributes = """
class Foo(object):
    first_attribute = 'foo'




    second_attribute = 'bar'
"""

expression_without_function = """
print(
    'Contributing in WPS',




    'is a lot of fun',
)
"""

module_level_empty_lines = """
fstrings_feature = Fstring()





fstrings_feature.deprecate()
"""

def_with_ellipsis = """
class BaseResponse(Protocol):

    @property
    def status_code(self) -> int: ...

    @property
    def content(self) -> Any: ...

    def json(self) -> Any: ...

    def raise_for_status(self) -> None: ...

    @property
    def headers(self) -> dict[str, str]: ...
"""

def_with_ellipsis_multiline = """
class BaseResponse(Protocol):

    @property
    def status_code(
        self,
        arg1,
        arg2,
    ) -> int: ...

    @property
    def content(self) -> Any: ...

    def json(self) -> Any: ...

    def raise_for_status(self) -> None: ...

    @property
    def headers(self) -> dict[str, str]: ...
"""

ellipsis_into_body = """
def status_code(arg) -> int:
    payload()
    if not arg:
        ...
    payload()




    payload()
"""


func_with_implicit_string_concatination = """
def kk() -> None:
    raise ValueError(
        "This is "
        "a very "
        "long message "
        "but there are "
        "no empty lines.",
    )
"""


@pytest.mark.parametrize('input_', [
    class_with_wrong_method,
    wrong_function,
    wrong_function_with_loop,
])
def test_wrong(
    input_,
    default_options,
    assert_errors,
    parse_tokens,
    mode,
):
    """Testing wrong cases."""
    file_tokens = parse_tokens(mode(input_))

    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [WrongEmptyLinesCountViolation])


@pytest.mark.parametrize('template', [
    class_with_valid_method,
    allow_function,
    allow_function_with_comments,
    function_with_docstring,
    function_with_docstring_and_comments,
    file_with_few_class,
    class_with_attributes,
    expression_without_function,
    module_level_empty_lines,
])
def test_success(
    template,
    parse_tokens,
    default_options,
    assert_errors,
    mode,
):
    """Testing available cases."""
    file_tokens = parse_tokens(mode(template))

    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


def test_zero_option(
    parse_tokens,
    default_options,
    assert_errors,
    options,
    mode,
):
    """Test zero configuration."""
    file_tokens = parse_tokens(mode(allow_function))
    visitor = WrongEmptyLinesCountVisitor(
        options(exps_for_one_empty_line=0), file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [WrongEmptyLinesCountViolation])


@pytest.mark.parametrize('template', [
    class_with_valid_method,
    file_with_few_class,
])
def test_zero_option_with_valid_method(
    template,
    parse_tokens,
    default_options,
    assert_errors,
    options,
    mode,
):
    """Test zero configuration with valid method."""
    file_tokens = parse_tokens(mode(template))
    visitor = WrongEmptyLinesCountVisitor(
        options(exps_for_one_empty_line=0), file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize('case', [
    def_with_ellipsis,
    def_with_ellipsis_multiline,
])
def test_def_with_ellipsis(
    case,
    parse_tokens,
    default_options,
    assert_errors,
    mode,
):
    """Test abstract classes/protocol definitions with ellipsis."""
    file_tokens = parse_tokens(mode(case))
    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [])


def test_ellipsis_into_body(
    parse_tokens,
    default_options,
    assert_errors,
    mode,
):
    """Test correct detection ellipsis into function body."""
    file_tokens = parse_tokens(mode(ellipsis_into_body))
    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [WrongEmptyLinesCountViolation])


def test_string_concatination(
    parse_tokens,
    default_options,
    assert_errors,
    options,
    mode,
):
    file_tokens = parse_tokens(mode(func_with_implicit_string_concatination))
    visitor = WrongEmptyLinesCountVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [])
