from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath
from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes
from typing import Union, List


class SSISTask(Job):
    """SSISTask's Job Class used for getting the required infomation for Pantomath
    :param project_name: Name of the Project
    :type project_name: str
    :param folder_name: Name of the Folder
    :type folder_name: str
    :param parent_executable_name: Name of the Parent Executable
    :type parent_executable_name: str
    :param executable_name: Name of the Task
    :type executable_name: str
    ...
    """

    def __init__(
        self,
        project_name,
        folder_name,
        parent_executable_name,
        executable_name,
        assets: Union[List[Asset], None] = None,
    ):
        """Constructor method"""
        self._project_name = project_name
        self._folder_name = folder_name
        self._parent_executable_name = parent_executable_name
        self._executable_name = executable_name
        self._asset_path = AssetPath(
            platform_type=self.get_platform_type(),
            connection_name=project_name,
            assets=assets,
        )

    @staticmethod
    def create(
        project_name,
        folder_name,
        parent_executable_name,
        executable_name,
        assets: Union[List[Asset], None] = None,
    ):
        """Static method for obtaining SSISTask's DataSet Class
        used for getting the required infomation for Pantomath
        :param project_name: Name of the Project
        :type project_name: str
        :param folder_name: Name of the Folder
        :type folder_name: str
        :param parent_executable_name: Name of the Parent Executable
        :type parent_executable_name: str
        :param executable_name: Name of the Task
        :type executable_name: str
        ...
        :return: SSISTask class object
        :rtype: SSISTask
        """
        return SSISTask(
            project_name, folder_name, parent_executable_name, executable_name, assets
        )

    def get_name(self):
        """Returns the name of the object
        ...
        :return: the name of the object
        :rtype: str
        """
        return self._executable_name

    def get_type(self):
        """Returns the type of the object
        ...
        :return: the type of the object
        :rtype: str
        """
        return JobTypes.TASK.value

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
            + self._parent_executable_name
            + "."
            + self._executable_name
        ).lower()

    def get_project_name(self):
        """Returns the project name of the object
        ...
        :return: the project name of the object
        :rtype: str
        """
        return self._project_name

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
