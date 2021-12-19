import datasette
from datasette.app import Datasette
import sqlite_utils
import pytest


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
    assert '<details class="nav-menu">' in response.text


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


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/", "/-/search"])
async def test_base_url(db_path, path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    datasette = Datasette([db_path], settings={"base_url": "/foo/"})
    response = await datasette.client.get(path)
    assert response.status_code == 200
    assert '<a href="/foo/-/search">' in response.text
    assert 'action="/foo/-/search"' in response.text
