from pantomath_sdk import AstroDag, PlatformTypes, Asset, AssetPathTypes


def test_astro_dag_good():
    node = AstroDag(
        host_name="https://testing.dev/astro_dags/",
        name="Astro Unit Test",
    )
    assert node.get_name() == "Astro Unit Test"
    assert node.get_type() == "DAG"
    assert (
        node.get_fully_qualified_object_name()
        == "https%3a//testing.dev/astro_dags//astro%20unit%20test"
    )
    assert node.get_platform_type() == PlatformTypes.ASTRO.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "ASTRONOMER", "type": "PLATFORM"}, {"depth": 1, "name": "https://testing.dev/astro_dags/", "type": "CONNECTION"}]'
    )


def test_custom_astro_dag_asset_path():
    node = AstroDag(
        host_name="https://testing.dev/astro_dags/",
        name="Astro Unit Test",
        assets=[
            Asset(name="Organization A", type=AssetPathTypes.ORGANIZATION.value),
            Asset(name="Container A", type=AssetPathTypes.CONTAINER.value),
        ],
    )
    # noqa
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "ASTRONOMER", "type": "PLATFORM"}, {"depth": 1, "name": "https://testing.dev/astro_dags/", "type": "CONNECTION"}, {"depth": 2, "name": "Organization A", "type": "ORGANIZATION"}, {"depth": 3, "name": "Container A", "type": "CONTAINER"}]'
    )
