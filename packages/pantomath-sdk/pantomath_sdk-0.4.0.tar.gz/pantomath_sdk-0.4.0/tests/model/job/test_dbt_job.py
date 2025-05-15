from pantomath_sdk import DBTJobConstructor, PlatformTypes, Asset, AssetPathTypes


def test_dbt_job_good():
    node = DBTJobConstructor(
        account_id=146523457734567,
        host="cloud.getdbt.com",
        name="DBTJobConstructor Unit Test",
        job_id=12453576758,
        project_name="DBTJobConstructor Project",
    )
    assert node.get_name() == "DBTJobConstructor Unit Test"
    assert node.get_type() == "JOB"
    assert (
        node.get_fully_qualified_object_name()
        == "cloud.getdbt.com/#/accounts/146523457734567.dbtjobconstructor project."
        "dbtjobconstructor unit test.12453576758"
    )
    assert node.get_platform_type() == PlatformTypes.DBT.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DBT", "type": "PLATFORM"}, {"depth": 1, "name": "DBTJobConstructor Project", "type": "CONNECTION"}]'
    )


def test_custom_dbt_job_asset_path_good():
    node = DBTJobConstructor(
        account_id=146523457734567,
        name="DBTJobConstructor Unit Test",
        host="cloud.getdbt.com",
        job_id=12453576758,
        project_name="DBTJobConstructor Project",
        assets=[
            Asset("Factory", AssetPathTypes.FACTORY.value),
        ],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DBT", "type": "PLATFORM"}, {"depth": 1, "name": "DBTJobConstructor Project", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
