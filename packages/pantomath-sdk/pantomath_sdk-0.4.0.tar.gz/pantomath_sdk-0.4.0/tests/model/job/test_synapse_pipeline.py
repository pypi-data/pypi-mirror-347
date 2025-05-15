from pantomath_sdk import SynapsePipeline, PlatformTypes, AssetPathTypes, Asset


def test_synapse_pipeline_good():
    node = SynapsePipeline(
        name="SynapsePipeline Unit Test", pipeline_id="3674798497356"
    )
    assert node.get_name() == "SynapsePipeline Unit Test"
    assert node.get_type() == "PIPELINE"
    assert node.get_fully_qualified_object_name() == "3674798497356"
    assert node.get_platform_type() == PlatformTypes.SYNAPSE.value

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SYNAPSE", "type": "PLATFORM"}, {"depth": 1, "name": "Synapse Connection", "type": "CONNECTION"}]'
    )


def test_custom_synapse_pipeline_asset_path_good():
    node = SynapsePipeline(
        name="SynapsePipeline Unit Test",
        pipeline_id="3674798497356",
        assets=[Asset(name="Factory", type=AssetPathTypes.FACTORY.value)],
    )

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SYNAPSE", "type": "PLATFORM"}, {"depth": 1, "name": "Synapse Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
