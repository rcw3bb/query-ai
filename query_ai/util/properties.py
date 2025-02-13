import configparser
import os

class Properties:
    """
    A class to handle reading properties from a configuration file.

    Author: Ron Webb
    Since: 1.0.0
    """

    def __init__(self, filename: str):
        """
        Initializes the Properties object with the given filename.

        Parameters:
        ----------
        filename : str
            The name of the properties file.
        """
        self.filename = filename
        self.properties = None

    def __get_properties(self):
        """
        Reads the properties file and returns a ConfigParser object.

        Returns:
        -------
        configparser.ConfigParser
            The ConfigParser object containing the properties.
        """
        if not self.properties:
            try:
                config = configparser.ConfigParser()
                config.read(self.filename)
                self.properties = config
            except FileNotFoundError as e:
                print(f"Error: Properties file {self.filename} not found")

        return self.properties

    def get(self, section: str, prop: str, default_value: str):
        """
        Gets the value of a property as a string.

        Parameters:
        ----------
        section : str
            The section of the properties file.
        prop : str
            The property name.
        default_value : str
            The default value to return if the property is not found.

        Returns:
        -------
        str
            The value of the property, or the default value if the property is not found.
        """
        return self.__get_properties().get(section, prop) \
            if self.__get_properties().has_option(section, prop) else default_value

    def getint(self, section: str, prop: str, default_value: int):
        """
        Gets the value of a property as an integer.

        Parameters:
        ----------
        section : str
            The section of the properties file.
        prop : str
            The property name.
        default_value : str
            The default value to return if the property is not found.

        Returns:
        -------
        int
            The value of the property as an integer, or the default value if the property is not found.
        """
        return self.__get_properties().getint(section, prop) \
            if self.__get_properties().has_option(section, prop) else default_value