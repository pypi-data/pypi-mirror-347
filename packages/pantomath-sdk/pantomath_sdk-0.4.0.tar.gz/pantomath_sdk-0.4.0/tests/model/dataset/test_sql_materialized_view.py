from pantomath_sdk import SqlMaterializedView, PlatformTypes


def test_sql_materilizaed_view_good():
    test_node = SqlMaterializedView(
        host="host",
        port=42,
        database="database",
        schema="Schema",
        name="SqlMaterializedView Unit Test",
    )
    assert test_node.get_name() == "SqlMaterializedView Unit Test"
    assert test_node.get_type() == "SQL_MATERIALIZED_VIEW"
    assert (
        test_node.get_fully_qualified_object_name()
        == "host:42.database.Schema.SqlMaterializedView Unit Test"
    )
    assert test_node.get_platform_type() == PlatformTypes.SQL_SERVER.value
