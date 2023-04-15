#!/usr/bin/python3
import os
import sys
import config
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from FeneconClientSocket import FeneconClientSocket
from HassioMqttClient import HassioMqttClient

def setup_root_logger():
    # Create the Logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ENV_IS_DOCKER = is_docker()
    logger.info(f"Runs in Docker {ENV_IS_DOCKER }")
    # Create a Formatter for formatting the log messages
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
    if ENV_IS_DOCKER:
        # Create the Handler for logging data to a file
        # ensure logfile location exists
        if not os.path.exists('/share/fenecon'):
            os.makedirs('/share/fenecon')
        logger_handler = RotatingFileHandler('/share/fenecon/daemon.log', maxBytes=1024, backupCount=2)
        logger_handler.setLevel(logging.INFO)
        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)
    #Create the Handler for logging data to console.
    console_handler = StreamHandler()
    console_handler.setLevel(logging.INFO)
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
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warn message')
    # logger.error('error message')
    # logger.critical('critical message')

    # Connect to Hassio integrated MQTT
    mqtt = HassioMqttClient()

    # start connect to Fenecon websocket
    s = FeneconClientSocket(mqtt)

if __name__ == "__main__":
    main()