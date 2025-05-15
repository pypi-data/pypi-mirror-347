from typing import Union, List
from pantomath_sdk.enums.platform_types import PlatformTypes
from pantomath_sdk.model.asset_path.asset_path import Asset
from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.model.asset_path import AssetPath
import pantomath_sdk.util as util


class AstroTask(Job):
    """AstroTask's Job Class used for getting the required infomation for Pantomath
    :param dag_name: Name of the dag
    :type dag_name: str
    :param host_name: Name of the host
    :type host_name: str
    :param name: Name of the task
    :type name: str
    ...
    """

    def __init__(
        self, dag_name, host_name, name, assets: Union[List[Asset], None] = None
    ):
        """Constructor method"""
        self._dag_name = dag_name
        self._host_name = host_name
        self._name = name
        self.asset_path = AssetPath(
            platform_type=PlatformTypes.ASTRONOMER.value,
            connection_name=self._host_name,
            assets=assets,
        )

    @staticmethod
    def create(dag_name, host_name, name, assets: Union[List[Asset], None] = None):
        """Static method for obtaining AstroTask's DataSet Class
        used for getting the required infomation for Pantomath
        :param dag_name: Name of the dag
        :type dag_name: str
        :param host_name: Name of the host
        :type host_name: str
        :param name: Name of the task
        :type name: str
        ...
        :return: AstroTask class object
        :rtype: AstroTask
        """
        return AstroTask(dag_name, host_name, name, assets)

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
        return JobTypes.TASK.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return util.sanitize_fully_qualified_object_name(
            self._host_name + "/" + self._dag_name + "/" + self.get_name()
        )

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.ASTRO.value

    def get_asset_path(self) -> AssetPath:
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: AssetPath
        """
        return self.asset_path
