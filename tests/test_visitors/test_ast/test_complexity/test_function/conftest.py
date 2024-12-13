import pytest

function_without_arguments = 'def function(): ...'
function_with_single_argument = 'def function(arg1): ...'
function_with_arguments = 'def function(arg1, arg2): ...'
function_with_args_kwargs = 'def function(*args, **kwargs): ...'
function_with_kwonly = 'def function(*, kwonly1, kwonly2=True): ...'
function_with_posonly = 'def function(arg1, arg2, /): ...'

method_without_arguments = """
class Test:
    def method(self): ...
"""

method_with_single_argument = """
class Test:
    def method(self, arg): ...
"""

method_with_single_args = """
class Test:
    def method(self, *args): ...
"""

method_with_single_posonly_arg = """
class Test:
    def method(self, arg, /): ...
"""

method_with_single_kwargs = """
class Test:
    def method(self, **kwargs): ...
"""

method_with_single_kwonly = """
class Test:
    def method(self, *, kwonly=True): ...
"""

method_with_arguments = """
class Test:
    def method(self, arg1, arg2): ...
"""

classmethod_without_arguments = """
class Test:
    @classmethod
    def method(cls): ...
"""

classmethod_with_single_argument = """
class Test:
    @classmethod
    def method(cls, arg1): ...
"""

new_method_without_arguments = """
class Test:
    def __new__(cls): ...
"""

new_method_single_argument = """
class Test:
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

staticmethod_with_no_argument = """
class Test:
    @staticmethod
    def method(): ...
"""

staticmethod_with_single_argument = """
class Test:
    @staticmethod
    def method(arg1): ...
"""

staticmethod_with_arguments = """
class Test:
    @staticmethod
    def method(arg1, arg2): ...
"""


# Actual fixtures:


@pytest.fixture(
    params=[
        function_without_arguments,
        method_without_arguments,
        classmethod_without_arguments,
        new_method_without_arguments,
        metaclass_without_arguments,
        staticmethod_with_no_argument,
    ]
)
def no_argument(request):
    """Fixture that returns different code examples that have no args."""
    return request.param


@pytest.fixture(
    params=[
        function_with_single_argument,
        method_with_single_argument,
        method_with_single_kwargs,
        method_with_single_kwonly,
        method_with_single_posonly_arg,
        classmethod_with_single_argument,
        new_method_single_argument,
        metaclass_with_single_argument,
        staticmethod_with_single_argument,
    ]
)
def single_argument(request):
    """Fixture that returns different code examples that have one arg."""
    return request.param


@pytest.fixture(
    params=[
        function_with_arguments,
        function_with_args_kwargs,
        function_with_kwonly,
        function_with_posonly,
        method_with_arguments,
        staticmethod_with_arguments,
    ]
)
def two_arguments(request):
    """Fixture that returns different code examples that have two args."""
    return request.param
