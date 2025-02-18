import os
import logging
from logging.handlers import RotatingFileHandler

__logs_directory = "../logs"  # Or whatever you want to call it
if not os.path.exists(__logs_directory):
    os.makedirs(__logs_directory)

__log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

__rotating_handler = RotatingFileHandler(os.path.join(__logs_directory, 'query-ai.log'),
                                         maxBytes=1024*1024*10, # 10MB max size
                                         backupCount=50)
__rotating_handler.setFormatter(__log_formatter)

__console_handler = logging.StreamHandler()  # Defaults to sys.stdout
__console_handler.setFormatter(__log_formatter)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(__rotating_handler)
    logger.addHandler(__console_handler)
    return logger

__all__ = ['get_logger']
