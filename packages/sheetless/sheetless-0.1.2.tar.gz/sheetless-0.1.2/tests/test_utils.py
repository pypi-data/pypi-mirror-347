import pandas as pd
import duckdb
from sheetless import utils


__author__ = "georgoulis"
__copyright__ = "georgoulis"
__license__ = "MIT"


def test_resolve_files_with_file(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text("a,b\n1,2")
    result = utils.resolve_files(str(test_file))
    assert result == [str(test_file)]


def test_resolve_files_with_directory(tmp_path):
    (tmp_path / "a.csv").write_text("x,y\n1,2")
    (tmp_path / "b.txt").write_text("hello")
    files = utils.resolve_files(str(tmp_path))
    assert any(f.endswith(".csv") for f in files)


def test_filter_supported_only_files(tmp_path):
    (tmp_path / "a.csv").write_text("x,y\n1,2")
    (tmp_path / "b.txt").write_text("ignore this")
    supported = utils.filter_supported_only_files(str(tmp_path))
    assert len(supported) == 1
    assert supported[0].endswith("a.csv")


def test_get_file_type():
    assert utils.get_file_type("report.csv") == ".csv"
    assert utils.get_file_type("data.xlsx") == ".xlsx"


def test_generate_table_name():
    assert utils.generate_table_name("My File.xlsx") == "my_file"
    assert utils.generate_table_name("File.xlsx", "Sheet 1") == "file_sheet_1"


def test_load_table_creates_table(tmp_path):
    db_path = tmp_path / "test.duckdb"
    df = pd.DataFrame({"a": [1, 2]})
    table_name = "my_table"
    n_rows = utils.load_table(str(db_path), table_name, df)
    assert n_rows == 2

    # Validate table creation
    con = duckdb.connect(str(db_path))
    result = con.execute("SELECT * FROM my_table").fetchall()
    assert result == [(1,), (2,)]


def test_read_file_csv(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("a,b\n1,2")
    dfs, names = utils.read_file(str(csv_path))
    assert len(dfs) == 1
    assert names[0] == "data"
    assert dfs[0].shape == (1, 2)


def test_read_file_xlsx(tmp_path):
    xlsx_path = tmp_path / "book.xlsx"
    df = pd.DataFrame({"a": [1, 2]})
    df.to_excel(xlsx_path, index=False, sheet_name="Sheet1")

    dfs, names = utils.read_file(str(xlsx_path))
    assert len(dfs) == 1
    assert names[0] == "book_sheet1"
    assert dfs[0].equals(df)


def test_read_file_xlsx_specific_sheet(tmp_path):
    xlsx_path = tmp_path / "book.xlsx"
    df = pd.DataFrame({"a": [1, 2]})
    df.to_excel(xlsx_path, index=False, sheet_name="test_sheet")

    dfs, names = utils.read_file(str(xlsx_path), sheet="test_sheet")
    assert len(dfs) == 1
    assert names[0] == "book_test_sheet"
    assert dfs[0].equals(df)
