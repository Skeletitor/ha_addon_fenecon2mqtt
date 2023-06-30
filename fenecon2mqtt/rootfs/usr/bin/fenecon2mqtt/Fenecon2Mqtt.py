#!/usr/bin/python3
import logging
import os
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

import config
from FeneconClient import FeneconClient
from MqttClient import MqttClient


def setup_root_logger():
    # Create the Logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ENV_IS_DOCKER = is_docker()
    logger.info(f"Runs in Docker {ENV_IS_DOCKER }")
    # Create a Formatter for formatting the log messages
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
    logger_level = logging.getLevelName(str(config.log_level).upper())
    if ENV_IS_DOCKER:
        # Create the Handler for logging data to a file
        # ensure logfile location exists
        if not os.path.exists('/share/fenecon'):
            os.makedirs('/share/fenecon')
        logger_handler = RotatingFileHandler('/share/fenecon/daemon.log', maxBytes=1024*1024, backupCount=2)
        logger_handler.setLevel(logger_level)
        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)
    #Create the Handler for logging data to console.
    console_handler = StreamHandler()
    console_handler.setLevel(logger_level)
    # Add the Formatter to the Handler
    console_handler.setFormatter(logger_formatter)
    # Add the Handler to the Logger
    if ENV_IS_DOCKER:
        logger.addHandler(logger_handler)
    logger.addHandler(console_handler)
    return logger

def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )

def main():
    logger = setup_root_logger()

    # Connect to Hassio integrated MQTT
    mqtt = MqttClient()

    # start connect to Fenecon websocket
    s = FeneconClient(mqtt)

if __name__ == "__main__":
    main()