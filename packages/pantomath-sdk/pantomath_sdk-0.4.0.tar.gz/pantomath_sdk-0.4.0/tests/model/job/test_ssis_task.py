from pantomath_sdk import SSISTask, PlatformTypes, AssetPathTypes, Asset


def test_ssis_task_good():
    node = SSISTask(
        executable_name="_executableName",
        parent_executable_name="_parentExecutableName",
        project_name="projectName",
        folder_name="_folderName",
    )
    assert node.get_name() == "_executableName"
    assert node.get_type() == "TASK"
    assert (
        node.get_fully_qualified_object_name()
        == "_foldername.projectname._parentexecutablename._executablename"
    )
    assert node.get_platform_type() == PlatformTypes.SSIS.value

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SSIS", "type": "PLATFORM"}, {"depth": 1, "name": "projectName", "type": "CONNECTION"}]'
    )


def test_custom_ssis_task_asset_path_good():
    node = SSISTask(
        executable_name="_executableName",
        parent_executable_name="_parentExecutableName",
        project_name="projectName",
        folder_name="_folderName",
        assets=[Asset(name="Factory", type=AssetPathTypes.FACTORY.value)],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SSIS", "type": "PLATFORM"}, {"depth": 1, "name": "projectName", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
