import unittest
from pantomath_sdk import AssetPath, Asset, AssetPathTypes


class TestAssetPath(unittest.TestCase):
    def setUp(self):
        self.platform_type = "TestPlatform"
        self.connection_name = "TestConnection"
        self.account = "TestAccount"
        self.agent = "TestAgent"
        self.asset_path = AssetPath(
            self.platform_type,
            self.connection_name,
            assets=[
                Asset(self.account, AssetPathTypes.ACCOUNT.value),
                Asset(self.agent, AssetPathTypes.AGENT.value),
            ],
        )

    def test_initial_assets(self):
        self.assertEqual(self.asset_path.assets[0].name, self.platform_type)
        self.assertEqual(self.asset_path.assets[0].type, AssetPathTypes.PLATFORM.value)
        self.assertEqual(self.asset_path.assets[1].name, self.connection_name)
        self.assertEqual(
            self.asset_path.assets[1].type, AssetPathTypes.CONNECTION.value
        )

        # Test user defined assets
        self.assertEqual(self.asset_path.assets[2].name, self.account)
        self.assertEqual(self.asset_path.assets[2].type, AssetPathTypes.ACCOUNT.value)
        self.assertEqual(self.asset_path.assets[3].name, self.agent)
        self.assertEqual(self.asset_path.assets[3].type, AssetPathTypes.AGENT.value)

    def test_get_path(self):
        expected_path = (
            f"{self.platform_type}/{self.connection_name}/{self.account}/{self.agent}"
        )
        self.assertEqual(self.asset_path.get_path, expected_path)

    def test_get_asset_path(self):
        assets = self.asset_path.get_asset_path()
        self.assertIsInstance(assets, object)
        self.assertEqual(len(assets), 4)

    def test_str(self):
        # noqa: For testing purposes
        expected_str = '[{"depth": 0, "name": "TestPlatform", "type": "PLATFORM"}, {"depth": 1, "name": "TestConnection", "type": "CONNECTION"}, {"depth": 2, "name": "TestAccount", "type": "ACCOUNT"}, {"depth": 3, "name": "TestAgent", "type": "AGENT"}]'  # noqa
        self.assertEqual(str(self.asset_path), expected_str)

    def test_append_asset(self):
        new_asset_name = "TestContainer"
        new_asset_type = AssetPathTypes.CONTAINER.value
        self.asset_path.append_asset(new_asset_name, new_asset_type)
        self.assertEqual(len(self.asset_path.assets), 5)
        self.assertEqual(self.asset_path.assets[4].name, new_asset_name)
        self.assertEqual(self.asset_path.assets[4].type, new_asset_type)
