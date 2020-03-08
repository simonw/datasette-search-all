from .utils import get_searchable_tables
import cgi
import json


def asgi_search_page(datasette):
    async def serve_search_page(scope, receive, send):
        assert scope["type"] == "http"
        searchable_tables = await get_searchable_tables(datasette)
        query_params = dict(cgi.parse_qsl(scope["query_string"].decode("utf-8")))
        body = await datasette.render_template(
            "search_all.html",
            {
                "q": query_params.get("q") or "",
                "searchable_tables": searchable_tables,
                "searchable_tables_json": json.dumps(searchable_tables),
            },
        )
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/html; charset=utf-8"]],
            }
        )
        await send({"type": "http.response.body", "body": body.encode("utf-8")})

    return serve_search_page
