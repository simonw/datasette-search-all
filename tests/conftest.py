from pathlib import Path
import pytest
import sqlite_utils
from subprocess import Popen, PIPE
import sys
import time
import httpx


def populate_db(db, search=False):
    db["creatures"].insert_all(
        [
            {"name": "Cleo", "description": "A medium sized dog"},
            {"name": "Siroco", "description": "A troublesome Kakapo"},
        ]
    )
    if search:
        db["creatures"].enable_fts(["name", "description"])


@pytest.fixture
def db_path(tmpdir):
    path = str(tmpdir / "data.db")
    db = sqlite_utils.Database(path)
    populate_db(db)
    return path


@pytest.fixture
def db_path_searchable(db_path):
    sqlite_utils.Database(db_path)["creatures"].enable_fts(["name", "description"])
    return db_path


@pytest.fixture(scope="session")
def ds_server(tmp_path_factory):
    db_path = str(tmp_path_factory.mktemp("data") / "data.db")
    db = sqlite_utils.Database(db_path)
    populate_db(db, search=True)
    process = Popen(
        [
            sys.executable,
            "-m",
            "datasette",
            "--port",
            "8126",
            str(db_path),
        ],
        stdout=PIPE,
    )
    wait_until_responds("http://localhost:8126/")
    yield "http://localhost:8126"

    process.terminate()
    process.wait()


def wait_until_responds(url, timeout=5.0, **kwargs):
    start = time.time()
    while time.time() - start < timeout:
        try:
            httpx.get(url, **kwargs)
            return
        except httpx.ConnectError:
            time.sleep(0.1)
    raise AssertionError("Timed out waiting for {} to respond".format(url))
