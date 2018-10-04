# -*- coding: utf-8 -*-

"""
This file contains async functions with too many arguments.
"""


async def normal_arguments_count_async(one, *two, three=3, four=4, **five):
    pass


async def check_too_many_arguments_async(
    one, two, *three, four=4, five=5, **six,
):
    pass


class ClassWithWrongAsyncMethodArgs:
    async def async_normal_method(self, one, two, *three, four=4, five=5):
        pass

    async def async_error_method(self, one, two, *three, four=4, five=5, **six):
        pass

    @classmethod
    async def async_class_normal_method(cls, one, two, *three, four=4, five=5):
        pass

    @classmethod
    async def async_class_error_method(
        cls, one=1, two=2, three=3, four=4, five=5, six=6,
    ):
        pass

    @staticmethod
    async def async_static_normal_method(one, two, *three, four=4, five=5):
        pass

    @staticmethod
    async def async_static_error_method(one, two, three, four, five, six):
        pass
