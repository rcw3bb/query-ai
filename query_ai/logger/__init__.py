import os
import logging
import logging.config

__logs_directory = "../logs"
__conf_directory = "../conf"

if not os.path.exists(__logs_directory):
    os.makedirs(__logs_directory)

__logger_ini_file = os.path.join(__conf_directory, 'logging.ini')

if os.path.exists(__logger_ini_file):
    logging.config.fileConfig(__logger_ini_file)
else:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('query_ai')
    logger.warning("Config file not found, using basic config.")

def get_logger(name):
    logger = logging.getLogger(name)
    return logger

__all__ = ['get_logger']
