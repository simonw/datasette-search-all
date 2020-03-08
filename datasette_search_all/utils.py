async def get_searchable_tables(datasette):
    searchable_tables = []
    for db_name, database in datasette.databases.items():
        hidden_tables = set(await database.hidden_table_names())
        for table in await database.table_names():
            if table in hidden_tables:
                continue
            fts_table = await database.fts_table(table)
            if fts_table:
                searchable_tables.append((db_name, table))
    return searchable_tables
