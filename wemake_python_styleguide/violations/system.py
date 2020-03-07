"""
These checks ensures that our internal checks passes.

For example, we can report violations from this group
when some exception occur during the linting process
or some dependencies are missing.

.. currentmodule:: wemake_python_styleguide.violations.system

Summary
-------

.. autosummary::
   :nosignatures:

   InternalErrorViolation

Respect your objects
--------------------

.. autoclass:: InternalErrorViolation

"""

from typing_extensions import final

from wemake_python_styleguide.violations.base import SimpleViolation


@final
class InternalErrorViolation(SimpleViolation):
    """
    Happens when we get unhandled exception during the linting process.

    All this violations should be reported to the main issue tracker.
    We ideally should not produce these violations at all.

    See also:
        https://github.com/wemake-services/wemake-python-styleguide/issues

    .. versionadded:: 0.13.0

    """

    error_template = (
        'Internal error happened, see log. Please, take some time to report it'
    )
    code = 0
