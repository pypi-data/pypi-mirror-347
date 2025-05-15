from pantomath_sdk import ControlMJob, PlatformTypes


def test_control_m_folder_good():
    node = ControlMJob(
        host="mockHost",
        server="mockserver",
        folder_hierarchy=["A", "B", "C"],
        name="ControlMJob Unit Test",
    )
    assert node.get_name() == "ControlMJob Unit Test"
    assert node.get_type() == "JOB"
    assert (
        node.get_fully_qualified_object_name()
        == "mockhost.mockserver.a.b.c.controlmjob%20unit%20test"
    )
    assert node.get_platform_type() == PlatformTypes.CONTROL_M.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "CONTROL_M", "type": "PLATFORM"}, {"depth": 1, "name": "mockHost", "type": "CONNECTION"}, {"depth": 2, "name": "mockserver", "type": "SERVER"}, {"depth": 3, "name": "A", "type": "FOLDER"}, {"depth": 4, "name": "B", "type": "FOLDER"}, {"depth": 5, "name": "C", "type": "FOLDER"}]'
    )


def test_control_m_folder_good_no_optional():
    node = ControlMJob(
        host="mockHost",
        server="mockserver",
        name="ControlMJob Unit Test",
    )
    assert node.get_name() == "ControlMJob Unit Test"
    assert node.get_type() == "JOB"
    assert (
        node.get_fully_qualified_object_name()
        == "mockhost.mockserver.controlmjob%20unit%20test"
    )
    assert node.get_platform_type() == PlatformTypes.CONTROL_M.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "CONTROL_M", "type": "PLATFORM"}, {"depth": 1, "name": "mockHost", "type": "CONNECTION"}, {"depth": 2, "name": "mockserver", "type": "SERVER"}]'
    )
