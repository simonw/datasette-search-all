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
    assert 200 == response.status_code
    assert b'<form action="/-/search" method="get">' not in response.content


@pytest.mark.asyncio
async def test_shows_form_if_searchable(db_path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    datasette = Datasette([db_path])
    response = await datasette.client.get("/")
    assert 200 == response.status_code
    assert b'<form action="/-/search" method="get">' in response.content


@pytest.mark.asyncio
async def test_search_page(db_path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    datasette = Datasette([db_path])
    response = await datasette.client.get("/-/search?q=dog")
    assert 200 == response.status_code
    content = response.content.decode("utf-8")
    assert '<form action="/-/search" method="get">' in content
    assert "<title>Search: dog</title>" in content
    assert (
        '<li><a href="/data/creatures?_search=dog">Search data: creatures for "dog"</a></li>'
        in content
    )
