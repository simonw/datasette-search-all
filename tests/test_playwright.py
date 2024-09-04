try:
    from playwright import sync_api
except ImportError:
    sync_api = None
import pytest
import nest_asyncio

nest_asyncio.apply()

pytestmark = pytest.mark.skipif(sync_api is None, reason="playwright not installed")


def test_ds_server(ds_server, page):
    page.goto(ds_server + "/")
    assert page.title() == "Datasette: data"
    # It should have a search form
    assert page.query_selector('form[action="/-/search"]')


table_js = """
function tableToJson() {
  return Array.from(document.querySelectorAll("table")).map((table) => {
    return {
      headers: Array.from(table.querySelectorAll("th")).map((th) =>
        th.textContent.trim(),
      ),
      rows: Array.from(table.querySelectorAll("tr"))
        .slice(1)
        .map((tr) => {
          return Array.from(tr.querySelectorAll("td")).map((cell) =>
            cell.textContent.trim(),
          );
        }),
    };
  });
}
"""


def test_search(ds_server, page):
    page.goto(ds_server + "/-/search?q=cleo")
    # Should show search results, after fetching them
    page.wait_for_selector("table")
    table = page.evaluate(table_js)
    assert table == [
        {
            "headers": ["rowid", "name", "description"],
            "rows": [["1", "Cleo", "A medium sized dog"]],
        },
    ]
