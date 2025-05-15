from pantomath_sdk import DataikuProject, PlatformTypes
from pantomath_sdk.enums.asset_path import AssetPathTypes
from pantomath_sdk.model.asset_path.asset_path import Asset


def test_dataiku_project_good():
    test_node = DataikuProject(
        host_name="host",
        project_key="96868946864896189",
        project_label="DataikuProject Unit Test",
    )
    assert test_node.get_name() == "DataikuProject Unit Test"
    assert test_node.get_type() == "PROJECT"
    assert (
        test_node.get_fully_qualified_object_name() == "host/projects/96868946864896189"
    )
    assert test_node.get_platform_type() == PlatformTypes.DATAIKU.value

    assert (
        test_node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DATAIKU", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}]'
    )


def test_custom_dataiku_project_asset_path_good():
    test_node = DataikuProject(
        host_name="host",
        project_key="96868946864896189",
        project_label="DataikuProject Unit Test",
        assets=[
            Asset("Factory", AssetPathTypes.FACTORY.value),
        ],
    )
    assert (
        test_node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DATAIKU", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
