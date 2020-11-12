import os
from setuptools import setup

VERSION = "0.3"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-search-all",
    description="Datasette plugin for searching all searchable tables at once",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-search-all",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_search_all"],
    entry_points={"datasette": ["search_all = datasette_search_all"]},
    package_data={"datasette_search_all": ["templates/*.html"]},
    install_requires=["datasette>=0.51"],
    extras_require={"test": ["pytest", "pytest-asyncio", "sqlite-utils"]},
    tests_require=["datasette-search-all[test]"],
)
