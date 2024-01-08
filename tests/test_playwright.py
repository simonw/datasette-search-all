try:
    from playwright import sync_api
except ImportError:
    sync_api = None
import pytest


@pytest.mark.skipif(sync_api is None, reason="playwright not installed")
def test_ds_server(ds_server):
    with sync_api.sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(ds_server + "/")
        assert page.title() == "Datasette: data"
        # It should have a search form
        assert page.query_selector('form[action="/-/search"]')
