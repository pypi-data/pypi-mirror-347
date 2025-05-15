from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath
from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes


class DBTJobConstructor(Job):
    """DBTJobConstructor's Job Class used for getting the required information for Pantomath
    :param name: Name of the Job
    :type name: str
    :param host: Host for the account, e.g. cloud.getdbt.com or ACCOUNT_PREFIX.us2.dbt.com
    :type host: str
    :param account_id: ID of the Account
    :type account_id: str
    :param job_id: ID of the Project
    :type job_id: str
    :param project_name: Name of the Project
    :type project_name: str
    ...
    """

    def __init__(
        self,
        name,
        host,
        account_id,
        job_id,
        project_name,
        assets: Union[List[Asset], None] = None,
    ):
        """Constructor method"""
        self._name = name
        self._host = host
        self._account_id = account_id
        self._job_id = job_id
        self._project_name = project_name
        self._asset_path = AssetPath(
            platform_type=self.get_platform_type(),
            connection_name=self._project_name,
            assets=assets,
        )

    @staticmethod
    def create(
        name,
        host,
        account_id,
        job_id,
        project_name,
        assets: Union[List[Asset], None] = None,
    ):
        """Static method for obtaining DBTJobConstructor's DataSet Class
        used for getting the required information for Pantomath
        :param name: Name of the Job
        :type name: str
        :param host: Host for the account, e.g. cloud.getdbt.com or ACCOUNT_PREFIX.us2.dbt.com
        :type host: str
        :param account_id: ID of the Account
        :type account_id: str
        :param job_id: ID of the Project
        :type job_id: str
        :param project_name: Name of the Project
        :type project_name: str
        """
        return DBTJobConstructor(name, host, account_id, job_id, project_name, assets)

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
        return JobTypes.JOB.value

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.DBT.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return str(
            str(self._host)
            + "/#/accounts/"
            + str(self._account_id)
            + "."
            + str(self._project_name)
            + "."
            + str(self._name)
            + "."
            + str(self._job_id)
        ).lower()

    def get_asset_path(self) -> AssetPath:
        """Returns the Asset Path of the object
        ...
        :return: the Asset Path of the object
        :rtype: AssetPath
        """
        return self._asset_path
