import os
from setuptools import setup

VERSION = "1.1.1"


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
    project_urls={
        "Issues": "https://github.com/simonw/datasette-search-all/issues",
        "CI": "https://github.com/simonw/datasette-search-all/actions",
        "Changelog": "https://github.com/simonw/datasette-search-all/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_search_all"],
    entry_points={"datasette": ["search_all = datasette_search_all"]},
    package_data={"datasette_search_all": ["templates/*.html"]},
    install_requires=["datasette>=0.63.1"],
    python_requires=">=3.7",
    extras_require={"test": ["pytest", "pytest-asyncio", "sqlite-utils"]},
    tests_require=["datasette-search-all[test]"],
)
