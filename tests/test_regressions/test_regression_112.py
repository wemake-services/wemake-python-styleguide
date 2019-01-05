# -*- coding: utf-8 -*-

import ast

from pyflakes.checker import Checker as PyFlakesChecker

from wemake_python_styleguide.checker import Checker


code_that_brakes = '''
def current_session(
    telegram_id: int,
    for_update: bool = True,
) -> TelegramSession:
    """
    Was triggering `AttributeError`.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/112
    """
    try:
        query = TelegramSession.objects.all()
        if for_update:  # Try to comment this `if` to fix everything
            query = query.select_for_update()

        return query.get(
            uid=telegram_id,
            is_verified=True,
        )

    except TelegramSession.DoesNotExist:
        raise AuthenticationException('Session is missing')
'''


def test_regression112(default_options):
    """
    There was a conflict between ``pyflakes`` and our plugin.

    We were fighting for ``parent`` property.
    Now we use a custom prefix.

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/112
    """
    module = ast.parse(code_that_brakes)
    Checker.parse_options(default_options)
    checker = Checker(tree=module, file_tokens=[], filename='custom.py')

    # It was failing on this line:
    # AttributeError: 'ExceptHandler' object has no attribute 'depth'
    flakes = PyFlakesChecker(module)

    assert flakes.root
