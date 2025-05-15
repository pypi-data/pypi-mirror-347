from pantomath_sdk import SynapseActivity, PlatformTypes, AssetPathTypes, Asset


def test_synapse_activity_good():
    node = SynapseActivity(
        name="SynapseActivity Unit Test", pipeline_id="3674798497356"
    )
    assert node.get_name() == "SynapseActivity Unit Test"
    assert node.get_type() == "ACTIVITY"
    assert (
        node.get_fully_qualified_object_name()
        == "3674798497356/activities/synapseactivity unit test"
    )
    assert node.get_platform_type() == PlatformTypes.SYNAPSE.value

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SYNAPSE", "type": "PLATFORM"}, {"depth": 1, "name": "Synapse Connection", "type": "CONNECTION"}]'
    )


def test_custom_synapse_activity_asset_path():
    node = SynapseActivity(
        name="SynapseActivity Unit Test",
        pipeline_id="3674798497356",
        assets=[Asset(name="Factory", type=AssetPathTypes.FACTORY.value)],
    )

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SYNAPSE", "type": "PLATFORM"}, {"depth": 1, "name": "Synapse Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
