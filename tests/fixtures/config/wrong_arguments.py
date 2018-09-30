# -*- coding: utf-8 -*-

"""
This file contains functions with too many arguments.
"""


def normal_arguments_count(one, *two, three=3, four=4, **five):
    pass


def check_too_many_arguments(one, two, *three, four=4, five=5, **six):
    pass


class ClassWithWrongMethodArgs:
    def normal_method(self, one, two, *three, four=4, five=5):
        pass

    def error_method(self, one, two, *three, four=4, five=5, **six):
        pass

    @classmethod
    def class_normal_method(cls, one, two, *three, four=4, five=5):
        pass

    @classmethod
    def class_error_method(cls, one=1, two=2, three=3, four=4, five=5, six=6):
        pass

    @staticmethod
    def static_normal_method(one, two, *three, four=4, five=5):
        pass

    @staticmethod
    def static_error_method(one, two, three, four, five, six):
        pass
