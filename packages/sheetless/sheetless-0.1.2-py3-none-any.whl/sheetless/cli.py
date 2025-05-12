import click
from sheetless import convert


@click.group()
def main():
    """Entry point for the CLI."""


main.add_command(convert.convert)
