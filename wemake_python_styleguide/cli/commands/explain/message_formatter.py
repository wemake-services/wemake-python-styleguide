import importlib
import re
import textwrap
from typing import Any, Final

from wemake_python_styleguide.cli.commands.explain.violation_loader import (
    ViolationInfo,
)
from wemake_python_styleguide.constants import SHORTLINK_TEMPLATE

_RST_ROLE_PATTERN: Final = re.compile(r':(str|py:data|py:class|py:func):`~?([\w.]+)`')
_MAX_INLINE_ITEMS: Final = 8


def _format_value(attribute: Any) -> str:
    """Render a resolved constant for inline display."""
    if isinstance(attribute, (frozenset, set)):
        attribute = tuple(sorted(attribute))
    if isinstance(attribute, (tuple, list)):
        return repr(tuple(attribute))
    return str(attribute)


def _resolve_rst_references(text: str) -> str:
    """Replace RST roles with readable plain text."""
    return _RST_ROLE_PATTERN.sub(_render_reference, text)


def _try_resolve(dotted_path: str) -> Any | None:
    """Resolve an attribute from a dotted path."""
    module_path, _, attr_name = dotted_path.rpartition('.')
    if not module_path or module_path.startswith('.'):
        # Relative refs like `~.Name` have no anchor package
        return None
    try:
        return getattr(importlib.import_module(module_path), attr_name)
    except Exception:
        return None


def _render_reference(match: re.Match[str]) -> str:
    """Render one RST role as a value or a plain-text path."""
    _, dotted_path = match.groups()
    attribute = _try_resolve(dotted_path)
    if attribute is None or (
        isinstance(attribute, (tuple, frozenset, list))
        and len(attribute) > _MAX_INLINE_ITEMS
    ):
        return dotted_path.lstrip('~.')
    return f'`{_format_value(attribute)}`'


def _remove_newlines_at_ends(text: str) -> str:
    """Remove leading and trailing newlines."""
    return text.strip('\n\r')


def format_violation(violation: ViolationInfo) -> str:
    """Format violation information."""
    cleaned_docstring = _resolve_rst_references(
        _remove_newlines_at_ends(
            textwrap.dedent(violation.docstring),
        ),
    )
    violation_url = SHORTLINK_TEMPLATE.format(f'WPS{violation.code}')
    return f'{cleaned_docstring}\n\nSee at website: {violation_url}'
