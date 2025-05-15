from pantomath_sdk import (
    TableauExtractRefreshTask,
    PlatformTypes,
    AssetPathTypes,
    Asset,
)


def test_tableau_extract_refresh_task_good():
    node = TableauExtractRefreshTask(
        name="TableauExtractRefreshTask Unit Test",
        site_id="site_id",
        refresh_id="refresh_id",
        host="host",
    )
    assert node.get_name() == "TableauExtractRefreshTask Unit Test"
    assert node.get_type() == "TABLEAU_EXTRACT_REFRESH_TASK"
    assert node.get_fully_qualified_object_name() == "host/site/site_id/task/refresh_id"
    assert node.get_platform_type() == PlatformTypes.TABLEAU.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "TABLEAU", "type": "PLATFORM"}, {"depth": 1, "name": "Tableau Connection", "type": "CONNECTION"}]'
    )


def test_custom_tableau_extract_refresh_task_asset_path():
    node = TableauExtractRefreshTask(
        name="TableauExtractRefreshTask Unit Test",
        site_id="site_id",
        refresh_id="refresh_id",
        host="host",
        assets=[Asset(name="Workbook", type=AssetPathTypes.WORKFLOW.value)],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "TABLEAU", "type": "PLATFORM"}, {"depth": 1, "name": "Tableau Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Workbook", "type": "WORKFLOW"}]'
    )
