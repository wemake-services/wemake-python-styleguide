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

async_method_name = """
class Input(object):
    def {0}(self): ...
"""

# Function arguments:

function_argument = 'def test({0}): ...'
async_function_argument = 'async def test({0}): ...'

method_argument = """
class Input(object):
    def validate(self, {0}): ...
"""

async_method_argument = """
class Input(object):
    async def validate(self, {0}): ...
"""

function_keyword_argument = 'def test({0}=None): ...'
async_function_keyword_argument = 'async def test({0}=None): ...'

method_keyword_argument = """
class Input(object):
    def validate(self, {0}=None): ...
"""

async_method_keyword_argument = """
class Input(object):
    async def validate(self, {0}=None): ...
"""

function_args_argument = 'def test(*{0}): ...'
async_function_args_argument = 'async def test(*{0}): ...'
function_kwargs_argument = 'def test(**{0}): ...'
async_function_kwargs_argument = 'async def test(**{0}): ...'

method_args_argument = """
class Input(object):
    def validate(self, *{0}): ...
"""

async_method_args_argument = """
class Input(object):
    def validate(self, *{0}): ...
"""

method_kwargs_argument = """
class Input(object):
    def validate(self, **{0}): ...
"""

async_method_kwargs_argument = """
class Input(object):
    def validate(self, **{0}): ...
"""

function_kwonly_argument = """
def test(*, {0}=True): ...
"""

async_function_kwonly_argument = """
async def test(*, {0}=True): ...
"""

method_kwonly_argument = """
class Input(object):
    def test(self, *, {0}=True): ...
"""

async_method_kwonly_argument = """
class Input(object):
    async def test(self, *, {0}=True): ...
"""

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

variable = """
{0} = 'test'
"""

for_variable = """
for {0} in []:
    print()
"""

async_for_variable = """
async def container():
    async for {0} in []:
        print()
"""

with_variable = """
with open('test.py') as {0}:
    raise ValueError()
"""

async_with_variable = """
async def container():
    async with open('test.py') as {0}:
        raise ValueError()
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
    async_function_name,
    method_name,
    async_method_name,

    # Function arguments:
    function_argument,
    async_function_argument,
    method_argument,
    async_method_argument,
    function_keyword_argument,
    async_function_keyword_argument,
    method_keyword_argument,
    async_method_keyword_argument,
    function_args_argument,
    async_function_args_argument,
    function_kwargs_argument,
    async_function_kwargs_argument,
    method_args_argument,
    async_method_args_argument,
    method_kwargs_argument,
    async_method_kwargs_argument,
    function_kwonly_argument,
    async_function_kwonly_argument,
    method_kwonly_argument,
    async_method_kwonly_argument,

    # Class attributes:
    static_attribute,
    instance_attribute,

    # Variables:
    variable,
    for_variable,
    async_for_variable,
    with_variable,
    async_with_variable,
    exception,
])
def naming_template(request):
    """Parametrized fixture that contains all possible naming templates."""
    return request.param
