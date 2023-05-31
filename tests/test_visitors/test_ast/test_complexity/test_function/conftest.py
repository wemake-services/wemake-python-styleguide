import pytest

function_with_single_argument = 'def function(arg1): ...'
function_with_arguments = 'def function(arg1, arg2): ...'
function_with_args_kwargs = 'def function(*args, **kwargs): ...'
function_with_kwonly = 'def function(*, kwonly1, kwonly2=True): ...'
function_with_posonly = 'def function(arg1, arg2, /): ...'

method_without_arguments = """
class Test(object):
    def method(self): ...
"""

method_with_single_argument = """
class Test(object):
    def method(self, arg): ...
"""

method_with_single_args = """
class Test(object):
    def method(self, *args): ...
"""

method_with_single_posonly_arg = """
class Test(object):
    def method(self, arg, /): ...
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
    function_with_single_argument,
    method_without_arguments,
    classmethod_without_arguments,
    new_method_without_arguments,
    metaclass_without_arguments,
])
def single_argument(request):
    """Fixture that returns different code examples that have one arg."""
    return request.param


@pytest.fixture(params=[
    function_with_arguments,
    function_with_args_kwargs,
    function_with_kwonly,
    function_with_posonly,
    method_with_single_argument,
    method_with_single_args,
    method_with_single_kwargs,
    method_with_single_kwonly,
    method_with_single_posonly_arg,
    classmethod_with_single_argument,
    new_method_single_argument,
    metaclass_with_single_argument,
])
def two_arguments(request):
    """Fixture that returns different code examples that have two args."""
    return request.param
