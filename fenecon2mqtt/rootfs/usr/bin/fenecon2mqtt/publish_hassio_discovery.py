#!/usr/bin/python3
import json
import logging
import re

import config

# Templates for device and entity discovery
json_template_device = {
    "name": "FEMS System",
    "uniq_id": "fenecon",
    "object_id": "fenecon",
    "device_class": "enum",
    "stat_t": "",
    "val_tpl": "",
    "dev": {
        "name": "Battery Inverter",
        "sw": "",
        "mf": "Fenecon",
        "mdl": "Fenecon Home",
        "ids": ["fenecon_home"]
    }
}

json_template_entity = {
    "name": "",
    "uniq_id": "",
    "object_id": "",
    "stat_t": "",
    "unit_of_measurement": "",
    "stat_cla": "measurement",
    "dev_cla": "",
    "val_tpl": "",
    "dev": {
        "ids": ["fenecon_home"]
    }
}

# Value templates
val_tmpl_state = '''{% set mapper = {
    "0": "Ok",
    "1": "Info",
    "2": "Warning",
    "3": "Fault"} %}
{% set state = value | string %}
{{ mapper[state] if state in mapper else state }}'''

val_tmpl_gridmode = '''{% set mapper = {
    "-1": "Undefined",
    "1": "On-Grid",
    "2": "Off-Grid"} %}
{% set gridmode = value | string %}
{{ mapper[gridmode] if gridmode in mapper else gridmode }}'''

val_tmpl_charging_state = '''{% set mapper = {
      0: 'Ok',
      1: 'Info',
      2: 'Warning',
      3: 'Fault'} %}
{% set state = value | int %}
{{ mapper[state] if state in mapper.keys() else 'Unknown' }}'''

val_tmpl_change_from_grid_allowed = '''{% set mapper = {
    "0": "No",
    "1": "Yes" %}
{% set state = value | string %}
{{ mapper[state] if state in mapper else 'Unknown' }}'''

charger_state_re = re.compile(r'charger\d+/State')
evcs_charge_state_re = re.compile(r'evcs\d+/ChargeState')

def get_entity_device_class(unit):
    """
    Get the device class based on the unit of measurement.

    Args:
        unit (str): The unit of measurement.

    Returns:
        str: The device class.
    """
    logger = logging.getLogger(__name__)
    if unit == "%":
        return "battery"
    elif unit in ["W", "mW"]:
        return "power"
    elif unit in ["Wh", "mWh", "kWh"]:
        return "energy"
    elif unit in ["V", "mV"]:
        return "voltage"
    elif unit in ["A", "mA"]:
        return "current"
    elif unit == "C":
        return "temperature"
    return None


def get_entity_state_class(device_class):
    """
    Get the state class based on the device class.

    Args:
        device_class (str): The device class.

    Returns:
        str: The state class.
    """
    if device_class == "energy":
        return "total_increasing"
    elif device_class in ['battery', 'power', 'voltage', 'current', 'temperature']:
        return "measurement"
    return None


def get_entity_value_template(channel):
    """
    Get the value template for a given channel.

    Args:
        channel (str): The channel name.

    Returns:
        str: The value template.
    """
    if charger_state_re.search(channel):
        return val_tmpl_state
    elif channel == "_sum/GridMode":
        return val_tmpl_gridmode
    elif evcs_charge_state_re.search(channel):
        return val_tmpl_charging_state
    elif channel == "_meta/IsEssChargeFromGridAllowed":
        return val_tmpl_change_from_grid_allowed
    return "{{value}}"


def get_dirty_guess(attribute, guess_type):
    """
    Guess the unit or class based on the attribute name.

    Args:
        attribute (str): The attribute name.
        guess_type (str): Either 'unit' or 'class'.

    Returns:
        str: The guessed unit or class.
    """
    guesses = {
        "unit": {
            "power": "W",
            "soc": "%",
            "soh": "%",
            "capacity": "Wh",
            "energy": "Wh",
            "voltage": "dV",
            "current": "mA",
            "temperature": "°C",
        },
        "class": {
            "soc": "battery",
            "soh": "battery",
            "power": "power",
            "energy": "energy",
            "voltage": "voltage",
            "current": "current",
            "temperature": "temperature",
        },
    }

    for key, value in guesses[guess_type].items():
        if key in attribute.lower():
            return value
    return None


def get_sensor_name(channel, config):
    """
    Get the sensor name for a given channel.

    Args:
        channel (str): The channel name.
        config (module): The configuration module.

    Returns:
        str: The sensor name.
    """
    try:
        for entry in config.lang_list['fems_channels_dict']:
            if entry['channel'] == channel:
                return f"{config.hassio['sensor_name_prefix']} {entry[config.language]}"
    except KeyError:
        return None
    return None


def publish_hassio_discovery(mqtt, fenecon_config, version):
    """
    Publish Home Assistant discovery messages for Fenecon sensors.

    Args:
        mqtt (MqttClient): The MQTT client instance.
        fenecon_config (dict): The Fenecon configuration.
        version (str): The Fenecon version.
    """
    logger = logging.getLogger(__name__)
    logger.info('Start publishing Home Assistant discovery messages.')

    for channel_config in config.fems_channels:
        hassio_uid = f"{config.hassio['sensor_uid_prefix']}{channel_config['channel']}".replace("/", "-").lower()
        try:
            # Handle special case for "_sum/State"
            if channel_config['channel'] == "_sum/State":
                json_template_device['dev']['sw'] = version
                json_template_device['stat_t'] = f"{config.hassio['mqtt_broker_hassio_queue']}/{hassio_uid}"
                json_template_device['val_tpl'] = channel_config.get('value_template', val_tmpl_state)
                mqtt.publish(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}/config", json.dumps(json_template_device), qos=0, retain=True)
                continue

            # Prepare entity discovery message
            json_template_entity['uniq_id'] = hassio_uid
            json_template_entity['object_id'] = f"battery_inverter_{config.hassio['sensor_name_prefix']}_{channel_config['channel']}"
            json_template_entity['name'] = channel_config.get('name') or get_sensor_name(channel_config['channel'], config) or f"{config.hassio['sensor_name_prefix']} {channel_config['channel']}"
            json_template_entity['unit_of_measurement'] = channel_config.get('device_unit') or get_dirty_guess(channel_config['channel'], 'unit')
            json_template_entity['dev_cla'] = channel_config.get('device_class') or get_dirty_guess(channel_config['channel'], 'class')
            json_template_entity['stat_cla'] = channel_config.get('state_class') or get_entity_state_class(json_template_entity['dev_cla'])
            json_template_entity['val_tpl'] = channel_config.get('value_template') or get_entity_value_template(channel_config['channel'])
            json_template_entity['stat_t'] = f"{config.hassio['mqtt_broker_hassio_queue']}/{hassio_uid}"

            # Publish discovery message
            mqtt.publish(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}/{hassio_uid}/config", json.dumps(json_template_entity), qos=0, retain=True)

        except Exception as e:
            logger.warning(f"Error processing channel '{channel_config['channel']}': {e}")

    logger.info('Finished publishing Home Assistant discovery messages.')