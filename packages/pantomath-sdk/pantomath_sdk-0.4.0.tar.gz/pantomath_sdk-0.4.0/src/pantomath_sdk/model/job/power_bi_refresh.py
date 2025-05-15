from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes
from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath


class PowerBIRefresh(Job):
    """PowerBIRefresh's Job Class used for getting the required infomation for Pantomath
    :param dataset_id: The dataset ID
    :type dataset_id: str
    :param refresh_schedule_context: Name of the refresh_schedule_context
    :type refresh_schedule_context: str
    :param name: Name of the activity
    :type name: str
    ...
    """

    def __init__(
        self,
        dataset_id,
        refresh_schedule_context,
        name,
        assets: Union[List[Asset], None] = None,
    ):
        """Constructor method"""
        self._name = name
        self._refresh_schedule_context = refresh_schedule_context
        self._dataset_id = dataset_id
        self._asset_path = AssetPath(
            platform_type=PlatformTypes.POWERBI.value,
            connection_name="PowerBI Connection",
            assets=assets,
        )

    @staticmethod
    def create(
        dataset_id,
        refresh_schedule_context,
        name,
        assets: Union[List[Asset], None] = None,
    ):
        """Static method for obtaining PowerBIRefresh's DataSet Class
        used for getting the required infomation for Pantomath
        :param dataset_id: The dataset ID
        :type dataset_id: str
        :param refresh_schedule_context: Name of the refresh_schedule_context
        :type refresh_schedule_context: str
        :param name: Name of the activity
        :type name: str
        ...
        :return: PowerBIRefresh class object
        :rtype: PowerBIRefresh
        """
        return PowerBIRefresh(dataset_id, refresh_schedule_context, name, assets)

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
        return JobTypes.POWER_BI_REFRESH.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return (
            str(
                self._refresh_schedule_context
                + "/"
                + self._dataset_id
                + "/"
                + self._name
            ).replace(" ", "_")
        ).lower()

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.POWERBI.value

    def get_asset_path(self):
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: AssetPath
        """
        return self._asset_path
