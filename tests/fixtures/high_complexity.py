# -*- coding: utf-8 -*-

"""
This file contains high complexity stuff.
"""


def chech_local_variables():
    a1 = '1'
    a2 = '2'
    a3 = '3'
    a4 = '4'
    a5 = '5'
    a6 = '6'
    a7 = '7'
    a8 = '8'
    a9 = '9'
    a10 = '10'  # error here


def chech_local_variables_with_single_body():
    with open('some') as context_counts:
        try:
            a1 = '1'
            a2 = '2'
            a3 = '3'
            a4 = '4'
            a5 = '5'
        except Exception as ex_does_not_count:
            a6 = '6'
            a7 = '7'
            a8 = '8'
            a9 = '9'  # error here


def check_too_many_returns():
    if 1 == 2:
        return 1
    elif 1 == 3:
        return 2
    elif 1 == 4:
        return 3
    elif 1 == 5:
        return 4
    elif 1 == 6:
        return 5
    return 6  # error here


def check_too_many_arguments(one, two, *tree, four=4, five=5, **six):
    pass


class ClassWithWrongMethodArgs:
    def normal_method(self, one, two, *tree, four=4, five=5):
        pass

    def error_method(self, one, two, *tree, four=4, five=5, **six):
        pass

    @classmethod
    def class_normal_method(cls, one, two, *tree, four=4, five=5):
        pass

    @classmethod
    def class_error_method(cls, one=1, two=2, tree=3, four=4, five=5, six=6):
        pass

    @staticmethod
    def static_normal_method(one, two, *tree, four=4, five=5):
        pass

    @staticmethod
    def static_error_method(one, two, tree, four, five, six):
        pass

