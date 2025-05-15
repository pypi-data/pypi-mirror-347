from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath
from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes


class FivetranConnectorConstructor(Job):
    """FivetranConnectorConstructor's Job Class
    used for getting the required infomation for Pantomath
    :param name: Name of the Constructor
    :type name: str
    ...
    """

    def __init__(self, name, assets: Union[List[Asset], None] = None):
        """Constructor method"""
        self._name = name
        self._asset_path = AssetPath(
            platform_type=self.get_platform_type(),
            connection_name="Fivetran Connection",
            assets=assets,
        )

    @staticmethod
    def create(name, assets: Union[List[Asset], None] = None):
        """Static method for obtaining FivetranConnectorConstructor's DataSet Class
        used for getting the required infomation for Pantomath
        :param name: Name of the Constructor
        :type name: str
        ...
        :return: FivetranConnectorConstructor class object
        :rtype: FivetranConnectorConstructor
        """
        return FivetranConnectorConstructor(name, assets)

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
        return JobTypes.FIVETRAN_CONNECTOR.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return str(self._name)

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.FIVETRAN.value

    def get_asset_path(self):
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: list
        """
        return self._asset_path
