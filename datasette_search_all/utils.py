async def iterate_searchable_tables(datasette, actor):
    for db_name, database in datasette.databases.items():
        perm_args = (actor, "view-database", (db_name,))
        if not await datasette.permission_allowed(*perm_args):
            continue
        hidden_tables = set(await database.hidden_table_names())
        for table in await database.table_names():
            if table in hidden_tables:
                continue
            perm_args = (actor, "view-table", (db_name, table))
            if not await datasette.permission_allowed(*perm_args):
                continue
            fts_table = await database.fts_table(table)
            if fts_table:
                yield (db_name, table)


async def has_searchable_tables(datasette, actor):
    # Return True on the first table we find
    async for _ in iterate_searchable_tables(datasette, actor):
        return True
    return False


async def get_searchable_tables(datasette, actor):
    tables = []
    async for table in iterate_searchable_tables(datasette, actor):
        tables.append(table)
    return tables
