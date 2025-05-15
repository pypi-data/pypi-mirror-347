from pantomath_sdk import ADFActivity, PlatformTypes, Asset, AssetPathTypes


def test_adf_activity_good():
    node = ADFActivity(
        pipeline_id=13465478579, name="ADFActivity Unit Test", assets=None
    )
    assert node.get_name() == "ADFActivity Unit Test"
    assert node.get_type() == "ADF_ACTIVITY"
    assert (
        node.get_fully_qualified_object_name()
        == "13465478579/activities/adfactivity%20unit%20test"
    )
    assert node.get_platform_type() == PlatformTypes.ADF.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "ADF", "type": "PLATFORM"}, {"depth": 1, "name": "Azure Data Factory Connection", "type": "CONNECTION"}]'
    )


def test_custom_asset_path_adf_activity_good():
    node = ADFActivity(
        pipeline_id=13465478579,
        name="ADFActivity Unit Test",
        assets=[Asset("Channel A", AssetPathTypes.CHANNEL.value)],
    )

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "ADF", "type": "PLATFORM"}, {"depth": 1, "name": "Azure Data Factory Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Channel A", "type": "CHANNEL"}]'
    )
