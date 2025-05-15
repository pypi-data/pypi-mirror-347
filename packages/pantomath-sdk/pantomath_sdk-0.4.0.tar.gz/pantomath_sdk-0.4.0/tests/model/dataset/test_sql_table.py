from pantomath_sdk import SqlTable, PlatformTypes


def test_sql_table_good():
    test_node = SqlTable(
        host="host",
        port=42,
        database="database",
        schema="Schema",
        name="SqlTable Unit Test",
    )
    assert test_node.get_name() == "SqlTable Unit Test"
    assert test_node.get_type() == "SQL_TABLE"
    assert (
        test_node.get_fully_qualified_object_name()
        == "host:42.database.Schema.SqlTable Unit Test"
    )
    assert test_node.get_platform_type() == PlatformTypes.SQL_SERVER.value
