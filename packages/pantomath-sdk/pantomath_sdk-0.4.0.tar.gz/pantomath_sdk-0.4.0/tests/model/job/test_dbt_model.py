from pantomath_sdk import DBTModelConstructor, PlatformTypes, Asset


def test_dbt_model_good():
    node = DBTModelConstructor(
        host="cloud.getdbt.com",
        account_id=146523457734567,
        project_name="DBTModelConstructor Unit Test",
        model_name="DBTModelConstructor Unit Test Model",
    )
    assert node.get_name() == "DBTModelConstructor Unit Test Model"
    assert node.get_type() == "DBT_MODEL"
    assert (
        node.get_fully_qualified_object_name()
        == "cloud.getdbt.com/#/accounts/146523457734567/project/dbtmodelconstructor unit test/model/dbtmodelconstructor unit test model"
    )
    assert node.get_platform_type() == PlatformTypes.DBT.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DBT", "type": "PLATFORM"}, {"depth": 1, "name": "Account Id - 146523457734567", "type": "CONNECTION"}]'
    )


def test_custom_dbt_model_asset_path_good():
    node = DBTModelConstructor(
        host="cloud.getdbt.com",
        account_id=146523457734567,
        project_name="DBTModelConstructor Unit Test",
        model_name="DBTModelConstructor Unit Test Model",
        assets=[
            Asset("Factory", "FACTORY"),
        ],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DBT", "type": "PLATFORM"}, {"depth": 1, "name": "Account Id - 146523457734567", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
