class Job(object):
    def get_name(self):
        """Returns the name of the object
        ...
        :return: the name of the object
        :rtype: str
        """
        raise NotImplementedError()

    def get_type(self):
        """Returns the type of the object
        ...
        :return: the type of the object
        :rtype: str
        """
        raise NotImplementedError()

    def get_fully_qualified_object_name(self):
        """Returns the Fully Qualified Name of the object
        ...
        :return: the Fully Qualified Name of the object
        :rtype: str
        """
        raise NotImplementedError()

    def get_platform_type(self):
        """Returns the platform type of the object
        ...
        :return: the platform type of the object
        :rtype: str
        """
        raise NotImplementedError()

    def asset_paths(self):
        """Returns the asset paths of the object
        ...
        :return: the asset paths of the object
        :rtype: AssetPath
        """
        raise NotImplementedError()
