from pantomath_sdk import PowerBiDataFlow, PlatformTypes
from pantomath_sdk.enums.asset_path import AssetPathTypes
from pantomath_sdk.model.asset_path.asset_path import Asset


def test_power_bi_data_flow_good():
    node = PowerBiDataFlow(
        name="PowerBiDataFlow Unit Test",
        group_id="245632457634",
        object_id="5785678976809",
    )
    assert node.get_name() == "PowerBiDataFlow Unit Test"
    assert node.get_type() == "POWER_BI_DATAFLOW"
    assert (
        node.get_fully_qualified_object_name()
        == "app.powerbi.com/groups/245632457634/dataflows/5785678976809"
    )
    assert node.get_platform_type() == PlatformTypes.POWERBI.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "POWERBI", "type": "PLATFORM"}, {"depth": 1, "name": "PowerBI Connection", "type": "CONNECTION"}]'
    )


def test_custom_power_bi_dataflow_asset_path_good():
    node = PowerBiDataFlow(
        name="PowerBiDataFlow Unit Test",
        group_id="245632457634",
        object_id="5785678976809",
        assets=[
            Asset(name="Factory", type=AssetPathTypes.FACTORY.value),
        ],
    )

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "POWERBI", "type": "PLATFORM"}, {"depth": 1, "name": "PowerBI Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
