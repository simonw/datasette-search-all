# datasette-search-all

[![PyPI](https://img.shields.io/pypi/v/datasette-search-all.svg)](https://pypi.org/project/datasette-search-all/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-search-all/blob/master/LICENSE)

Datasette plugin for searching all searchable tables at once.

## Installation

Install the plugin in the same Python environment as Datasette:

    pip install datasette-search-all

## Usage

Navigate to `/-/search` on your Datasette instance to use this plugin.

It will scan all of the attached databases for any tables that have been configured for full-text search, and allow you to run searches across all of those tables at once.

Learn more about full-text search and how to enable it in the [Datasette search documentation](https://datasette.readthedocs.io/en/stable/full_text_search.html).
