from pantomath_sdk import FTP, PlatformTypes


def test_ftp_good():
    test_node = FTP(uri="https://testing.dev/ftp/", name="ftp Unit Test")
    assert test_node.get_name() == "ftp Unit Test"
    assert test_node.get_type() == "FTP"
    assert test_node.get_fully_qualified_object_name() == "https://testing.dev/ftp/"
    assert test_node.get_platform_type() == PlatformTypes.UNKNOWN.value
