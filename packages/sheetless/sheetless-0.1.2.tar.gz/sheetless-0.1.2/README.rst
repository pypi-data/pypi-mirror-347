
.. image:: static/commic.png
   :alt: commic

=========

.. image:: static/sheetless.png
   :alt: Logo

Sheetless
=========

**Sheetless** is a command-line tool that helps you escape the spreadsheet swamp.

It loads `.csv` and `.xlsx` files into a DuckDB database, so you can explore your data using pure SQL — without writing a line of Python.

Think of it as your bridge from Excel to SQL based analytics.



Features
--------

- 🔄 Convert CSV and Excel files to DuckDB tables
- 📁 Supports directories and wildcards
- 📊 Handles multi-sheet Excel files
- 🧠 Generates safe table names automatically
- 🧹 One command, clean results



Installation
------------

Install it directly from PyPI:

.. code-block:: bash

    pip install sheetless



Quick Start
-----------

Convert a single CSV file into a DuckDB database:

.. code-block:: bash

    sheetless convert --path data.csv --duckdb mydata.duckdb

Convert all Excel files in a directory:

.. code-block:: bash

    sheetless convert --path "data/*.xlsx" --duckdb warehouse.duckdb

Load a specific sheet from an Excel file:

.. code-block:: bash

    sheetless convert --path report.xlsx --sheet "Q2 Sales" --duckdb insights.duckdb

If no table name is given, one is generated from the file and sheet name.


Options
-------

- ``--path``: Path to file, folder, or wildcard pattern (e.g. `*.csv`)
- ``--duckdb``: DuckDB file to use or create
- ``--table``: (Optional) Custom table name (only works for single file/sheet)
- ``--sheet``: (Optional) Sheet name to load from an Excel file



Why Sheetless?
--------------

Because if you're stuck in Excel, SQL is freedom.  
**Sheetless** makes it one CLI command away.



License
-------

MIT License



Author
------

Developed by Christos Georgoulis – `GitHub <https://github.com/georgoulis>`_

