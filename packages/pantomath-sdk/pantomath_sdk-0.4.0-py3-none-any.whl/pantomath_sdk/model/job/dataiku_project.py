from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath
from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes
import pantomath_sdk.util as util


class DataikuProject(Job):
    """DataikuProject's Job Class used for getting the required infomation for Pantomath
    :param _host_name: Dataiku Host
    :type _host_name: str
    :param project_label: Projects name
    :type project_label: str
    :param project_key: Project ID
    :type project_key: str
    ...
    """

    def __init__(
        self,
        host_name,
        project_label,
        project_key,
        assets: Union[List[Asset], None] = None,
    ):
        """Constructor method"""
        self._host_name = host_name
        self._project_label = project_label
        self._project_key = project_key
        self._asset_path = AssetPath(
            platform_type=PlatformTypes.DATAIKU.value,
            connection_name=host_name,
            assets=assets,
        )

    @staticmethod
    def create(
        host_name, project_label, project_key, assets: Union[List[Asset], None] = None
    ):
        """Static method for obtaining DataikuProject's DataSet Class
        used for getting the required infomation for Pantomath
        :param _host_name: Dataiku Host
        :type _host_name: str
        :param project_label: Projects name
        :type project_label: str
        :param project_key: Project ID
        :type project_key: str
        ...
        :return: DataikuProject class object
        :rtype: DataikuProject
        """
        return DataikuProject(host_name, project_label, project_key, assets)

    def get_name(self):
        """Returns the name of the object
        ...
        :return: the name of the object
        :rtype: str
        """
        return self._project_label

    def get_type(self):
        """Returns the type of the object
        ...
        :return: the type of the object
        :rtype: str
        """
        return JobTypes.PROJECT.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return util.sanitize_fully_qualified_object_name(
            util.normalize_host(
                str(str(self._host_name) + "/projects/" + str(self._project_key))
            )
        )

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.DATAIKU.value

    def get_asset_path(self) -> AssetPath:
        """Returns the Asset Path of the object
        ...
        :return: the Asset Path of the object
        :rtype: AssetPath
        """
        return self._asset_path
