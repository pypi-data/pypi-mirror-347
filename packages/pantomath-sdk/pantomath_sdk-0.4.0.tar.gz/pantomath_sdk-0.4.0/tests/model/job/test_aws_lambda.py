from pantomath_sdk import AWSLambda, PlatformTypes, Asset, AssetPathTypes


def test_aws_lambda_good():
    node = AWSLambda(
        name="AWSLambda Unit Test",
    )
    assert node.get_name() == "AWSLambda Unit Test"
    assert node.get_type() == "AWS_LAMBDA"
    assert node.get_fully_qualified_object_name() == "AWSLambda Unit Test"
    assert node.get_platform_type() == PlatformTypes.AWS.value

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "AWS", "type": "PLATFORM"}, {"depth": 1, "name": "AWS Connection", "type": "CONNECTION"}]'
    )


def test_custom_aws_lambda_asset_path():
    node = AWSLambda(
        name="AWSLambda Unit Test",
        assets=[
            Asset(name="Organization A", type=AssetPathTypes.ORGANIZATION.value),
            Asset(name="Container A", type=AssetPathTypes.CONTAINER.value),
        ],
    )

    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "AWS", "type": "PLATFORM"}, {"depth": 1, "name": "AWS Connection", "type": "CONNECTION"}, {"depth": 2, "name": "Organization A", "type": "ORGANIZATION"}, {"depth": 3, "name": "Container A", "type": "CONTAINER"}]'
    )
