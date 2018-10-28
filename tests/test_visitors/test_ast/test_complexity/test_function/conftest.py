# -*- coding: utf-8 -*-

import pytest

function_without_arguments = 'def function(): ...'
function_with_single_argument = 'def function(arg1): ...'
function_with_single_args = 'def function(*args): ...'
function_with_single_kwargs = 'def function(**kwargs): ...'
function_with_single_kwonly = 'def function(*, kwonly=True): ...'

method_without_arguments = """
class Test(object):
    def method(self): ...
"""

method_with_single_argument = """
class Test(object):
    def method(self, arg1): ...
"""

method_with_single_args = """
class Test(object):
    def method(self, *args): ...
"""

method_with_single_kwargs = """
class Test(object):
    def method(self, **kwargs): ...
"""

method_with_single_kwonly = """
class Test(object):
    def method(self, *, kwonly=True): ...
"""

classmethod_without_arguments = """
class Test(object):
    @classmethod
    def method(cls): ...
"""

classmethod_with_single_argument = """
class Test(object):
    @classmethod
    def method(cls, arg1): ...
"""

classmethod_with_single_args = """
class Test(object):
    @classmethod
    def method(cls, *args): ...
"""

classmethod_with_single_kwargs = """
class Test(object):
    @classmethod
    def method(cls, **kwargs): ...
"""

classmethod_with_single_kwonly = """
class Test(object):
    @classmethod
    def method(cls, *, kwonly=True): ...
"""

new_method_without_arguments = """
class Test(object):
    def __new__(cls): ...
"""

new_method_single_argument = """
class Test(object):
    def __new__(cls, arg1): ...
"""

metaclass_without_arguments = """
class TestMeta(type):
    def method(cls): ...
"""

metaclass_with_single_argument = """
class TestMeta(type):
    def method(cls, arg1): ...
"""


# Actual fixtures:

@pytest.fixture(params=[
    function_without_arguments,
    method_without_arguments,
    classmethod_without_arguments,
    new_method_without_arguments,
    metaclass_without_arguments,
])
def no_arguments(request):
    """Fixture that returns different code examples that do not have args."""
    return request.param


@pytest.fixture(params=[
    function_with_single_argument,
    function_with_single_args,
    function_with_single_kwargs,
    function_with_single_kwonly,
    method_with_single_argument,
    method_with_single_args,
    method_with_single_kwargs,
    method_with_single_kwonly,
    classmethod_with_single_argument,
    classmethod_with_single_args,
    classmethod_with_single_kwargs,
    classmethod_with_single_kwonly,
    new_method_single_argument,
    metaclass_with_single_argument,
])
def single_argument(request):
    """Fixture that returns different code examples that have a single arg."""
    return request.param
