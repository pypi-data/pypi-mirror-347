from pantomath_sdk import SqlView, PlatformTypes


def test_sql_view_good():
    test_node = SqlView(
        host="host",
        port=42,
        database="database",
        schema="Schema",
        name="SqlView Unit Test",
    )
    assert test_node.get_name() == "SqlView Unit Test"
    assert test_node.get_type() == "SQL_VIEW"
    assert (
        test_node.get_fully_qualified_object_name()
        == "host:42.database.Schema.SqlView Unit Test"
    )
    assert test_node.get_platform_type() == PlatformTypes.SQL_SERVER.value
