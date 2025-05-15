from pantomath_sdk import TableauWorkbook, PlatformTypes


def test_tableau_workbook_good():
    test_node = TableauWorkbook(
        host="host",
        uri="uri",
        name="TableauWorkbook Unit Test",
    )
    assert test_node.get_name() == "TableauWorkbook Unit Test"
    assert test_node.get_type() == "TABLEAU_WORKBOOK"
    assert test_node.get_fully_qualified_object_name() == "host/uri"
    assert test_node.get_platform_type() == PlatformTypes.TABLEAU.value
