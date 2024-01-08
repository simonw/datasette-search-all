import datasette
from datasette.app import Datasette
import sqlite_utils
import pytest
import json


@pytest.fixture
def db_path(tmpdir):
    path = str(tmpdir / "data.db")
    db = sqlite_utils.Database(path)
    db["creatures"].insert_all(
        [
            {"name": "Cleo", "description": "A medium sized dog"},
            {"name": "Siroco", "description": "A troublesome Kakapo"},
        ]
    )
    return path


@pytest.mark.asyncio
async def test_no_form_on_index_if_not_searchable(db_path):
    datasette = Datasette([db_path])
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert '<form action="/-/search" method="get">' not in response.text


@pytest.mark.asyncio
async def test_no_nav_menu_if_not_searchable(db_path):
    datasette = Datasette([db_path])
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert '<details class="nav-menu">' not in response.text


@pytest.mark.asyncio
async def test_shows_form_on_index_if_searchable(db_path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    datasette = Datasette([db_path])
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert '<form action="/-/search" method="get">' in response.text


@pytest.mark.asyncio
async def test_shows_nav_menu_if_searchable(db_path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    datasette = Datasette([db_path])
    response = await datasette.client.get("/")
    assert response.status_code == 200
    for fragment in (
        '<details class="nav-menu',
        '"/-/search">Search all tables</a>'
    ):
        assert fragment in response.text


@pytest.mark.asyncio
async def test_search_page(db_path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    datasette = Datasette([db_path])
    response = await datasette.client.get("/-/search?q=dog")
    assert response.status_code == 200
    content = response.text
    assert '<form action="/-/search" method="get">' in content
    assert "<title>Search: dog</title>" in content
    assert (
        '<li data-searchable-url="/data/creatures">'
        '<a href="/data/creatures?_search=dog">'
        'Search data: creatures for "dog"</a></li>'
    ) in content
    # Should only have one set of breadcrumbs
    # https://github.com/simonw/datasette/issues/1901
    assert content.count('<p class="crumbs">') == 1
    assert content.count('<a href="/">home</a>') == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/", "/-/search"])
async def test_base_url(db_path, path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    datasette = Datasette([db_path], settings={"base_url": "/foo/"})
    response = await datasette.client.get(path)
    assert response.status_code == 200
    assert '<a href="/foo/-/search">' in response.text
    assert 'action="/foo/-/search"' in response.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "metadata,expected_tables",
    (
        ({}, ["creatures", "other"]),
        ({"allow": False}, []),
        (
            {"allow": False, "databases": {"data": {"allow": True}}},
            ["creatures", "other"],
        ),
        (
            {
                "allow": False,
                "databases": {"data": {"tables": {"creatures": {"allow": True}}}},
            },
            ["creatures"],
        ),
    ),
)
async def test_table_permissions(db_path, metadata, expected_tables):
    db = sqlite_utils.Database(db_path)
    db["creatures"].enable_fts(["name", "description"])
    db["other"].insert({"name": "name here"})
    db["other"].enable_fts(["name"])
    datasette = Datasette([db_path], metadata=metadata)
    response = await datasette.client.get("/-/search")
    menu_fragment = '<li><a href="/-/search">Search all tables</a></li>'
    if expected_tables:
        # Nav menu option should be present
        assert menu_fragment in response.text
    else:
        assert menu_fragment not in response.text
    # searchable_tables JSON should match expected
    encoded = response.text.split("var searchable_tables = ")[1].split(";")[0]
    searchable_tables = json.loads(encoded)
    assert [t["table"] for t in searchable_tables] == expected_tables
