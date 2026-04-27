"""Tests for the flake8 runner used by the MCP server."""

from wemake_python_styleguide.mcp.flake8_runner import (
    _get_explanation,  # noqa: PLC2701
    _parse_violations,  # noqa: PLC2701
    lint_file,
    run_flake8,
)


class TestParseViolationsBasic:
    """Test the output parser basic functionality."""

    def test_empty_output(self):
        """No output means no violations."""
        assert _parse_violations('', []) == []

    def test_single_violation_code(self):
        """Parse a single violation line code."""
        raw = 'WPS100|||1|||0|||Found wrong module name'
        source_lines = ['# bad module']
        parsed = _parse_violations(raw, source_lines)

        assert len(parsed) == 1
        first = parsed[0]
        assert first['code'] == 'WPS100'
        assert first['message'] == 'Found wrong module name'

    def test_single_violation_location(self):
        """Parse a single violation line location."""
        raw = 'WPS100|||1|||0|||Found wrong module name'
        source_lines = ['# bad module']
        first = _parse_violations(raw, source_lines)[0]

        assert first['line'] == 1
        assert first['column'] == 0
        assert first['source_line'] == '# bad module'

    def test_multiple_violations(self):
        """Parse multiple violation lines."""
        raw = (
            'WPS100|||1|||0|||First violation\n'
            'WPS200|||2|||4|||Second violation'
        )
        source_lines = ['line one', '    line two']
        parsed = _parse_violations(raw, source_lines)
        assert len(parsed) == 2

    def test_malformed_line_skipped(self):
        """Malformed lines are silently skipped."""
        raw = 'this is not a valid line'
        assert _parse_violations(raw, []) == []

    def test_out_of_range_line_number(self):
        """Line numbers beyond source produce empty source_line."""
        raw = 'WPS100|||999|||0|||some error'
        first = _parse_violations(raw, ['only one line'])[0]
        assert not first['source_line']


class TestParseViolationsEnrichment:
    """Test the output parser WPS enrichment."""

    def test_wps_violation_has_link(self):
        """WPS violations include a documentation link."""
        raw = 'WPS100|||1|||0|||msg'
        first = _parse_violations(raw, ['x'])[0]
        assert 'link' in first
        assert 'WPS100' in first['link']

    def test_non_wps_violation_has_no_explanation(self):
        """Non-WPS codes should not include explanation or link."""
        raw = 'E501|||1|||80|||line too long'
        first = _parse_violations(raw, ['x' * 100])[0]
        assert 'explanation' not in first
        assert 'link' not in first


class TestGetExplanation:
    """Test looking up violation docstrings."""

    def test_known_violation(self):
        """Known WPS codes return a non-empty explanation."""
        explanation = _get_explanation('WPS100')
        assert explanation is not None
        assert len(explanation) > 0

    def test_unknown_violation(self):
        """Unknown codes return None."""
        assert _get_explanation('WPS99999') is None

    def test_invalid_code_format(self):
        """Non-numeric codes return None."""
        assert _get_explanation('NOT_A_CODE') is None


class TestRunFlake8:
    """Integration tests for the flake8 runner."""

    def test_clean_code(self):
        """Clean code produces zero violations."""
        output = run_flake8('coordinate = 1\n')
        assert output['total_violations'] == 0
        assert output['violations'] == []

    def test_code_with_violations_count(self):
        """Code that triggers WPS violations returns them."""
        source = 'print("hello")\n'
        output = run_flake8(source)
        assert output['total_violations'] > 0

    def test_code_with_violations_fields(self):
        """Each violation has the required fields."""
        source = 'print("hello")\n'
        violation = run_flake8(source)['violations'][0]
        assert 'code' in violation
        assert 'message' in violation
        assert 'line' in violation
        assert 'column' in violation
        assert 'source_line' in violation

    def test_custom_filename(self):
        """Custom filename is accepted without error."""
        output = run_flake8('x = 1\n', filename='my_module.py')
        assert isinstance(output['violations'], list)

    def test_result_structure(self):
        """Result dict always has required keys."""
        output = run_flake8('coordinate = 1\n')
        assert 'violations' in output
        assert 'total_violations' in output


class TestLintFile:
    """Integration tests for lint_file."""

    def test_lint_file(self, tmp_path):
        """Lint a file on disk."""
        test_file = tmp_path / 'test_module.py'
        test_file.write_text('coordinate = 1\n')
        output = lint_file(str(test_file))
        assert 'file' in output
        assert output['file'] == str(test_file)
        assert 'violations' in output
        assert 'total_violations' in output
