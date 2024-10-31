import logging

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def file_handler(filename: str, level: int) -> logging.FileHandler:
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    formatter = logging.Formatter(LOGGING_FORMAT)
    handler.setFormatter(formatter)
    return handler

def setup_logging():
    # 1. Setup Root Logger
    root_logger = logging.getLogger(__name__)  # Gets the root logger
    root_logger.setLevel(logging.INFO)  # Set the level of the root logger
    root_logger.addHandler(file_handler('log/app.log', logging.INFO))

    # 2. Setup Submodule Logger
    submodule_logger = logging.getLogger('psycopg2')  # Gets or creates the submodule logger
    submodule_logger.setLevel(logging.DEBUG)  # Submodule logger level
    submodule_logger.addHandler(file_handler('log/db.log', logging.INFO))
