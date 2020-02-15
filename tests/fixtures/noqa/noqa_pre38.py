# -*- coding: utf-8 -*-

"""
This file represents how AST worked before python3.8 release.

We used to have violations on the first decorator
that wraps function, method, or a class.

We also store here things that are ``SyntaxError`` in python3.8 and above.
"""


class WithStatic(object):
    @staticmethod  # noqa: WPS602
    def some_static(arg1):
        anti_wps428 = 1

    @staticmethod  # noqa: WPS602
    async def some_async_static(arg1):
        anti_wps428 = 1


@first  # noqa: WPS216
@second
@third(param='a')
@fourth
@fifth()
@error
def decorated():
    anti_wps428 = 1


iters = list((yield letter) for letter in 'ab')  # noqa: WPS416
