from starlette.responses import HTMLResponse
from starlette.endpoints import HTTPEndpoint
from .utils import get_searchable_tables
import json


class SearchAll(HTTPEndpoint):
    async def get(self, request):
        searchable_tables = await get_searchable_tables(self.datasette)

        return HTMLResponse(
            await self.datasette.render_template(
                "search_all.html",
                {
                    "q": request.query_params.get("q") or "",
                    "searchable_tables": searchable_tables,
                    "searchable_tables_json": json.dumps(searchable_tables),
                },
            )
        )
