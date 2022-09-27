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


def wrong_comprehension1():
    return [  # noqa: WPS307
        node
        for node in 'ab'
        if node != 'a'
        if node != 'b'
    ]


def wrong_comprehension2():
    return [  # noqa: WPS224
        target
        for assignment in range(hex_number)
        for target in range(assignment)
        for _ in range(10)
        if isinstance(target, int)
    ]


def positional_only(first, /, second):  # noqa: WPS451
    anti_wps428 = 1


for element in range(10):
    if (other := element) > 5:  # noqa: WPS332
        my_print(1)

    try:  # noqa: WPS452
        my_print(1)
    except AnyError:
        my_print('nope')
    finally:
        # See:
        # https://github.com/wemake-services/wemake-python-styleguide/issues/1082
        continue
    my_print(4)
