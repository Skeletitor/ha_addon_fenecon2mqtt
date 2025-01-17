#!/usr/bin/python3
import json
import os
import logging
import yaml

logger = logging.getLogger(__name__)
data = None

try:
    with open('/data/options.json') as file:
        data = json.load(file)
except Exception:
    script_dir = os.path.dirname(__file__)
    rel_path = "./config.json"
    with open(os.path.join(script_dir, rel_path)) as file:
        data = json.load(file)

fenecon = data['fenecon']
hassio = data['hassio']
log_level = data['log_level']
language = data['sensor_language']
channels2subscribe = []
fems_channels = []

# prepare for channel subscription
try:
    fems_channels = data['fems_channels']
    channels2subscribe.extend(c['channel'] for c in fems_channels)
except Exception:
    logger.warning("Deprecated add-on config found. Migrate from 'fems_request_channels' to 'fems_channels'. ")
    channels2subscribe = fenecon['fems_request_channels']

# languages for default sensors
lang_list = []
try:
    script_dir = os.path.dirname(__file__)
    rel_path = "./language.yaml"
    with open(os.path.join(script_dir, rel_path)) as file2:
        lang_list = yaml.safe_load(file2)
except Exception:
    lang_list = []

# add defaults:
hassio['mqtt_broker_keepalive'] = 60
hassio['mqtt_broker_hassio_discovery_queue'] = "homeassistant/sensor/fenecon"
hassio['mqtt_broker_hassio_queue'] = "fenecon"
hassio['sensor_uid_prefix'] = "fems-"
