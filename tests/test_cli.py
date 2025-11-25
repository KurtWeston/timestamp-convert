"""Tests for CLI interface."""

import pytest
from click.testing import CliRunner
from timestamp_convert.cli import cli, convert, relative, batch


@pytest.fixture
def runner():
    return CliRunner()


class TestConvertCommand:
    """Test convert command."""

    def test_convert_current_time(self, runner):
        result = runner.invoke(convert)
        assert result.exit_code == 0
        assert len(result.output) > 0

    def test_convert_unix_to_iso(self, runner):
        result = runner.invoke(convert, ["1609459200", "--to", "iso"])
        assert result.exit_code == 0
        assert "2021" in result.output

    def test_convert_to_unix(self, runner):
        result = runner.invoke(convert, ["2021-01-01T00:00:00Z", "--to", "unix"])
        assert result.exit_code == 0
        assert "1609459200" in result.output

    def test_convert_with_timezone(self, runner):
        result = runner.invoke(convert, ["1609459200", "--timezone", "America/New_York"])
        assert result.exit_code == 0

    def test_convert_custom_format_without_format_flag(self, runner):
        result = runner.invoke(convert, ["1609459200", "--to", "custom"])
        assert result.exit_code == 1
        assert "required" in result.output.lower()

    def test_convert_custom_format_with_format(self, runner):
        result = runner.invoke(convert, ["1609459200", "--to", "custom", "--format", "%Y-%m-%d"])
        assert result.exit_code == 0
        assert "2021-01-01" in result.output

    def test_convert_invalid_timestamp(self, runner):
        result = runner.invoke(convert, ["invalid"])
        assert result.exit_code == 1

    def test_convert_unknown_format(self, runner):
        result = runner.invoke(convert, ["1609459200", "--to", "unknown"])
        assert result.exit_code == 1


class TestRelativeCommand:
    """Test relative time command."""

    def test_relative_time(self, runner):
        result = runner.invoke(relative, ["1609459200"])
        assert result.exit_code == 0
        assert "ago" in result.output or "in" in result.output

    def test_relative_with_reference(self, runner):
        result = runner.invoke(relative, ["1609459200", "--reference", "1609545600"])
        assert result.exit_code == 0

    def test_relative_invalid_timestamp(self, runner):
        result = runner.invoke(relative, ["invalid"])
        assert result.exit_code == 1


class TestBatchCommand:
    """Test batch processing command."""

    def test_batch_from_stdin(self, runner):
        result = runner.invoke(batch, input="1609459200\n1609545600\n")
        assert result.exit_code == 0
        assert "2021" in result.output

    def test_batch_with_format(self, runner):
        result = runner.invoke(batch, ["--to", "unix"], input="2021-01-01T00:00:00Z\n")
        assert result.exit_code == 0

    def test_batch_empty_input(self, runner):
        result = runner.invoke(batch, input="")
        assert result.exit_code == 0


class TestCLIVersion:
    """Test CLI version and help."""

    def test_version_flag(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0

    def test_help_flag(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Timestamp conversion" in result.output