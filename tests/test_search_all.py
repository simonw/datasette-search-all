from datasette.app import Datasette
import sqlite_utils
import pytest


@pytest.fixture
def db_paths(tmpdir):
    path1 = str(tmpdir / "data.db")
    db = sqlite_utils.Database(path1)
    db["creatures"].insert_all(
        [
            {"name": "Cleo", "description": "A medium sized dog"},
            {"name": "Siroco", "description": "A troublesome Kakapo"},
        ]
    )
    path2 = str(tmpdir / "another.db")
    db = sqlite_utils.Database(path2)
    db["things"].insert_all(
        [
            {"name": "Pencil", "description": "A writing instrument"},
            {"name": "Wheel", "description": "A basic tool"},
        ]
    )
    return [path1, path2]


async def permission_allowed(*args, **kwargs):
    return True


@pytest.mark.asyncio
async def test_no_form_on_index_if_not_searchable(db_paths):
    datasette = Datasette(db_paths)
    datasette.permission_allowed = permission_allowed
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert '<form action="/-/search" method="get">' not in response.text


@pytest.mark.asyncio
async def test_no_nav_menu_if_not_searchable(db_paths):
    datasette = Datasette(db_paths)
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert '<details class="nav-menu">' not in response.text


@pytest.mark.asyncio
async def test_shows_form_on_index_if_searchable(db_paths):
    sqlite_utils.Database(db_paths[0])["creatures"].enable_fts(["name", "description"])
    datasette = Datasette(db_paths)
    datasette.permission_allowed = permission_allowed
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert '<form action="/-/search" method="get">' in response.text


@pytest.mark.asyncio
async def test_shows_nav_menu_if_searchable(db_paths):
    sqlite_utils.Database(db_paths[0])["creatures"].enable_fts(["name", "description"])
    datasette = Datasette(db_paths)
    datasette.permission_allowed = permission_allowed
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert '<details class="nav-menu">' in response.text


@pytest.mark.asyncio
async def test_form_respects_permissions(db_paths):
    sqlite_utils.Database(db_paths[0])["creatures"].enable_fts(["name", "description"])
    sqlite_utils.Database(db_paths[1])["things"].enable_fts(["name", "description"])
    datasette = Datasette(db_paths)
    async def permission_some_dbs(actor, action, *args, **kwargs):
        resource = ()
        if args:
            resource = args[0]
        if action == "view-database" and "another" in resource:
            return False
        return True
    datasette.permission_allowed = permission_some_dbs
    response = await datasette.client.get("/")
    assert response.status_code == 200
    assert 'across 1 table' in response.text


@pytest.mark.asyncio
async def test_search_page(db_paths):
    sqlite_utils.Database(db_paths[0])["creatures"].enable_fts(["name", "description"])
    datasette = Datasette(db_paths)
    datasette.permission_allowed = permission_allowed
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
async def test_base_url(db_paths, path):
    sqlite_utils.Database(db_paths[0])["creatures"].enable_fts(["name", "description"])
    datasette = Datasette(db_paths, config={"base_url": "/foo/"})
    datasette.permission_allowed = permission_allowed
    response = await datasette.client.get(path)
    assert response.status_code == 200
    assert '<a href="/foo/-/search">' in response.text
    assert 'action="/foo/-/search"' in response.text
