from pantomath_sdk import (
    FivetranConnectorConstructor,
    PlatformTypes,
    Asset,
    AssetPathTypes,
)


def test_fivetran_connector_constructor_good():
    node = FivetranConnectorConstructor(
        name="FivetranConnectorConstructor Unit Test",
    )
    assert node.get_name() == "FivetranConnectorConstructor Unit Test"
    assert node.get_type() == "FIVETRAN_CONNECTOR"
    assert (
        node.get_fully_qualified_object_name()
        == "FivetranConnectorConstructor Unit Test"
    )
    assert node.get_platform_type() == PlatformTypes.FIVETRAN.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "FIVETRAN", "type": "PLATFORM"}, {"depth": 1, "name": "Fivetran Connection", "type": "CONNECTION"}]'
    )


def test_custom_fivetran_connector_asset_path_good():
    node = FivetranConnectorConstructor(
        name="FivetranConnectorConstructor Unit Test",
        assets=[
            Asset("Factory", AssetPathTypes.FACTORY.value),
        ],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "FIVETRAN", "type": "PLATFORM"}, {"depth": 1, "name": "Fivetran Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
