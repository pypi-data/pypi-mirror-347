from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath
from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes


class DBTModelConstructor(Job):
    """DBTModelConstructor's Job Class used for getting the required information for Pantomath
    :param host: Host for the account, e.g. cloud.getdbt.com or ACCOUNT_PREFIX.us2.dbt.com
    :type host: str
    :param account_id: ID of the Account
    :type account_id: str
    :param project_name: Name of the Project
    :type project_name: str
    :param model_name: Name of the Model
    :type model_name: str
    ...
    """

    def __init__(
        self,
        host,
        account_id,
        project_name,
        model_name,
        assets: Union[List[Asset], None] = None,
    ):
        """Constructor method"""
        self._host = host
        self._account_id = account_id
        self._project_name = project_name
        self._model_name = model_name
        self._asset_path = AssetPath(
            platform_type=self.get_platform_type(),
            connection_name=f"Account Id - {self._account_id}",
            assets=assets,
        )

    @staticmethod
    def create(
        host,
        account_id,
        project_name,
        model_name,
        assets: Union[List[Asset], None] = None,
    ):
        """Static method for obtaining DBTModelConstructor's DataSet Class
        used for getting the required information for Pantomath
        :param host: Host for the account, e.g. cloud.getdbt.com or ACCOUNT_PREFIX.us2.dbt.com
        :type host: str
        :param account_id: ID of the Account
        :type account_id: str
        :param project_name: Name of the Project
        :type project_name: str
        :param model_name: Name of the Model
        :type model_name: str
        ...
        :return: DBTModelConstructor class object
        :rtype: DBTModelConstructor
        """
        return DBTModelConstructor(
            host, account_id, project_name, model_name, assets=assets
        )

    def get_name(self):
        """Returns the name of the object
        ...
        :return: the name of the object
        :rtype: str
        """
        return self._model_name

    def get_type(self):
        """Returns the type of the object
        ...
        :return: the type of the object
        :rtype: str
        """
        return JobTypes.DBT_MODEL.value

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
            + "/project/"
            + str(self._project_name)
            + "/model/"
            + str(self._model_name)
        ).lower()

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.DBT.value

    def get_asset_path(self) -> AssetPath:
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: AssetPath
        """
        return self._asset_path
