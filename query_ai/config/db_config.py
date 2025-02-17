import os

class DBConfig:
    """
    Configuration class for database settings.

    Author: Ron Webb
    Since: 1.0.0
    """

    def __init__(self):
        """
        Initialize the DBConfig object by loading properties from the properties file
        and environment variables.
        """

        self.__database = os.getenv("QA_DB_NAME", "query-ai")
        self.__host = os.getenv("QA_DB_HOST", "localhost")
        self.__port = os.getenv("QA_DB_PORT", 5432)
        self.__user = os.getenv("QA_DB_USERNAME", "postgres")
        self.__password = os.getenv("QA_DB_PASSWORD", "mypassword")

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