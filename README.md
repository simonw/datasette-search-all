# datasette-search-all

[![PyPI](https://img.shields.io/pypi/v/datasette-search-all.svg)](https://pypi.org/project/datasette-search-all/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-search-all/blob/master/LICENSE)

Datasette plugin for searching all searchable tables at once.

## Installation

Install the plugin in the same Python environment as Datasette:

    pip install datasette-search-all

## Usage

This plugin only works if at least one of the tables connected to your Datasette instance has been configured for SQLite's full-text search.

The [Datasette search documentation](https://datasette.readthedocs.io/en/stable/full_text_search.html) includes details on how to enable full-text search for a table.

You can also use the following tools:

* [sqlite-utils](https://sqlite-utils.readthedocs.io/en/stable/cli.html#configuring-full-text-search) includes a command-line tool for enabling full-text search.
* [datasette-enable-fts](https://github.com/simonw/datasette-enable-fts) is a Datasette plugin that adds a web interface for enabling search for specific columns.

If the plugin detects at least one searchable table it will add a search form to the homepage.

You can also navigate to `/-/search` on your Datasette instance to use the search interface directly.
