# -*- coding: utf-8 -*-

import pytest

function_arg_template = """
def function(arg: {0}):
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

annotation_alias_template1 = """
a = {0}
"""

annotation_alias_template2 = """
b = c = {0}
"""

annotation_alias_template3 = """
d, e = {0}, {0}
"""


@pytest.fixture(params=[
    function_arg_template,
    function_return_template,
    class_field_template,
    variable_template,
    annotation_alias_template1,
    annotation_alias_template2,
    annotation_alias_template3,
])
def annotation_template(request):
    """Returns all possible annotation places."""
    return request.param
