import os
import logging
import logging.config

LOG_DIR="./log"
LOG_FILE="running.log"
LOG_PATH=os.path.join(LOG_DIR, LOG_FILE)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


config = {
    "version": 1,
    "formatters": {
        "simple": {"format": "[%(name)s] %(message)s"},
        "complex": {
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": f"{LOG_PATH}",
            "formatter": "complex",
            "level": "ERROR",
        },
    },
    "root": {"handlers": ["console", "file"], "level": "WARNING"},
    "loggers": {"parent": {"level": "INFO"}, "parent.child": {"level": "DEBUG"},},
}

config_new = {
    "version": 1,
    "formatters": {
        "simple": {"format": "[%(name)s] %(message)s"},
        "complex": {
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": f"{LOG_PATH}",
            "formatter": "complex",
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console", "file"], 
        "level": "DEBUG"
    },
    "loggers": {
        "parent": {"level": "INFO"}, 
        "parent.child": {"level": "DEBUG"},
    },
}

logging.config.dictConfig(config_new)

def debug(log_str: str):
    logging.debug(log_str)

def info(log_str: str):
    logging.info(log_str)

def error(log_str: str):
    logging.error(log_str)
