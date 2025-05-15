from pantomath_sdk import ADFPipeline, PlatformTypes, AssetPathTypes, Asset


def test_adf_pipeline_good():
    node = ADFPipeline(
        pipeline_id=13465478579,
        name="ADFPipeline Unit Test",
    )
    assert node.get_name() == "ADFPipeline Unit Test"
    assert node.get_type() == "ADF_PIPELINE"
    assert node.get_fully_qualified_object_name() == "13465478579"
    assert node.get_platform_type() == PlatformTypes.ADF.value

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "ADF", "type": "PLATFORM"}, {"depth": 1, "name": "Azure Data Factory Connection", "type": "CONNECTION"}]'
    )


def test_custom_adf_pipeline_asset_path_good():
    node = ADFPipeline(
        pipeline_id=13465478579,
        name="ADFPipeline Unit Test",
        assets=[
            Asset(name="Organization A", type=AssetPathTypes.ORGANIZATION.value),
            Asset(name="Container A", type=AssetPathTypes.CONTAINER.value),
        ],
    )
    # noqa
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "ADF", "type": "PLATFORM"}, {"depth": 1, "name": "Azure Data Factory Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Organization A", "type": "ORGANIZATION"}, {"depth": 3, "name": "Container A", "type": "CONTAINER"}]'
    )
