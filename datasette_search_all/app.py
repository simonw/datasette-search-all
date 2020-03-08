from starlette.responses import HTMLResponse
from starlette.endpoints import HTTPEndpoint
import json


class SearchAll(HTTPEndpoint):
    async def get(self, request):
        searchable_tables = []
        for db_name, database in self.datasette.databases.items():
            hidden_tables = set(await database.hidden_table_names())
            for table in await database.table_names():
                if table in hidden_tables:
                    continue
                fts_table = await database.fts_table(table)
                if fts_table:
                    searchable_tables.append((db_name, table))

        print(json.dumps(searchable_tables))
        return HTMLResponse(
            await self.datasette.render_template(
                "search_all.html", {
                    "q": request.query_params.get("q") or "",
                    "searchable_tables": searchable_tables,
                    "searchable_tables_json": json.dumps(searchable_tables),
                }
            )
        )
