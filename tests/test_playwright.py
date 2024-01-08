try:
    from playwright import sync_api
except ImportError:
    sync_api = None
import pytest

pytestmark = pytest.mark.skipif(sync_api is None, reason="playwright not installed")


def test_ds_server(ds_server):
    with sync_api.sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(ds_server + "/")
        assert page.title() == "Datasette: data"
        # It should have a search form
        assert page.query_selector('form[action="/-/search"]')


def test_search(ds_server):
    with sync_api.sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(ds_server + "/-/search?q=cleo")
        # Should show search results, after fetching them
        assert page.locator("table tr th:nth-child(1)").inner_text() == "rowid"
        assert page.locator("table tr th:nth-child(2)").inner_text() == "name"
        assert page.locator("table tr th:nth-child(3)").inner_text() == "description"
        assert page.locator("table tr:nth-child(2) td:nth-child(1)").inner_text() == "1"
        assert (
            page.locator("table tr:nth-child(2) td:nth-child(2)").inner_text() == "Cleo"
        )
        assert (
            page.locator("table tr:nth-child(2) td:nth-child(3)").inner_text()
            == "A medium sized dog"
        )
