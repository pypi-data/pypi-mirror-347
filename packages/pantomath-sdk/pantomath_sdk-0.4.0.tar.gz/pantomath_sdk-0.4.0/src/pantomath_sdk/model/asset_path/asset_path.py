from pantomath_sdk.enums.asset_path import AssetPathTypes
from typing import List, Union
import json


class Asset:
    def __init__(self, name: str, type: AssetPathTypes):
        self.name = name
        self.type = type


class AssetPathObject:
    def __init__(self, depth: int, name: str, type: AssetPathTypes):
        self.depth = depth
        self.name = name
        self.type = type


class AssetPath:
    def __init__(
        self,
        platform_type: str,
        connection_name: str,
        assets: Union[List[Asset], None] = None,
    ):
        self.assets: List[AssetPathObject] = [
            AssetPathObject(
                depth=0, name=platform_type, type=AssetPathTypes.PLATFORM.value
            ),
            AssetPathObject(
                depth=1, name=connection_name, type=AssetPathTypes.CONNECTION.value
            ),
        ]

        if assets is not None:
            for asset in assets:
                self.append_asset(asset.name, asset.type)

    @property
    def get_path(self) -> str:
        return "/".join(
            asset.name for asset in sorted(self.assets, key=lambda x: x.depth)
        )

    @property
    def get_asset_paths(self) -> List[AssetPathObject]:
        return self.assets

    def __str__(self) -> str:
        return json.dumps([asset.__dict__ for asset in self.assets])

    def append_asset(self, name: str, type: AssetPathTypes) -> "AssetPath":
        current_depth = len(self.assets)
        asset = AssetPathObject(depth=current_depth, name=name, type=type)
        self.assets.append(asset)
        return self

    def get_asset_path(self):
        asset_paths = []
        for asset in self.assets:
            asset_paths.append(
                {
                    "depth": asset.depth,
                    "name": asset.name,
                    "type": asset.type,
                }
            )
        return asset_paths
