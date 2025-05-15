from typing import Union, List
from pantomath_sdk.model.asset_path.asset_path import Asset, AssetPath
from pantomath_sdk.model.job.job import Job
from pantomath_sdk.enums.job_type import JobTypes
from pantomath_sdk.enums.platform_types import PlatformTypes
import pantomath_sdk.util as util


class ADFPipeline(Job):
    """ADFPipeline's Job Class used for getting the required infomation for Pantomath
    :param pipeline_id: The Pipeline ID
    :type pipeline_id: str
    :param name: Name of the pipeline
    :type name: str
    ...
    """

    def __init__(self, pipeline_id, name, assets: Union[List[Asset], None] = None):
        """Constructor method"""
        self._pipeline_id = pipeline_id
        self._name = name
        self.asset_path = AssetPath(
            platform_type=PlatformTypes.ADF.value,
            connection_name="Azure Data Factory Connection",
            assets=assets,
        )

    @staticmethod
    def create(pipeline_id, name, assets: Union[List[Asset], None] = None):
        """Static method for obtaining ADFPipeline's DataSet Class
        used for getting the required infomation for Pantomath
        :param pipeline_id: The Pipeline ID
        :type pipeline_id: str
        :param name: Name of the pipeline
        :type name: str
        ...
        :return: ADFPipeline class object
        :rtype: ADFPipeline
        """
        return ADFPipeline(pipeline_id, name, assets)

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
        return JobTypes.ADF_PIPELINE.value

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        return util.sanitize_fully_qualified_object_name(str(self._pipeline_id).lower())

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        return PlatformTypes.ADF.value

    def get_asset_path(self):
        """Returns the asset path of the object
        ...
        :return: the asset path of the object
        :rtype: AssetPath
        """
        return self.asset_path
