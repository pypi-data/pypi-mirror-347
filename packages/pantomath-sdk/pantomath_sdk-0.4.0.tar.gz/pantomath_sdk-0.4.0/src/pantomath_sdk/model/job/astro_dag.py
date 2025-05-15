from typing import Union, List
from pantomath_sdk.enums.platform_types import PlatformTypes
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath
from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
import pantomath_sdk.util as util


class AstroDag(Job):
    """AstroDag's Job Class used for getting the required infomation for Pantomath
    :param host_name: NAme of the host
    :type host_name: str
    :param name: Name of the DAG
    :type name: str
    :param assets: List of assets
    :type assets: List[Asset]
    ...
    """

    def __init__(self, host_name, name, assets: Union[List[Asset], None] = None):
        """Constructor method"""
        self._host_name = host_name
        self._name = name
        self._asset_path = AssetPath(
            platform_type=PlatformTypes.ASTRONOMER.value,
            connection_name=self._host_name,
            assets=assets,
        )  # Default value

    @staticmethod
    def create(host_name, name, assets: Union[List[Asset], None] = None):
        """Static method for obtaining AstroDag's DataSet Class
        used for getting the required infomation for Pantomath
        :param host_name: NAme of the host
        :type host_name: str
        :param name: Name of the DAG
        :type name: str
        :param assets: List of assets
        :type assets: List[Asset]
        ...
        :return: AstroDag class object
        :rtype: AstroDag
        """
        return AstroDag(host_name, name, assets)

    def get_name(self):
        """Returns the name of the object
        ...
        :return: the name of the object
        :rtype: str
        """
        return self._name

    def get_type(self):
        """Returns the type of the object
        ...
        :return: the type of the object
        :rtype: str
        """
        return JobTypes.DAG.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return util.sanitize_fully_qualified_object_name(
            self._host_name + "/" + self.get_name()
        )

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.ASTRO.value

    def get_asset_path(self) -> AssetPath:
        """Returns the asset paths of the object
        ...
        :return: the asset paths of the object
        :rtype: AssetPath
        """
        return self._asset_path
