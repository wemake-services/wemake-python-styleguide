import pytest

from wemake_python_styleguide.compat.constants import PY38

# Imports:

import_alias = """
import os as {0}
"""

from_import_alias = """
from os import path as {0}
"""

# Class names:

class_name = 'class {0}: ...'


# Function names:

function_name = 'def {0}(): ...'

method_name = """
class Input(object):
    def {0}(self): ...
"""

# Function arguments:

function_argument = 'def test(arg, {0}): ...'

method_argument = """
class Input(object):
    def validate(self, {0}): ...
"""

function_keyword_argument = 'def test(arg, {0}=None): ...'

method_keyword_argument = """
class Input(object):
    def validate(self, {0}=None): ...
"""

function_args_argument = 'def test(arg, *{0}): ...'
function_kwargs_argument = 'def test(arg, **{0}): ...'

method_args_argument = """
class Input(object):
    def validate(self, *{0}): ...
"""

method_kwargs_argument = """
class Input(object):
    def validate(self, **{0}): ...
"""

function_posonly_argument = """
def test({0}, /): ...
"""

function_kwonly_argument = """
def test(*, {0}): ...
"""

function_kwonly_default_argument = """
def test(*, {0}=True): ...
"""

method_kwonly_argument = """
class Input(object):
    def test(self, *, {0}=True): ...
"""

lambda_argument = 'lambda {0}: ...'
lambda_posonly_argument = 'lambda {0}, /: ...'

# Class attributes:

static_attribute = """
class Test:
    {0} = None
"""

static_typed_attribute = """
class Test:
    {0}: int = None
"""

static_typed_annotation = """
class Test:
    {0}: int
"""

instance_attribute = """
class Test(object):
    def __init__(self):
        self.{0} = 123
"""

instance_typed_attribute = """
class Test(object):
    def __init__(self):
        self.{0}: int = 123
"""

# Variables:

variable_def = '{0} = 1'
variable_typed_def = '{0}: int = 2'
variable_typed = '{0}: str'
assignment_expression = '({0} := 1)'

# See: https://github.com/wemake-services/wemake-python-styleguide/issues/405
unpacking_variables = """
first.attr, {0} = range(2)
"""

unpacking_star_variables = """
first, *{0} = range(2)
"""

for_variable = """
def container():
    for {0} in []:
        ...
"""

for_star_variable = """
def container():
    for index, *{0} in []:
        ...
"""

with_variable = """
def container():
    with open('test.py') as {0}:
        ...
"""

with_star_variable = """
def container():
    with open('test.py') as (first, *{0}):
        ...
"""

exception = """
try:
    1 / 0
except Exception as {0}:
    raise
"""


# Fixtures:

_ALL_FIXTURES = frozenset((
    # Imports:
    import_alias,
    from_import_alias,

    # Class names:
    class_name,

    # Function names, we don't use async function because we generate them:
    function_name,
    method_name,

    # Function arguments:
    function_argument,
    method_argument,
    function_keyword_argument,
    method_keyword_argument,
    function_args_argument,
    function_kwargs_argument,
    method_args_argument,
    method_kwargs_argument,
    function_kwonly_argument,
    function_kwonly_default_argument,
    method_kwonly_argument,
    lambda_argument,

    # Class attributes:
    static_attribute,
    static_typed_attribute,
    static_typed_annotation,
    instance_attribute,
    instance_typed_attribute,

    # Variables:
    variable_def,
    variable_typed_def,
    variable_typed,
    unpacking_variables,
    unpacking_star_variables,
    for_variable,
    for_star_variable,
    with_variable,
    with_star_variable,
    exception,
))

if PY38:
    _ALL_FIXTURES |= {
        function_posonly_argument,
        lambda_posonly_argument,
        assignment_expression,
    }

_FORBIDDEN_UNUSED_TUPLE = frozenset((
    unpacking_variables,
    variable_def,
    with_variable,
    for_variable,
))

# Raw unused variables return True for logic.naming.access.is_unused().
# Example: _, __.
# Protected unused variables return True for logic.naming.access.is_protected().
# Example: _protected.
_FORBIDDEN_BOTH_RAW_AND_PROTECTED_UNUSED = frozenset((
    unpacking_variables,
    variable_def,
    with_variable,
    variable_typed_def,
    variable_typed,
    exception,
))

if PY38:
    _FORBIDDEN_BOTH_RAW_AND_PROTECTED_UNUSED |= {
        assignment_expression,
    }

_FORBIDDEN_RAW_UNUSED = _FORBIDDEN_BOTH_RAW_AND_PROTECTED_UNUSED | {
    static_attribute,
    static_typed_attribute,
    static_typed_annotation,
}

_FORBIDDEN_PROTECTED_UNUSED = _FORBIDDEN_BOTH_RAW_AND_PROTECTED_UNUSED | {
    for_variable,
}


@pytest.fixture(params=_ALL_FIXTURES)
def naming_template(request):
    """Parametrized fixture that contains all possible naming templates."""
    return request.param


@pytest.fixture(params=_FORBIDDEN_UNUSED_TUPLE)
def forbidden_tuple_unused_template(request):
    """Returns template that can be used to define wrong unused tuples."""
    return request.param


@pytest.fixture(params=_FORBIDDEN_RAW_UNUSED)
def forbidden_raw_unused_template(request):
    """Returns template that forbids defining raw unused variables."""
    return request.param


@pytest.fixture(params=_ALL_FIXTURES - _FORBIDDEN_RAW_UNUSED)
def allowed_raw_unused_template(request):
    """Returns template that allows defining raw unused variables."""
    return request.param


@pytest.fixture(params=_FORBIDDEN_PROTECTED_UNUSED)
def forbidden_protected_unused_template(request):
    """Returns template that forbids defining protected unused variables."""
    return request.param


@pytest.fixture(params=_ALL_FIXTURES - _FORBIDDEN_PROTECTED_UNUSED)
def allowed_protected_unused_template(request):
    """Returns template that allows defining protected unused variables."""
    return request.param
