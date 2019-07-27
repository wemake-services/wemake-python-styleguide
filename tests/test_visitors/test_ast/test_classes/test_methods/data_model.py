# -*- coding: utf-8 -*-

import attr


@attr.dataclass(frozen=True, slots=True)
class TestMethodArgs(object):
    """Test method arguments data wrapper."""

    definition: str = attr.ib()
    invocation: str = attr.ib()
