from aenum import Enum


class AssetPathTypes(Enum):
    """This class is an enum of all the AssetPathTypes supported by the Pantomath Python SDK."""

    ACCOUNT = "ACCOUNT"
    AGENT = "AGENT"
    APP = "APP"
    APP_HOST = "APP_HOST"
    BUCKET = "BUCKET"
    CATALOG = "CATALOG"
    CHANNEL = "CHANNEL"
    CONNECTION = "CONNECTION"
    CONNECTOR = "CONNECTOR"
    CONTAINER = "CONTAINER"
    COUNTER = "COUNTER"
    CUBE = "CUBE"
    DAG = "DAG"
    DASHBOARD = "DASHBOARD"
    DATABASE = "DATABASE"
    DATAFLOW = "DATAFLOW"
    DATASET = "DATASET"
    DATASOURCE = "DATASOURCE"
    DEPLOYMENT = "DEPLOYMENT"
    DIMENSION = "DIMENSION"
    ENVIRONMENT = "ENVIRONMENT"
    FACTORY = "FACTORY"
    FLOW = "FLOW"
    FOLDER = "FOLDER"
    FUNCTION = "FUNCTION"
    GROUP = "GROUP"
    HOST = "HOST"
    HUB = "HUB"
    JOB = "JOB"
    MEASURE = "MEASURE"
    MEASURE_GROUP = "MEASURE_GROUP"
    MODEL = "MODEL"
    OBJECT = "OBJECT"
    ORGANIZATION = "ORGANIZATION"
    PACKAGE = "PACKAGE"
    PARTITION = "PARTITION"
    PERSPECTIVE = "PERSPECTIVE"
    PIPELINE = "PIPELINE"
    PLAN = "PLAN"
    PLATFORM = "PLATFORM"
    PROJECT = "PROJECT"
    RECIPE = "RECIPE"
    REFRESH = "REFRESH"
    REGION = "REGION"
    REPORT = "REPORT"
    RESOURCE_GROUP = "RESOURCE_GROUP"
    ROUTINE = "ROUTINE"
    SCENARIO = "SCENARIO"
    SCHEDULE = "SCHEDULE"
    SCHEDULER = "SCHEDULER"
    SCHEMA = "SCHEMA"
    SERVER = "SERVER"
    SITE = "SITE"
    STAGE = "STAGE"
    STORAGE_ACCOUNT = "STORAGE_ACCOUNT"
    SUBSCRIPTION = "SUBSCRIPTION"
    TABLE = "TABLE"
    TASK = "TASK"
    TENANT = "TENANT"
    URI = "URI"
    WORKFLOW = "WORKFLOW"
    WORKSPACE = "WORKSPACE"
    ZONE = "ZONE"

    @staticmethod
    def get_asset_path_types():
        """Get a list of all the enum values
        ...
        :return: list of all the enum values
        :rtype: list of strings
        """
        return dir(AssetPathTypes)[: len(AssetPathTypes)]

    @staticmethod
    def is_object_type(input):
        """Validates if the unput is part of the enum
        :param input: string to check if part of enum
        :type input: str
        ...
        :return: True if in enum else False
        :rtype: Boolean
        """
        return input in AssetPathTypes.get_asset_path_types()
