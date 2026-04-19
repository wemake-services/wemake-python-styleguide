"""Tests for the flake8 runner used by the MCP server."""

from wemake_python_styleguide.mcp.flake8_runner import (
    _get_explanation,  # noqa: PLC2701
    _parse_violations,  # noqa: PLC2701
    lint_file,
    run_flake8,
)


class TestParseViolations:
    """Test the output parser."""

    def test_empty_output(self):
        """No output means no violations."""
        assert _parse_violations('', []) == []

    def test_single_violation(self):
        """Parse a single violation line."""
        raw = 'WPS100|||1|||0|||Found wrong module name'
        source_lines = ['# bad module']
        result = _parse_violations(raw, source_lines)

        assert len(result) == 1
        assert result[0]['code'] == 'WPS100'
        assert result[0]['message'] == 'Found wrong module name'
        assert result[0]['line'] == 1
        assert result[0]['column'] == 0
        assert result[0]['source_line'] == '# bad module'

    def test_multiple_violations(self):
        """Parse multiple violation lines."""
        raw = (
            'WPS100|||1|||0|||First violation\n'
            'WPS200|||2|||4|||Second violation'
        )
        source_lines = ['line one', '    line two']
        result = _parse_violations(raw, source_lines)
        assert len(result) == 2

    def test_malformed_line_skipped(self):
        """Malformed lines are silently skipped."""
        raw = 'this is not a valid line'
        assert _parse_violations(raw, []) == []

    def test_out_of_range_line_number(self):
        """Line numbers beyond source produce empty source_line."""
        raw = 'WPS100|||999|||0|||some error'
        result = _parse_violations(raw, ['only one line'])
        assert not result[0]['source_line']

    def test_wps_violation_has_link(self):
        """WPS violations include a documentation link."""
        raw = 'WPS100|||1|||0|||msg'
        result = _parse_violations(raw, ['x'])
        assert 'link' in result[0]
        assert 'WPS100' in result[0]['link']

    def test_non_wps_violation_has_no_explanation(self):
        """Non-WPS codes should not include explanation or link."""
        raw = 'E501|||1|||80|||line too long'
        result = _parse_violations(raw, ['x' * 100])
        assert 'explanation' not in result[0]
        assert 'link' not in result[0]


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
        result = run_flake8('coordinate = 1\n')
        assert result['total_violations'] == 0
        assert result['violations'] == []

    def test_code_with_violations(self):
        """Code that triggers WPS violations returns them."""
        # Using `print` should trigger WPS421
        source = 'print("hello")\n'
        result = run_flake8(source)
        assert result['total_violations'] > 0
        violation = result['violations'][0]
        assert 'code' in violation
        assert 'message' in violation
        assert 'line' in violation
        assert 'column' in violation
        assert 'source_line' in violation

    def test_custom_filename(self):
        """Custom filename is accepted without error."""
        result = run_flake8('x = 1\n', filename='my_module.py')
        assert isinstance(result['violations'], list)

    def test_result_structure(self):
        """Result dict always has required keys."""
        result = run_flake8('coordinate = 1\n')
        assert 'violations' in result
        assert 'total_violations' in result


class TestLintFile:
    """Integration tests for lint_file."""

    def test_lint_file(self, tmp_path):
        """Lint a file on disk."""
        test_file = tmp_path / 'test_module.py'
        test_file.write_text('coordinate = 1\n')
        result = lint_file(str(test_file))
        assert 'file' in result
        assert result['file'] == str(test_file)
        assert 'violations' in result
        assert 'total_violations' in result
