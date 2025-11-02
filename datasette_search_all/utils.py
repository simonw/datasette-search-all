from datasette import Forbidden
from datasette.resources import TableResource


async def iterate_searchable_tables(datasette, request):
    for db_name, database in datasette.databases.items():
        hidden_tables = set(await database.hidden_table_names())
        for table in await database.table_names():
            if table in hidden_tables:
                continue
            if table.endswith("_fts"):
                continue
            fts_table = await database.fts_table(table)
            if fts_table:
                # Check user has permission to view that table
                try:
                    await datasette.ensure_permission(
                        action="view-table",
                        resource=TableResource(database=database.name, table=table),
                        actor=request.actor,
                    )
                    yield (db_name, table)
                except Forbidden:
                    pass


async def has_searchable_tables(datasette, request):
    # Return True on the first table we find
    async for _ in iterate_searchable_tables(datasette, request):
        return True
    return False


async def get_searchable_tables(datasette, request):
    tables = []
    async for table in iterate_searchable_tables(datasette, request):
        tables.append(table)
    return tables
