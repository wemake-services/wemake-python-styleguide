# -*- coding: utf-8 -*-

import pytest

# Imports:

import_alias = """
import os as {0}
"""

from_import_alias = """
from os import path as {0}
"""

# Function names:

function_name = 'def {0}(): ...'
async_function_name = 'async def {0}(): ...'

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

function_kwonly_argument = """
def test(*, {0}=True): ...
"""

method_kwonly_argument = """
class Input(object):
    def test(self, *, {0}=True): ...
"""

lambda_argument = 'lambda {0}: ...'

# Class attributes:

static_attribute = """
class Test:
    {0} = None
"""

instance_attribute = """
class Test(object):
    def __init__(self):
        self.{0} = 123
"""

# Variables:

variable_def = """
{0} = 'test'
"""

# See: https://github.com/wemake-services/wemake-python-styleguide/issues/405
unpacking_variables = """
first.attr, {0} = range(2)
"""

for_variable = """
def container():
    for {0} in []:
        ...
"""

with_variable = """
def container():
    with open('test.py') as {0}:
        ...
"""

exception = """
try:
    1 / 0
except Exception as {0}:
    raise
"""


# Fixture itself:

@pytest.fixture(params=[
    # Imports:
    import_alias,
    from_import_alias,

    # Function names:
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
    method_kwonly_argument,
    lambda_argument,

    # Class attributes:
    static_attribute,
    instance_attribute,

    # Variables:
    variable_def,
    unpacking_variables,
    for_variable,
    with_variable,
    exception,
])
def naming_template(request):
    """Parametrized fixture that contains all possible naming templates."""
    return request.param
