# -*- coding: utf-8 -*-

import pytest

function_arg_template = """
def function(arg: {0}):
    ...
"""

function_arg_alias_template = """
Type_Alias = {0}

def function(arg: type_alias):
    ...
"""

function_arg_multiple_alias_template = """
Type_Alias, Another_Alias = {0}, str

def function(arg: type_alias):
    ...
"""

function_return_template = """
def function(arg) -> {0}:
    ...
"""

class_field_template = """
class Test(object):
    field: {0}
"""

variable_template = """
variable: {0} = some()
"""


@pytest.fixture(params=[
    function_arg_template,
    function_arg_alias_template,
    function_return_template,
    class_field_template,
    variable_template,
])
def annotation_template(request):
    """Returns all possible annotation places."""
    return request.param
