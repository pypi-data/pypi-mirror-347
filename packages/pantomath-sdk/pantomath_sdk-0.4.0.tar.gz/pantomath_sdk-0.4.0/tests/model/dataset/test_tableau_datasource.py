from pantomath_sdk import TableauDatasource, PlatformTypes


def test_tableau_datasource_good():
    test_node = TableauDatasource(
        host="host",
        uri="uri",
        name="TableauDatasource Unit Test",
    )
    assert test_node.get_name() == "TableauDatasource Unit Test"
    assert test_node.get_type() == "TABLEAU_DATASOURCE"
    assert test_node.get_fully_qualified_object_name() == "host/uri"
    assert test_node.get_platform_type() == PlatformTypes.TABLEAU.value
