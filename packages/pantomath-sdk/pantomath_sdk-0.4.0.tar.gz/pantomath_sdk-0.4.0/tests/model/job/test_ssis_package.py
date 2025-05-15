from pantomath_sdk import SSISPackage, PlatformTypes, AssetPathTypes, Asset


def test_ssis_package_good():
    node = SSISPackage(
        name="SSISPackage Unit Test",
        folder_name="_folderName",
        project_name="projectName",
    )
    assert node.get_name() == "SSISPackage Unit Test"
    assert node.get_type() == "PACKAGE"
    assert (
        node.get_fully_qualified_object_name()
        == "_foldername.projectname.ssispackage unit test"
    )
    assert node.get_platform_type() == PlatformTypes.SSIS.value

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SSIS", "type": "PLATFORM"}, {"depth": 1, "name": "projectName", "type": "CONNECTION"}]'
    )


def test_custom_ssis_package_asset_path_good():
    node = SSISPackage(
        name="SSISPackage Unit Test",
        folder_name="_folderName",
        project_name="projectName",
        assets=[Asset(name="Factory", type=AssetPathTypes.FACTORY.value)],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "SSIS", "type": "PLATFORM"}, {"depth": 1, "name": "projectName", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
