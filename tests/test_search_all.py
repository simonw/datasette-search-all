import datasette
from datasette.app import Datasette
import sqlite_utils
import pytest
import httpx


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
async def test_no_form_on_index_if_not_searcable(db_path):
    app = Datasette([db_path]).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/")
    assert 200 == response.status_code
    assert b'<form action="/-/search" method="get">' not in response.content


@pytest.mark.asyncio
async def test_shows_form_if_searchable(db_path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    app = Datasette([db_path]).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/")
    assert 200 == response.status_code
    assert b'<form action="/-/search" method="get">' in response.content


@pytest.mark.asyncio
async def test_search_page(db_path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    app = Datasette([db_path]).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/-/search?q=dog")
    assert 200 == response.status_code
    content = response.content.decode("utf-8")
    assert '<form action="/-/search" method="get">' in content
    assert "<title>Search: dog</title>" in content
    assert (
        '<li><a href="/data/creatures?_search=dog">Search data: creatures for "dog"</a></li>'
        in content
    )
