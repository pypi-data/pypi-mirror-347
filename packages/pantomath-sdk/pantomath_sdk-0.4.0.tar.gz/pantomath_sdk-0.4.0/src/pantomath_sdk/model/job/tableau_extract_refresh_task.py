from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
import pantomath_sdk.util as util
from pantomath_sdk.enums.platform_types import PlatformTypes
from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath


class TableauExtractRefreshTask(Job):
    """TableauExtractRefreshTask's Job Class used for getting the required infomation for Pantomath
    :param host: Host URL
    :type host: str
    :param site_id: ID of the site
    :type site_id: str
    :param refresh_id: The Refresh ID
    :type refresh_id: str
    :param name: Name of the Refresh
    :type name: str
    :param assets: List of assets
    :type assets: List[Asset], optional
    ...
    """

    def __init__(
        self, host, site_id, refresh_id, name, assets: Union[List[Asset], None] = None
    ):
        """Constructor method"""
        self._name = name
        self._host = host
        self._site_id = site_id
        self._refresh_id = refresh_id
        self._asset_path = AssetPath(
            platform_type=PlatformTypes.TABLEAU.value,
            connection_name="Tableau Connection",
            assets=assets,
        )

    @staticmethod
    def create(
        host, site_id, refresh_id, name, assets: Union[List[Asset], None] = None
    ):
        """Static method for obtaining TableauExtractRefreshTask's DataSet Class
        used for getting the required infomation for Pantomath
        :param host: Host URL
        :type host: str
        :param site_id: ID of the site
        :type site_id: str
        :param refresh_id: The Refresh ID
        :type refresh_id: str
        :param name: Name of the Refresh
        :type name: str
        :param assets: List of assets
        :type assets: List[Asset], optional
        ...
        :return: TableauExtractRefreshTask class object
        :rtype: TableauExtractRefreshTask
        """
        return TableauExtractRefreshTask(host, site_id, refresh_id, name, assets)

    def get_name(self):
        """Returns the name of the object
        ...
        :return: the name of the object
        :rtype: str
        """
        return util.sanitize_tableau_string(self._name)

    def get_type(self):
        """Returns the type of the object
        ...
        :return: the type of the object
        :rtype: str
        """
        return JobTypes.TABLEAU_EXTRACT_REFRESH_TASK.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return str(
            util.normalize_host(self._host)
            + "/site/"
            + self._site_id
            + "/task/"
            + self._refresh_id
        ).lower()

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: PlatformTypes
        """
        return PlatformTypes.TABLEAU.value

    def get_asset_path(self):
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: AssetPath
        """
        return self._asset_path
