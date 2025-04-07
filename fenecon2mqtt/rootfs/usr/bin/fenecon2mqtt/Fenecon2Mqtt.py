#!/usr/bin/python3
import logging
import os
import signal
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

import config
from FeneconClient import FeneconClient
from MqttClient import MqttClient


def setup_root_logger():
    """
    Set up the root logger with console and file handlers.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Detect if running in Docker
    ENV_IS_DOCKER = is_docker()
    logger.info(f"Running in Docker: {ENV_IS_DOCKER}")

    # Create a formatter for log messages
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
    logger_level = logging.getLevelName(str(config.log_level).upper())

    # File logging for Docker environment
    if ENV_IS_DOCKER:
        log_dir = '/share/fenecon'
        log_file = os.path.join(log_dir, 'daemon.log')

        # Ensure the log directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Create a rotating file handler
        logger_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=2)
        logger_handler.setLevel(logger_level)
        logger_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_handler)

    # Console logging
    console_handler = StreamHandler()
    console_handler.setLevel(logger_level)
    console_handler.setFormatter(logger_formatter)
    logger.addHandler(console_handler)

    return logger


def is_docker():
    """
    Check if the application is running inside a Docker container.

    Returns:
        bool: True if running in Docker, False otherwise.
    """
    try:
        return os.path.exists('/.dockerenv') or any('docker' in line for line in open('/proc/self/cgroup', 'r'))
    except Exception:
        return False


def handle_shutdown(signal_number, frame):
    """
    Handle termination signals for graceful shutdown.

    Args:
        signal_number (int): The signal number.
        frame (FrameType): The current stack frame.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Received termination signal ({signal_number}). Shutting down...")
    sys.exit(0)


def main():
    """
    Main entry point for the Fenecon2Mqtt application.
    """
    logger = setup_root_logger()
    logger.info("Starting Fenecon2Mqtt...")

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        # Connect to Hassio integrated MQTT
        mqtt = MqttClient()

        # Start connection to Fenecon WebSocket
        fenecon_client = FeneconClient(mqtt)

        # Keep the main thread alive
        signal.pause()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        logger.info("Fenecon2Mqtt is shutting down.")


if __name__ == "__main__":
    main()