from pantomath_sdk import SqlProcedure, PlatformTypes, AssetPathTypes, Asset


def test_sql_procedure_good():
    node = SqlProcedure(
        name="SqlProcedure Unit Test",
        schema="schema",
        database="database",
        port=42,
        host="host",
    )
    assert node.get_name() == "SqlProcedure Unit Test"
    assert node.get_type() == "SQL_PROCEDURE"
    assert (
        node.get_fully_qualified_object_name()
        == "host:42.database.schema.SqlProcedure Unit Test"
    )
    assert node.get_platform_type() == PlatformTypes.SQL_SERVER.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SQL_SERVER", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}]'
    )


def test_custom_sql_procedure_asset_path_good():
    node = SqlProcedure(
        name="SqlProcedure Unit Test",
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
