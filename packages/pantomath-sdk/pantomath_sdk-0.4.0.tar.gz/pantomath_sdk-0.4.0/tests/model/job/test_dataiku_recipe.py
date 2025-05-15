from pantomath_sdk import DataikuRecipe, PlatformTypes
from pantomath_sdk.enums.asset_path import AssetPathTypes
from pantomath_sdk.model.asset_path.asset_path import Asset


def test_dataiku_model_good():
    test_node = DataikuRecipe(
        host_name="host",
        project_key="96868946864896189",
        recipe_name="DataikuRecipe Unit Test",
    )
    assert test_node.get_name() == "DataikuRecipe Unit Test"
    assert test_node.get_type() == "RECIPE"
    assert (
        test_node.get_fully_qualified_object_name()
        == "host/projects/96868946864896189/recipes/%24dataikurecipe%20unit%20test"
    )
    assert test_node.get_platform_type() == PlatformTypes.DATAIKU.value
    assert (
        test_node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DATAIKU", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}]'
    )


def test_custom_dataiku_project_asset_path_good():
    test_node = DataikuRecipe(
        host_name="host",
        project_key="96868946864896189",
        recipe_name="DataikuRecipe Unit Test",
        assets=[
            Asset("Factory", AssetPathTypes.FACTORY.value),
        ],
    )
    assert (
        test_node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DATAIKU", "type": "PLATFORM"}, {"depth": 1, "name": "host", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
