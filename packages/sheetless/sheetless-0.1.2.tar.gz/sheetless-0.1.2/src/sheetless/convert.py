import click
from sheetless import utils
import duckdb as dudb


@click.command()
@click.option(
    "--duckdb",
    type=str,
    required=False,
    help="Path to duckdb file to be used/created",
    default="db.duckdb",
)
@click.option(
    "--path",
    type=str,
    required=True,
    help="Path to file or directory. Supports *.csv, *.xlsx, etc.",
)
@click.option(
    "--table", type=str, help="The name of the table that will be created in db."
)
@click.option(
    "--sheet", type=str, help="The sheet name to be loaded from an xlsx file."
)
def convert(duckdb: str, path: str, table: str, sheet: str) -> None:
    """
    A command-line interface (CLI) function to convert data files (CSV, Excel)
    into DuckDB tables.

    This function reads the provided file(s), processes them, and loads them into
    a DuckDB database.

    Args:
        duckdb (str): Path to the DuckDB database file.
        path (str): Path to the file or directory containing files to be converted.
        table (str, optional): Table name for storing data in DuckDB.
        sheet (str, optional): Sheet name for Excel files to specify which sheet
                                to load.

    Returns:
        None
    """
    try:
        # Resolves the files in the provided path and filters for supported file types
        file_paths_lst = utils.filter_supported_only_files(path)
    except ValueError as e:
        # In case of invalid path or unsupported file types, show error and exit
        click.echo(f"🚨  Skipping: {e}")
        return

    # If no supported files are found, notify the user and exit
    if len(file_paths_lst) == 0:
        click.echo("🚨  Skipping: No supported files found.")
        return

    # If multiple files are found, notify the user that specific table and sheet
    # options won't apply
    if len(file_paths_lst) > 1:
        if table:
            click.echo(
                f"⚠️  Table name given '{table}' will be not considered due to \
                     mutliple files found for loading."
            )
        if sheet:
            click.echo(f"⚠️  Sheet name given '{sheet}' will be not considered.")

        # Process each file individually and load them into the DuckDB database
        for file_path in file_paths_lst:
            df_lst, table_lst = utils.read_file(file_path)
            for i in range(len(table_lst)):
                # Load each table and confirm success
                n_rows = utils.load_table(db=duckdb, table=table_lst[i], df=df_lst[i])
                click.echo(
                    f"✅ Table '{table_lst[i]}' with {n_rows} lines loaded "
                    + f"from file '{file_paths_lst[0]}'"
                )

    # If only one file is found, process that file
    elif len(file_paths_lst) == 1:

        # Read the file and get the dataframes and table names
        df_lst, table_lst = utils.read_file(file_paths_lst[0], sheet=sheet)

        # If the file contains multiple tables (e.g., multiple sheets in Excel),
        # load them one by one
        if len(table_lst) > 1:
            for i in range(len(table_lst)):
                try:
                    # Load each table into DuckDB and handle any CatalogExceptions
                    n_rows = utils.load_table(
                        db=duckdb, table=table_lst[i], df=df_lst[i]
                    )
                    click.echo(
                        f"✅ Table '{table_lst[i]}' with {n_rows} lines "
                        + f"loaded from file '{file_paths_lst[0]}'"
                    )
                except dudb.CatalogException as e:
                    # If there is a problem with creating the table in the database,
                    #  show error
                    click.echo(f"🚨  Table '{table_lst[i]}' was not loaded: {e}")
            return

        # If a specific table name is provided, use it; otherwise, use the default
        # table name generated from the file
        if table:
            n_rows = utils.load_table(db=duckdb, table=table, df=df_lst[0])
            click.echo(
                f"✅ Table '{table}' with {n_rows} lines loaded "
                + f"from file '{file_paths_lst[0]}'"
            )
            return

        # Otherwise, use the generated table name
        n_rows = utils.load_table(db=duckdb, table=table_lst[0], df=df_lst[0])
        click.echo(
            f"✅ Table '{table_lst[0]}' with {n_rows} "
            + f"lines loaded from file '{file_paths_lst[0]}'"
        )
        return
