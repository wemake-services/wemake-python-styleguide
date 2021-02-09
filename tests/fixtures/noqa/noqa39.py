"""
Here we list errors that are specific for python3.9 and further versions.

Please, do not add general violations here.
"""


@some_decorator['text']  # noqa: WPS466
def my_function():
    return 1
