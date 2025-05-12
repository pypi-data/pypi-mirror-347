import glob
import os
import duckdb as dudb
import pandas as pd


SUPPORTED = {".csv", ".xlsx"}


def resolve_files(path: str):
    """
    Resolves a given path to a list of files. Supports direct file paths, directories,
    and glob patterns.

    Args:
        path (str): A path to a file, directory, or glob pattern.

    Returns:
        list: List of resolved file paths.

    Raises:
        ValueError: If the path is invalid or cannot be resolved.
    """
    if os.path.isdir(path):
        return glob.glob(os.path.join(path, "**", "*.*"), recursive=True)
    elif "*" in path or "?" in path:
        return glob.glob(path, recursive=True)
    elif os.path.isfile(path):
        return [path]
    else:
        raise ValueError(f"Invalid path: {path}")


def filter_supported_only_files(path):
    """
    Filters the resolved files to include only supported file types (.csv, .xlsx).

    Args:
        path (str): A path to a file, directory, or glob pattern.

    Returns:
        list: List of supported file paths.
    """
    return [
        f for f in resolve_files(path) if os.path.splitext(f)[1].lower() in SUPPORTED
    ]


def get_file_type(path):
    """
    Extracts the file extension from a file path.

    Args:
        path (str): Path to the file.

    Returns:
        str: File extension (e.g., '.csv', '.xlsx').
    """
    return os.path.splitext(path)[-1].lower()


def generate_table_name(file_path, sheet_name=None):
    """
    Generates a DuckDB-compatible table name from a file name and optional sheet name.

    Args:
        file_path (str): Path to the data file.
        sheet_name (str, optional): Name of the Excel sheet.

    Returns:
        str: Sanitized table name.
    """
    base = os.path.splitext(os.path.basename(file_path))[0]
    if sheet_name:
        return f"{base}_{sheet_name}".replace(" ", "_").lower()
    return base.replace(" ", "_").lower()


def load_table(db: str, table: str, df: pd.DataFrame):
    """
    Loads a pandas DataFrame into a DuckDB table.

    Args:
        db (str): Path to DuckDB database file.
        table (str): Name of the table to create.
        df (pd.DataFrame): DataFrame to be inserted.

    Returns:
        int: Number of rows inserted.
    """
    with dudb.connect(db) as con:
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM df")
        con.commit()
    return len(df.index)


def read_file(file_path: str, sheet: str = None) -> tuple:
    """
    Reads a .csv or .xlsx file and returns a list of DataFrames and table names.

    Args:
        file_path (str): Path to the file.
        sheet (str, optional): Sheet name for Excel files.

    Returns:
        tuple: A tuple of two lists:
            - List of pandas DataFrames.
            - List of corresponding table names.
    """
    file_type = get_file_type(file_path)

    # Initialize empty lists to store DataFrames and their corresponding table names
    df_lst = []
    table_lst = []

    if file_type == ".csv":
        # Read CSV file into DataFrame and generate table name
        df_lst.append(pd.read_csv(file_path))
        table_lst.append(generate_table_name(file_path=file_path, sheet_name=sheet))

    elif file_type == ".xlsx":
        if sheet:
            # If sheet name provided, read that sheet into DataFrame
            df_lst.append(pd.read_excel(open(file_path, "rb"), sheet_name=sheet))
            table_lst.append(generate_table_name(file_path=file_path, sheet_name=sheet))
        else:
            # If no sheet name, read all sheets
            sheets = pd.ExcelFile(file_path).sheet_names
            for sheet in sheets:
                df_lst.append(pd.read_excel(file_path, sheet_name=sheet))
                table_lst.append(
                    generate_table_name(file_path=file_path, sheet_name=sheet)
                )

    return df_lst, table_lst
