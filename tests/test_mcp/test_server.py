"""Tests for the MCP server tool definitions."""

import json

from wemake_python_styleguide.mcp.server import (
    explain_rule,
    lint,
    lint_file,
    mcp_server,
)


class TestLintTool:
    """Test the ``lint`` MCP tool."""

    def test_clean_code_returns_no_violations(self):
        """Clean code returns empty violations list."""
        output = json.loads(lint('coordinate = 1\n'))
        assert output['total_violations'] == 0
        assert output['violations'] == []

    def test_bad_code_returns_violations(self):
        """Code with issues returns violations in JSON."""
        output = json.loads(lint('print("hello")\n'))
        assert output['total_violations'] > 0
        assert isinstance(output['violations'], list)

    def test_violation_has_required_fields(self):
        """Each violation has all required fields."""
        output = json.loads(lint('print("hello")\n'))
        assert output['total_violations'] > 0
        violation = output['violations'][0]
        for field in ('code', 'message', 'line', 'column', 'source_line'):
            assert field in violation, f'Missing field: {field}'

    def test_wps_violation_has_explanation(self):
        """WPS violations include an explanation and link."""
        output = json.loads(lint('print("hello")\n'))
        wps_violations = [
            entry
            for entry in output['violations']
            if entry['code'].startswith('WPS')
        ]
        assert len(wps_violations) > 0
        for violation in wps_violations:
            assert 'explanation' in violation
            assert 'link' in violation

    def test_output_is_valid_json(self):
        """Output is always valid JSON."""
        raw = lint('coordinate = 1\n')
        parsed = json.loads(raw)
        assert isinstance(parsed, dict)

    def test_custom_filename(self):
        """Custom filename parameter is accepted."""
        output = json.loads(lint('coordinate = 1\n', filename='module.py'))
        assert output['total_violations'] == 0


class TestLintFileTool:
    """Test the ``lint_file`` MCP tool."""

    def test_lint_file_returns_json(self, tmp_path):
        """lint_file returns valid JSON with file key."""
        test_file = tmp_path / 'example.py'
        test_file.write_text('coordinate = 1\n')
        output = json.loads(lint_file(str(test_file)))
        assert 'file' in output
        assert output['file'] == str(test_file)
        assert 'violations' in output


class TestExplainRuleTool:
    """Test the ``explain_rule`` MCP tool."""

    def test_known_rule(self):
        """Known rules return full documentation."""
        output = json.loads(explain_rule('WPS100'))
        assert output['code'] == 'WPS100'
        assert 'name' in output
        assert 'section' in output
        assert 'explanation' in output
        assert 'link' in output

    def test_numeric_code(self):
        """Accepts numeric-only codes."""
        output = json.loads(explain_rule('100'))
        assert output['code'] == 'WPS100'

    def test_unknown_rule(self):
        """Unknown rules return an error."""
        output = json.loads(explain_rule('WPS99999'))
        assert 'error' in output

    def test_invalid_code(self):
        """Non-numeric codes return an error."""
        output = json.loads(explain_rule('NOT_A_CODE'))
        assert 'error' in output

    def test_low_number_zero_padded(self):
        """Low-numbered codes are zero-padded to 3 digits."""
        output = json.loads(explain_rule('0'))
        assert output.get('code', '') == 'WPS000'


class TestMCPServerRegistration:
    """Test the MCP server object has tools registered."""

    def test_server_name(self):
        """Server has the correct name."""
        assert mcp_server.name == 'wemake-python-styleguide'
