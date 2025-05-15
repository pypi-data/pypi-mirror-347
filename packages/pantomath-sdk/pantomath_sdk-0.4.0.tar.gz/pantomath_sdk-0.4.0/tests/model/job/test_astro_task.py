from pantomath_sdk import AstroTask, PlatformTypes, Asset, AssetPathTypes


def test_astro_task_good():
    node = AstroTask(
        host_name="https://testing.dev/astro_dags/",
        name="Astro Unit Test",
        dag_name="Unit Test Dag",
    )
    assert node.get_name() == "Astro Unit Test"
    assert node.get_type() == "TASK"
    assert (
        node.get_fully_qualified_object_name()
        == "https%3a//testing.dev/astro_dags//unit%20test%20dag/astro%20unit%20test"
    )
    assert node.get_platform_type() == PlatformTypes.ASTRO.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "ASTRONOMER", "type": "PLATFORM"}, {"depth": 1, "name": "https://testing.dev/astro_dags/", "type": "CONNECTION"}]'
    )


def test_custom_astro_task_asset_path():
    node = AstroTask(
        host_name="https://testing.dev/astro_dags/",
        name="Astro Unit Test",
        dag_name="Unit Test Dag",
        assets=[
            Asset(name="Organization A", type=AssetPathTypes.ORGANIZATION.value),
            Asset(name="Container A", type=AssetPathTypes.CONTAINER.value),
        ],
    )

    print(node.get_asset_path().__str__())
    # noqa
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "ASTRONOMER", "type": "PLATFORM"}, {"depth": 1, "name": "https://testing.dev/astro_dags/", "type": "CONNECTION"}, {"depth": 2, "name": "Organization A", "type": "ORGANIZATION"}, {"depth": 3, "name": "Container A", "type": "CONTAINER"}]'
    )
