# -*- coding: utf-8 -*-

from server.logics.exceptions import AuthenticationException
from server.models import ApplicationUser, TelegramSession


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
