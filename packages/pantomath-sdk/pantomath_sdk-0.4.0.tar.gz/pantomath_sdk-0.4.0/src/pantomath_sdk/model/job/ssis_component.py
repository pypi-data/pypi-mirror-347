from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes
from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath


class SSISComponent(Job):
    """SSISComponent's Job Class used for getting the required infomation for Pantomath
    :param project_name: Name of the project
    :type project_name: str
    :param execution_path: Path of Execution
    :type execution_path: str
    :param folder_name: Name of the folder
    :type folder_name: str
    :param name: Name of the component
    :type name: str
    ...
    """

    def __init__(
        self,
        project_name,
        execution_path,
        folder_name,
        name,
        assets: Union[List[Asset], None] = None,
    ):
        """Constructor method"""
        self._name = name
        self._folder_name = folder_name
        self._execution_path = execution_path
        self._project_name = project_name
        self._asset_path = AssetPath(
            platform_type=PlatformTypes.SSIS.value,
            connection_name=project_name,
            assets=assets,
        )

    @staticmethod
    def create(
        project_name,
        execution_path,
        folder_name,
        name,
        assets: Union[List[Asset], None] = None,
    ):
        """Static method for obtaining SSISComponent's DataSet Class
        used for getting the required infomation for Pantomath
        :param project_name: Name of the project
        :type project_name: str
        :param execution_path: Path of Execution
        :type execution_path: str
        :param folder_name: Name of the folder
        :type folder_name: str
        :param name: Name of the component
        :type name: str
        ...
        :return: SSISComponent class object
        :rtype: SSISComponent
        """
        return SSISComponent(project_name, execution_path, folder_name, name, assets)

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
        return JobTypes.COMPONENT.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return str(
            self._folder_name
            + "."
            + self._project_name
            + "."
            + self._execution_path
            + "."
            + self._name
        ).lower()

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.SSIS.value

    def get_asset_path(self):
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: AssetPath
        """
        return self._asset_path
