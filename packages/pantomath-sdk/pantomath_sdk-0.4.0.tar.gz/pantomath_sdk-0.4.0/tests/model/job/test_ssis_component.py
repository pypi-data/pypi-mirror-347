from pantomath_sdk import SSISComponent, PlatformTypes, AssetPathTypes, Asset


def test_ssis_component_good():
    node = SSISComponent(
        name="SSISComponent Unit Test",
        folder_name="_folderName",
        execution_path="_executionPath",
        project_name="projectName",
    )
    assert node.get_name() == "SSISComponent Unit Test"
    assert node.get_type() == "COMPONENT"
    assert (
        node.get_fully_qualified_object_name()
        == "_foldername.projectname._executionpath.ssiscomponent unit test"
    )
    assert node.get_platform_type() == PlatformTypes.SSIS.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SSIS", "type": "PLATFORM"}, {"depth": 1, "name": "projectName", "type": "CONNECTION"}]'
    )


def test_custom_ssis_component_asset_path_good():
    node = SSISComponent(
        name="SSISComponent Unit Test",
        folder_name="_folderName",
        execution_path="_executionPath",
        project_name="projectName",
        assets=[Asset(name="Factory", type=AssetPathTypes.FACTORY.value)],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SSIS", "type": "PLATFORM"}, {"depth": 1, "name": "projectName", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
