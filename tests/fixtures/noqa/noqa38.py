# -*- coding: utf-8 -*-

"""
This file represents AST location changes in python3.8 and above.

The reason is that some AST nodes now have a different location.
Now violations are reported on lines where functions, methods,
and classes are defined.

Not on lines where the first decorator is defined.
"""


class WithStatic(object):
    @staticmethod
    def some_static(arg1):  # noqa: WPS602
        anti_wps428 = 1

    @staticmethod
    async def some_async_static(arg1):  # noqa: WPS602
        anti_wps428 = 1


@first
@second
@third(param='a')
@fourth
@fifth()
@error
def decorated():  # noqa: WPS216
    anti_wps428 = 1
