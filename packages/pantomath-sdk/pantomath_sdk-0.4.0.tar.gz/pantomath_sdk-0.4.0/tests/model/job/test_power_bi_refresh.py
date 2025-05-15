from pantomath_sdk import PowerBIRefresh, PlatformTypes
from pantomath_sdk.enums.asset_path import AssetPathTypes
from pantomath_sdk.model.asset_path.asset_path import Asset


def test_power_bi_refresh_good():
    node = PowerBIRefresh(
        name="PowerBIRefresh Unit Test",
        refresh_schedule_context="refresh_schedule_context",
        dataset_id="5785678976809",
    )
    assert node.get_name() == "PowerBIRefresh Unit Test"
    assert node.get_type() == "POWER_BI_REFRESH"
    assert (
        node.get_fully_qualified_object_name()
        == "refresh_schedule_context/5785678976809/powerbirefresh_unit_test"
    )
    assert node.get_platform_type() == PlatformTypes.POWERBI.value

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "POWERBI", "type": "PLATFORM"}, {"depth": 1, "name": "PowerBI Connection", "type": "CONNECTION"}]'
    )


def test_custom_power_bi_refresh_asset_path_good():
    node = PowerBIRefresh(
        name="PowerBIRefresh Unit Test",
        refresh_schedule_context="refresh_schedule_context",
        dataset_id="5785678976809",
        assets=[Asset(name="Factory", type=AssetPathTypes.FACTORY.value)],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "POWERBI", "type": "PLATFORM"}, {"depth": 1, "name": "PowerBI Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
