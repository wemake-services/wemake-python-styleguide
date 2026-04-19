"""Tests for the MCP server tool definitions."""

import json

import pytest

from wemake_python_styleguide.mcp.server import (
    lint,
    lint_file,
    explain_rule,
    mcp_server,
)


class TestLintTool:
    """Test the ``lint`` MCP tool."""

    def test_clean_code_returns_no_violations(self):
        """Clean code returns empty violations list."""
        result = json.loads(lint('x = 1\n'))
        assert result['total_violations'] == 0
        assert result['violations'] == []

    def test_bad_code_returns_violations(self):
        """Code with issues returns violations in JSON."""
        result = json.loads(lint('print("hello")\n'))
        assert result['total_violations'] > 0
        assert isinstance(result['violations'], list)

    def test_violation_has_required_fields(self):
        """Each violation has all required fields."""
        result = json.loads(lint('print("hello")\n'))
        assert result['total_violations'] > 0
        violation = result['violations'][0]
        for field in ('code', 'message', 'line', 'column', 'source_line'):
            assert field in violation, f'Missing field: {field}'

    def test_wps_violation_has_explanation(self):
        """WPS violations include an explanation and link."""
        result = json.loads(lint('print("hello")\n'))
        wps_violations = [
            v for v in result['violations']
            if v['code'].startswith('WPS')
        ]
        assert len(wps_violations) > 0
        for violation in wps_violations:
            assert 'explanation' in violation
            assert 'link' in violation

    def test_output_is_valid_json(self):
        """Output is always valid JSON."""
        raw = lint('x = 1\n')
        parsed = json.loads(raw)
        assert isinstance(parsed, dict)

    def test_custom_filename(self):
        """Custom filename parameter is accepted."""
        result = json.loads(lint('x = 1\n', filename='module.py'))
        assert result['total_violations'] == 0


class TestLintFileTool:
    """Test the ``lint_file`` MCP tool."""

    def test_lint_file_returns_json(self, tmp_path):
        """lint_file returns valid JSON with file key."""
        test_file = tmp_path / 'example.py'
        test_file.write_text('x = 1\n')
        result = json.loads(lint_file(str(test_file)))
        assert 'file' in result
        assert result['file'] == str(test_file)
        assert 'violations' in result


class TestExplainRuleTool:
    """Test the ``explain_rule`` MCP tool."""

    def test_known_rule(self):
        """Known rules return full documentation."""
        result = json.loads(explain_rule('WPS100'))
        assert result['code'] == 'WPS100'
        assert 'name' in result
        assert 'section' in result
        assert 'explanation' in result
        assert 'link' in result

    def test_numeric_code(self):
        """Accepts numeric-only codes."""
        result = json.loads(explain_rule('100'))
        assert result['code'] == 'WPS100'

    def test_unknown_rule(self):
        """Unknown rules return an error."""
        result = json.loads(explain_rule('WPS99999'))
        assert 'error' in result

    def test_invalid_code(self):
        """Non-numeric codes return an error."""
        result = json.loads(explain_rule('NOT_A_CODE'))
        assert 'error' in result

    def test_low_number_zero_padded(self):
        """Low-numbered codes are zero-padded to 3 digits."""
        result = json.loads(explain_rule('1'))
        assert result.get('code', '').startswith('WPS0')


class TestMCPServerRegistration:
    """Test the MCP server object has tools registered."""

    def test_server_name(self):
        """Server has the correct name."""
        assert mcp_server.name == 'wemake-python-styleguide'
