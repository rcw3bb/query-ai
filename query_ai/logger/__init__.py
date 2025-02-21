"""
This module is used to configure the logger for the application.

Author: Ron Webb
Since: 1.0.0
"""

import os
import logging
import logging.config

script_dir = os.path.dirname(os.path.abspath(__file__))

__CONF_DIR = f"{script_dir}/../../conf"

if not os.path.exists(__CONF_DIR):
    raise FileNotFoundError("Config directory not found.")

__logger_ini_file = os.path.join(__CONF_DIR, 'logging.ini')

if os.path.exists(__logger_ini_file):
    logging.config.fileConfig(__logger_ini_file)
else:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('query_ai')
    logger.warning("Config file not found, using basic config.")

def get_logger(name):
    """
    This function returns a logger object.
    :param name: The name of the logger.
    :return: The logger object.
    """

    new_logger = logging.getLogger(name)
    return new_logger

__all__ = ['get_logger']
