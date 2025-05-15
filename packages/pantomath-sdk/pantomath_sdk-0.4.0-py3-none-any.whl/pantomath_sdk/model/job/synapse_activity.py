from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes
from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath


class SynapseActivity(Job):
    """SynapseActivity's Job Class used for getting the required infomation for Pantomath
    :param pipeline_id: The Pipeline ID
    :type pipeline_id: str
    :param name: Name of the activity
    :type name: str
    ...
    """

    def __init__(self, pipeline_id, name, assets: Union[List[Asset], None] = None):
        """Constructor method"""
        self._pipeline_id = pipeline_id
        self._name = name
        self._asset_path = AssetPath(
            platform_type=PlatformTypes.SYNAPSE.value,
            connection_name="Synapse Connection",
            assets=assets,
        )

    @staticmethod
    def create(pipeline_id, name, assets: Union[List[Asset], None] = None):
        """Static method for obtaining SynapseActivity's DataSet Class
        used for getting the required infomation for Pantomath
        :param pipeline_id: The Pipeline ID
        :type pipeline_id: str
        :param name: Name of the activity
        :type name: str
        ...
        :return: SynapseActivity class object
        :rtype: SynapseActivity
        """
        return SynapseActivity(pipeline_id, name, assets)

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
        return JobTypes.ACTIVITY.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return str(self._pipeline_id + "/activities/" + self._name).lower()

    def get_pipeline_id(self):
        """Returns the pipeline ID of the object
        ...
        :return: the pipeline ID of the object
        :rtype: str
        """
        return self._pipeline_id

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.SYNAPSE.value

    def get_asset_path(self):
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: AssetPath
        """
        return self._asset_path
