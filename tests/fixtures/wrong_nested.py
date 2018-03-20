# -*- coding: utf-8 -*-


def nested_functions():
    def inner_function():
        print('nested')


def nested_with_lambda():
    map(lambda x: x, [])


class ClassWithNested(object):
    class Meta:
        field = 12

    class NestedClass:
        nested_field = 1

    def method_with_nested(self):
        def function_in_method():
            print('inside method')


def function_with_nested_class(object):
    class NestedInFunction(object):
        blob = 'some'
