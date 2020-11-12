async def iterate_searchable_tables(datasette):
    for db_name, database in datasette.databases.items():
        hidden_tables = set(await database.hidden_table_names())
        for table in await database.table_names():
            if table in hidden_tables:
                continue
            fts_table = await database.fts_table(table)
            if fts_table:
                yield (db_name, table)


async def has_searchable_tables(datasette):
    # Return True on the first table we find
    async for _ in iterate_searchable_tables(datasette):
        return True
    return False


async def get_searchable_tables(datasette):
    tables = []
    async for table in iterate_searchable_tables(datasette):
        tables.append(table)
    return tables
