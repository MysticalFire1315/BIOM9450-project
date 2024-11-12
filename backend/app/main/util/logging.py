import logging.config

def setup_logging(env: str):
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "logs/app.log",
                "maxBytes": 1000000,
                "backupCount": 5,
            },
            "db_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "logs/db.log",
                "maxBytes": 1000000,
                "backupCount": 5,
            },
            "error_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "logs/errors.log",
                "maxBytes": 1000000,
                "backupCount": 5,
            },
            "requests_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "logs/requests.log",
                "maxBytes": 1000000,
                "backupCount": 5,
            },
        },
        "loggers": {
            "psycopg2": {
                "level": "INFO",
                "handlers": ["db_handler"],
                "propagate": False,
            },
            "errors": {
                "level": "DEBUG" if env == "dev" else "WARNING",
                "handlers": ["console", "error_handler"],
                "propagate": False,
            },
            "requests": {
                "level": "INFO",
                "handlers": ["requests_handler"],
                "propagate": False,
            },
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console"],
        },
    }

    logging.config.dictConfig(logging_config)
