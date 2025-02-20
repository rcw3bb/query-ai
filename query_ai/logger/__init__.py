import os
import logging
import logging.config

script_dir = os.path.dirname(os.path.abspath(__file__))

__conf_directory = f"{script_dir}/../../conf"

if not os.path.exists(__conf_directory):
    raise Exception("Config directory not found.")

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
