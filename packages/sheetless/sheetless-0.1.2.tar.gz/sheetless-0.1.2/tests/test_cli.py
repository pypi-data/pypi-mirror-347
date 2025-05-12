# tests/test_cli.py

from click.testing import CliRunner
from sheetless.cli import main


def test_cli_invokes_main_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "convert" in result.output


def test_cli_with_no_args():
    runner = CliRunner()
    result = runner.invoke(main)

    # CLI group without args returns help and exits with 0
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "convert" in result.output


def test_convert_command_registered():
    runner = CliRunner()
    result = runner.invoke(main, ["convert", "--help"])

    assert result.exit_code == 0
    assert "Path to file or directory" in result.output
