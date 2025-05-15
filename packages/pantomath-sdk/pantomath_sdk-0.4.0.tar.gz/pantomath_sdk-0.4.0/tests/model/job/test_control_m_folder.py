from pantomath_sdk import ControlMFolder, PlatformTypes


def test_control_m_folder_good():
    node = ControlMFolder(
        host="mockHost",
        server="mockserver",
        folder_hierarchy=["A", "B"],
        name="ControlMFolder Unit Test",
    )
    assert node.get_name() == "ControlMFolder Unit Test"
    assert node.get_type() == "FOLDER"
    assert (
        node.get_fully_qualified_object_name()
        == "mockhost.mockserver.a.b.controlmfolder%20unit%20test"
    )
    assert node.get_platform_type() == PlatformTypes.CONTROL_M.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "CONTROL_M", "type": "PLATFORM"}, {"depth": 1, "name": "mockHost", "type": "CONNECTION"}, {"depth": 2, "name": "mockserver", "type": "SERVER"}, {"depth": 3, "name": "A", "type": "FOLDER"}, {"depth": 4, "name": "B", "type": "FOLDER"}]'
    )


def test_control_m_folder_good_no_optional():
    node = ControlMFolder(
        host="mockHost",
        server="mockserver",
        name="ControlMFolder Unit Test",
    )
    assert node.get_name() == "ControlMFolder Unit Test"
    assert node.get_type() == "FOLDER"
    assert (
        node.get_fully_qualified_object_name()
        == "mockhost.mockserver.controlmfolder%20unit%20test"
    )
    assert node.get_platform_type() == PlatformTypes.CONTROL_M.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "CONTROL_M", "type": "PLATFORM"}, {"depth": 1, "name": "mockHost", "type": "CONNECTION"}, {"depth": 2, "name": "mockserver", "type": "SERVER"}]'
    )
