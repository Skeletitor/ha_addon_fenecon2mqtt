#!/usr/bin/python3
import json
import os
import logging
import yaml

logger = logging.getLogger(__name__)

def load_json_config(file_path, fallback_path=None):
    """
    Load a JSON configuration file. If the file is not found or invalid, fallback to another path.

    Args:
        file_path (str): The primary path to the JSON file.
        fallback_path (str): The fallback path to the JSON file.

    Returns:
        dict: The loaded JSON configuration.
    """
    try:
        with open(file_path) as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning(f"Configuration file not found: {file_path}")
        if fallback_path:
            logger.info(f"Attempting to load fallback configuration: {fallback_path}")
            return load_json_config(fallback_path)
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in {file_path}: {e}")
        raise

def load_yaml_config(file_path):
    """
    Load a YAML configuration file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The loaded YAML configuration.
    """
    try:
        with open(file_path) as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.warning(f"YAML configuration file not found: {file_path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML format in {file_path}: {e}")
        return {}

# Load the main configuration
script_dir = os.path.dirname(__file__)
data = load_json_config('/data/options.json', fallback_path=os.path.join(script_dir, './config.json'))

# Extract configuration sections
fenecon = data.get('fenecon', {})
hassio = data.get('hassio', {})
log_level = data.get('log_level', 'INFO').upper()
language = data.get('sensor_language', 'en')
channels2subscribe = []
fems_channels = []

# Prepare for channel subscription
try:
    fems_channels = data.get('fems_channels', [])
    channels2subscribe.extend(c['channel'] for c in fems_channels)
except KeyError:
    logger.warning("Deprecated add-on config found. Migrate from 'fems_request_channels' to 'fems_channels'.")
    channels2subscribe = fenecon.get('fems_request_channels', [])

# Load language configuration
lang_list = load_yaml_config(os.path.join(script_dir, './language.yaml'))

# Add default values for Hassio configuration
hassio.setdefault('mqtt_broker_keepalive', 60)
hassio.setdefault('mqtt_broker_hassio_discovery_queue', "homeassistant/sensor/fenecon")
hassio.setdefault('mqtt_broker_hassio_queue', "fenecon")
hassio.setdefault('sensor_uid_prefix', "fems-")

# Validate required fields
required_fields = ['mqtt_broker_host', 'mqtt_broker_port', 'mqtt_broker_user', 'mqtt_broker_passwd']
missing_fields = [field for field in required_fields if field not in hassio]
if missing_fields:
    logger.error(f"Missing required Hassio configuration fields: {', '.join(missing_fields)}")
    raise ValueError(f"Missing required Hassio configuration fields: {', '.join(missing_fields)}")

logger.info("Configuration loaded successfully.")
