import os

from query_ai.util.properties import Properties

class DBConfig:
    """
    Configuration class for database settings.

    Author: Ron Webb
    Since: 1.0.0
    """

    def __init__(self, properties_file: str):
        """
        Initialize the DBConfig object by loading properties from the properties file
        and environment variables.
        """

        properties = Properties(properties_file)
        self.__database = properties.get("DATABASE", "DATABASE_NAME", "query-ai")
        self.__host = properties.get("DATABASE", "HOST", "localhost")
        self.__port = properties.getint("DATABASE", "PORT", 5432)
        self.__user = os.getenv("DB_USERNAME", "postgres")
        self.__password = os.getenv("DB_PASSWORD", "mypassword")

    def get_database(self):
        """
        Get the database name.

        :return: The name of the database.
        """
        return self.__database

    def get_host(self):
        """
        Get the database host.

        :return: The host of the database.
        """
        return self.__host

    def get_port(self):
        """
        Get the database port.

        :return: The port of the database.
        """
        return self.__port

    def get_user(self):
        """
        Get the database user.

        :return: The user of the database.
        """
        return self.__user

    def get_password(self):
        """
        Get the database password.

        :return: The password of the database.
        """
        return self.__password