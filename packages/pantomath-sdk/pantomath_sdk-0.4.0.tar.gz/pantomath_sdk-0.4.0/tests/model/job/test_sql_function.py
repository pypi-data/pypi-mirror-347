from pantomath_sdk import SqlFunction, PlatformTypes, AssetPathTypes, Asset


def test_sql_function_good():
    node = SqlFunction(
        name="SqlFunction Unit Test",
        schema="schema",
        database="database",
        port=42,
        host="host",
    )
    assert node.get_name() == "SqlFunction Unit Test"
    assert node.get_type() == "SQL_FUNCTION"
    assert (
        node.get_fully_qualified_object_name()
        == "host:42.database.schema.SqlFunction Unit Test"
    )
    assert node.get_platform_type() == PlatformTypes.SQL_SERVER.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SQL_SERVER", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}]'
    )


def test_custom_sql_function_asset_path_good():
    node = SqlFunction(
        name="SqlFunction Unit Test",
        schema="schema",
        database="database",
        port=42,
        host="host",
        assets=[Asset(name="Factory", type=AssetPathTypes.FACTORY.value)],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SQL_SERVER", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
