from pantomath_sdk import AstroDag
from pantomath_sdk.enums.platform_types import PlatformTypes


def test_astro_dag_good():
    test_node = AstroDag(
        host_name="https://testing.dev/astro_dags/", name="Astro Unit Test"
    )
    assert test_node.get_name() == "Astro Unit Test"
    assert test_node.get_type() == "DAG"
    assert (
        test_node.get_fully_qualified_object_name()
        == "https%3a//testing.dev/astro_dags//astro%20unit%20test"
    )
    assert test_node.get_platform_type() == PlatformTypes.ASTRO.value
