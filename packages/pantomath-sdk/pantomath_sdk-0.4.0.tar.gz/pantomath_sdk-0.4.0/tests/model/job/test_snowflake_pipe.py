from pantomath_sdk import SnowflakePipe, PlatformTypes, AssetPathTypes, Asset


def test_snowflake_pipe_good():
    node = SnowflakePipe(
        name="SnowflakePipe Unit Test",
        schema="schema",
        database="database",
        port=42,
        host="host",
    )
    assert node.get_name() == "SnowflakePipe Unit Test"
    assert node.get_type() == "SNOWFLAKE_PIPE"
    assert (
        node.get_fully_qualified_object_name()
        == "host:42.database.schema.SnowflakePipe Unit Test"
    )
    assert node.get_platform_type() == PlatformTypes.SNOWFLAKE.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SNOWFLAKE", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}]'
    )


def test_custom_snowflake_pipe_asset_path_good():
    node = SnowflakePipe(
        name="SnowflakePipe Unit Test",
        schema="schema",
        database="database",
        port=42,
        host="host",
        assets=[Asset(name="Factory", type=AssetPathTypes.FACTORY.value)],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SNOWFLAKE", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
