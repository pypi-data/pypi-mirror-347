from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes
from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath


class PowerBiDataFlow(Job):
    """PowerBiDataFlow's Job Class used for getting the required infomation for Pantomath
    :param group_id: The Group ID
    :type group_id: str
    :param object_id: The Object ID
    :type object_id: str
    :param name: Name of the Data  Flow
    :type name: str
    ...
    """

    def __init__(
        self, group_id, object_id, name, assets: Union[List[Asset], None] = None
    ):
        """Constructor method"""
        self._name = name
        self._object_id = object_id
        self._groupId = group_id
        self._asset_path = AssetPath(
            platform_type=PlatformTypes.POWERBI.value,
            connection_name="PowerBI Connection",
            assets=assets,
        )

    @staticmethod
    def create(group_id, object_id, name, assets: Union[List[Asset], None] = None):
        """Static method for obtaining PowerBiDataFlow's DataSet Class
        used for getting the required infomation for Pantomath
        :param group_id: The Group ID
        :type group_id: str
        :param object_id: The Object ID
        :type object_id: str
        :param name: Name of the Data  Flow
        :type name: str
        ...
        :return: PowerBiDataFlow class object
        :rtype: PowerBiDataFlow
        """
        return PowerBiDataFlow(group_id, object_id, name, assets)

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
        return JobTypes.POWER_BI_DATAFLOW.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return str(
            "app.powerbi.com/groups/" + self._groupId + "/dataflows/" + self._object_id
        ).lower()

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.POWERBI.value

    def get_asset_path(self) -> AssetPath:
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: AssetPath
        """
        return self._asset_path
