import pytest


@pytest.fixture()
def async_wrapper():
    """Fixture to convert all regular functions into async ones."""
    def factory(template: str) -> str:
        return template.replace(
            'def ', 'async def ',
        ).replace(
            'with ', 'async with ',
        ).replace(
            'for ', 'async for ',
        )
    return factory


@pytest.fixture()
def regular_wrapper():
    """Fixture to return regular functions without modifications."""
    def factory(template: str) -> str:
        return template
    return factory


@pytest.fixture(params=['async_wrapper', 'regular_wrapper'])
def mode(request):
    """Fixture that returns either `async` or regular functions."""
    return request.getfixturevalue(request.param)
