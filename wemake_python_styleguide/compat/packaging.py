# -*- coding: utf-8 -*-

import sys

# Note that we use ``sys.version_info`` directly,
# because that's how ``mypy`` knows about what we are doing.
if sys.version_info >= (3, 8):  # pragma: py-lt-38
    from importlib import metadata as importlib_metadata  # noqa: WPS433
else:  # pragma: py-gte-38
    import importlib_metadata  # noqa: F401, WPS440, WPS433
