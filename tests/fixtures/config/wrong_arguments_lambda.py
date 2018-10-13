# -*- coding: utf-8 -*-

"""
This file contains lambda functions with too many arguments.
"""


x = lambda one, *two, three=3, four=4, **five: one

y = lambda one, two, *three, four=4, five=5, **six: one


def method_with_internal_lambda_function():
    y = lambda one, two, *three, four=4, five=5, **six: one


class ClassWithWrongMethodArgs:
    def class_method_with_internal_lambda_function(self):
        y = lambda one, two, *three, four=4, five=5, **six: one

    def error_method_with_internal_lambda_function(self, one, two, *three, four=4, five=5, **six):
        y = lambda one, two, *three, four=4, five=5, **six: one
