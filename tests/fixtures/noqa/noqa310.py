user_id = 'uuid-user-id'
match user:
    case 'user_id' | 'uid' as _uid:  # noqa: WPS122
        raise ValueError(_uid)
    case {'key': k}:  # noqa: WPS111
        raise ValueError(k)
    case [value]:  # noqa: WPS110
        raise ValueError(value)
