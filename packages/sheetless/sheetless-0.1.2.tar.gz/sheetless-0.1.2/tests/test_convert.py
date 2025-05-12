import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from sheetless.convert import convert
from duckdb import CatalogException


@pytest.fixture
def runner():
    return CliRunner()


def test_convert_no_files_found(runner):
    with patch("sheetless.utils.filter_supported_only_files", return_value=[]):
        result = runner.invoke(convert, ["--path", "some/path"])
        assert "No supported files found" in result.output
        assert result.exit_code == 0


def test_convert_invalid_path(runner):
    with patch(
        "sheetless.utils.filter_supported_only_files",
        side_effect=ValueError("Invalid path"),
    ):
        result = runner.invoke(convert, ["--path", "invalid"])
        assert "Skipping: Invalid path" in result.output
        assert result.exit_code == 0


def test_convert_multiple_files(runner):
    dummy_dfs = [MagicMock(), MagicMock()]
    dummy_tables = ["table1", "table2"]
    file_list = ["file1.csv", "file2.xlsx"]

    with patch(
        "sheetless.utils.filter_supported_only_files", return_value=file_list
    ), patch(
        "sheetless.utils.read_file", return_value=(dummy_dfs, dummy_tables)
    ), patch(
        "sheetless.utils.load_table", return_value=42
    ):
        result = runner.invoke(convert, ["--path", "dir/"])
        assert "table1" in result.output
        assert "table2" in result.output
        assert result.exit_code == 0


def test_convert_single_file_with_sheet_and_table(runner):
    dummy_df = MagicMock()
    dummy_dfs = [dummy_df]
    dummy_tables = ["auto_table"]

    with patch(
        "sheetless.utils.filter_supported_only_files", return_value=["file.xlsx"]
    ), patch(
        "sheetless.utils.read_file", return_value=(dummy_dfs, dummy_tables)
    ), patch(
        "sheetless.utils.load_table", return_value=100
    ):
        result = runner.invoke(
            convert, ["--path", "file.xlsx", "--table", "my_table", "--sheet", "Sheet1"]
        )
        assert "my_table" in result.output
        assert result.exit_code == 0


def test_convert_catalog_exception_on_table(runner):
    dummy_df = MagicMock()
    dummy_dfs = [dummy_df, dummy_df]
    dummy_tables = ["table1", "table2"]

    with patch(
        "sheetless.utils.filter_supported_only_files", return_value=["file.xlsx"]
    ), patch(
        "sheetless.utils.read_file", return_value=(dummy_dfs, dummy_tables)
    ), patch(
        "sheetless.utils.load_table",
        side_effect=[100, CatalogException("Simulated error")],
    ):
        result = runner.invoke(convert, ["--path", "file.xlsx"])
        assert "table1" in result.output
        assert "was not loaded" in result.output
        assert result.exit_code == 0  # convert doesn't raise, it prints and continues
