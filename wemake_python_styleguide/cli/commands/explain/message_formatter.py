from typing import Final

from wemake_python_styleguide.cli.commands.explain.violation_loader import ViolationInfo

_DOCS_URL: Final = (
    'https://wemake-python-styleguide.readthedocs.io/en/latest/pages/'
    'usage/violations/{0}.html#{1}'
)


def _clean_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _replace_tabs(text: str, tab_size: int = 4) -> str:
    return text.replace("\t", " " * tab_size)


def _get_whitespace_prefix(line: str) -> int:
    for char_index, char in enumerate(line):
        if char != ' ':
            return char_index
    return len(line)


def _get_greatest_common_indent(text: str) -> int:
    lines = text.split("\n")
    if len(lines) == 0:
        return 0
    greatest_common_indent = float("+inf")
    for line in lines:
        if len(line.strip()) == 0:
            continue
        greatest_common_indent = min(
            greatest_common_indent,
            _get_whitespace_prefix(line)
        )
    if greatest_common_indent == float("+inf"):
        greatest_common_indent = 0
    return greatest_common_indent


def _remove_indentation(text: str, tab_size: int = 4) -> str:
    text = _replace_tabs(_clean_text(text), tab_size)
    max_indent = _get_greatest_common_indent(text)
    return "\n".join(line[max_indent:] for line in text.split("\n"))


def format_violation(violation: ViolationInfo) -> str:
    cleaned_docstring = _remove_indentation(violation.docstring)
    violation_url = _DOCS_URL.format(
        violation.section,
        violation.fully_qualified_id,
    )
    return (
        f"WPS{violation.code} ({violation.identifier})\n"
        f"{cleaned_docstring}\n"
        f"See at website: {violation_url}"
    )
