#!/usr/bin/python3
import json
import logging
import re

import config

json_template_device = {
        "name": "FEMS System",
        "uniq_id": "fenecon",
        "object_id": "fenecon",
        "device_class": "enum",
        "stat_t": "",
        "val_tpl": "",
        "dev": {
            "name":"Battery Inverter",
            "sw":"",
            "mf":"Fenecon",
            "mdl":"Fenecon Home",
            "ids":[
                "fenecon_home"
            ]
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
            "ids":[
                "fenecon_home"
            ]
        }
    }

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

def get_entity_device_class(unit):
    logger = logging.getLogger(__name__)
    def_cla = None
    if unit == "%":
        def_cla = "battery"
    elif unit in ["W", "mW"]:
        def_cla = "power"
    elif unit in ["Wh", "mWh", "kWh"]:
        def_cla = "energy"
    elif unit in ["V", "mV"]:
        def_cla = "voltage"
    elif unit == ["A", "mA"]:
        def_cla = "current"
    elif unit == "C":
        def_cla = "temperature"
    #elif unit == "None":
    #    def_cla = None
    return def_cla

def get_entity_state_class(device_class):
    logger = logging.getLogger(__name__)
    state_class = None
    if device_class == "energy":
        state_class = "total_increasing"
    elif device_class in ['battery', 'power', 'voltage', 'current', 'temperature']:
        state_class = "measurement"
    return state_class

def get_fems_values(fenecon_config, component, channel):
    logger = logging.getLogger(__name__)
    fems_entity_unit = fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['unit']
    fems_entity_type = fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['type']

    return fems_entity_unit, fems_entity_type

def get_entity_unit_of_measurement(unit, name, type):
    logger = logging.getLogger(__name__)
    if type == "INTEGER" and "Voltage".casefold() in name.casefold():
        unit = "V"
    # Correct Fenecons new Sum Unit. Return None if no unit is given
    return None if unit == "" else unit.replace('_Σ','')

def get_entity_value_template(c):
    logger = logging.getLogger(__name__)

    ret_val = "{{value}}"
    #if c in ["charger0/State", "charger1/State"]:
    if re.search(r'charger\d+/State', c):
        ret_val = val_tmpl_state
    elif c == "_sum/GridMode":
        ret_val = val_tmpl_gridmode
    return ret_val

def get_dirty_guess_units(c):
    logger = logging.getLogger(__name__)

    if "power" in c.lower():
        return "W"
    elif "soc" in c.lower():
        return "%"
    elif "soh" in c.lower():
        return "%"
    elif "state" in c.lower():
        return None
    elif "gridmode" in c.lower():
        return None
    elif "capacity" in c.lower():
        return "Wh"
    elif "energy" in c.lower():
        return "Wh"
    elif "voltage" in c.lower():
        return "dV"
    elif "current" in c.lower():
        return "mA"
    elif "temperature" in c.lower():
        return "°C"
    return None

def get_dirty_guess_class(c):
    logger = logging.getLogger(__name__)
    def_cla = None
    if "soc" in c.lower():
        def_cla = "battery"
    elif "soh" in c.lower():
        def_cla = "battery"
    elif "power" in c.lower():
        def_cla = "power"
    elif "energy" in c.lower():
        def_cla = "energy"
    elif "voltage" in c.lower():
        def_cla = "voltage"
    elif "current" in c.lower():
        def_cla = "current"
    elif "temperature" in c.lower():
        def_cla = "temperature"
    #elif unit == "None":
    #    def_cla = None
    return def_cla

def get_hassio_newoverwrite(c):
    logger = logging.getLogger(__name__)
    items = ['name', 'device_class', 'state_class', 'device_unit', 'value_template', 'icon']

    for i in items:
        try:
            c[i] = c[i]
        except Exception:
            c[i] = None

    return c

def get_sensor_name(channel, config):
    try:
        for e in config.lang_list['fems_channels_dict']:
            if e['channel'] == channel:
                return e[config.language]
    except Exception:
        return None

    return None

def get_hassio_overwrite(channel, config):
    logger = logging.getLogger(__name__)
    overwrite_channel = None
    overwrite_device_class = None
    overwrite_state_class = None
    overwrite_device_unit = None
    overwrite_value_template = None
    overwrite_name = None
    #"channel;device_class;state_class;device_unit;value_template"
    for overwrite in config:
        try:
            overwrite_channel, overwrite_device_class, overwrite_state_class, overwrite_device_unit, overwrite_value_template, overwrite_name = overwrite.split(';')
        except Exception:
            logger.warning(f"ERROR: Hassio overwrite can not be parsed ({overwrite})")
            continue
        if channel == overwrite_channel:
            logger.info('Hassio sensor overwrite found')
            return overwrite_device_class, overwrite_state_class, overwrite_device_unit, overwrite_value_template, overwrite_name
    return None, None, None, None, None

def publish_hassio_discovery(mqtt, fenecon_config, version):
    logger = logging.getLogger(__name__)
    logger.info('Start publish hassio dicovery')

    if config.fems_channels:
        logger.info('Processing new channel config')

        for c in config.fems_channels:

            hassio_uid = str(f"{config.hassio['sensor_uid_prefix']}{c['channel']}").replace("/", "-")
            try:
                if c['channel'] == "_sum/State":
                    c = get_hassio_newoverwrite(c)
                    json_template_device['dev']['sw'] = version
                    #json_template_device['ops'] = fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['text']
                    json_template_device['stat_t'] =  (config.hassio['mqtt_broker_hassio_queue'] + "/" + hassio_uid).lower()
                    #json_template_device['val_tpl'] = "{{value}}"
                    json_template_device['val_tpl'] = c['value_template'] or val_tmpl_state
                    mqtt.publish(config.hassio['mqtt_broker_hassio_discovery_queue'] + "/config", json.dumps(json_template_device), 0, True)
                else:
                    # check for overwrites
                    c = get_hassio_newoverwrite(c)
                    json_template_entity['uniq_id'] = hassio_uid
                    json_template_entity['object_id'] = str(f"battery_inverter_{config.hassio['sensor_name_prefix']} {c['channel']}")
                    # get default Sensor names
                    default_sensor_name = get_sensor_name(c['channel'], config)
                    json_template_entity['name'] = c['name'] or default_sensor_name or str(f"{config.hassio['sensor_name_prefix']} {c['channel']}")
                    if c['icon'] is not None:
                        json_template_entity['icon'] = c['icon']
                    ## this will not work anymore if FEMS backend provides no data
                    ##fems_unit, fems_type  = get_fems_values(fenecon_config, component, channel)
                    ##json_template_entity['unit_of_meas'] = ow_device_unit or get_entity_unit_of_measurement(fems_unit , json_template_entity['name'], fems_type)
                    #json_template_entity['dev_cla'] =  ow_device_class or get_entity_device_class(json_template_entity['unit_of_meas'])
                    json_template_entity['dev_cla'] =  c['device_class'] or get_dirty_guess_class(c['channel'])
                    json_template_entity['unit_of_measurement'] = c['device_unit'] or get_dirty_guess_units(c['channel'])
                    json_template_entity['val_tpl'] = c['value_template'] or get_entity_value_template(c['channel'])
                    json_template_entity['stat_cla'] =  c['state_class'] or get_entity_state_class(json_template_entity['dev_cla'])
                    json_template_entity['stat_t'] =  (config.hassio['mqtt_broker_hassio_queue'] + "/" + hassio_uid).lower()
                    mqtt.publish(config.hassio['mqtt_broker_hassio_discovery_queue'] + "/" + hassio_uid + "/config", json.dumps(json_template_entity), 0, True)
                    if c['icon'] is not None:
                        json_template_entity.pop('icon', None)
                continue

            except Exception:
                logger.warning(
                    f"FEMS Component or Channel not found or any other problem occured ({c['channel']})"
                )
    else:
        logger.info('Processing old channel config')
        for c in config.fenecon['fems_request_channels']:
            #if c == '_meta/Version':
            #    # only use this for updating Fenecon device in Homeassistant, we don't need this as sensor
            #    continue
            #component, channel = c.split('/')
            hassio_uid = str(f"{config.hassio['sensor_uid_prefix']}{c}").replace("/", "-")
            #logger.info(hassio_uid)
            # Data structure fenecon_config
            #  fenecon_config.result.payload.result.components.[_sum/ess0/charger0/...].channels.[ConsumptionActivePowerL2/name...]
            # Data structure config
            #  _sum/ConsumptionActivePowerL2

            # check if channel is available
            #try:
            #    if not(isinstance(fenecon_config['result']['payload']['result']['components'][component]['channels'][channel], dict)):
            #        logger.warning(f"configured channel is not available in Fenecon system configuration ({c})")
            #        continue
            #except Exception:
            #    logger.error(f"configured channel is not available in Fenecon system configuration ({c})")
            #    continue

            try:
                if c == "_sum/State":
                    json_template_device['dev']['sw'] = version
                    #json_template_device['ops'] = fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['text']
                    json_template_device['stat_t'] =  (config.hassio['mqtt_broker_hassio_queue'] + "/" + hassio_uid).lower()
                    #json_template_device['val_tpl'] = "{{value}}"
                    json_template_device['val_tpl'] = val_tmpl_state
                    mqtt.publish(config.hassio['mqtt_broker_hassio_discovery_queue'] + "/config", json.dumps(json_template_device), 0, True)
                else:
                    # check for overwrites
                    ow_device_class, ow_state_class, ow_device_unit, ow_value_template, ow_name = get_hassio_overwrite(c, config.hassio['sensor_overwrite'])
                    json_template_entity['name'] = ow_name or str(f"{config.hassio['sensor_name_prefix']} {c}")
                    json_template_entity['uniq_id'] = hassio_uid
                    ## this will not work anymore if FEMS backend provides no data
                    ##fems_unit, fems_type  = get_fems_values(fenecon_config, component, channel)
                    ##json_template_entity['unit_of_meas'] = ow_device_unit or get_entity_unit_of_measurement(fems_unit , json_template_entity['name'], fems_type)
                    #json_template_entity['dev_cla'] =  ow_device_class or get_entity_device_class(json_template_entity['unit_of_meas'])
                    json_template_entity['dev_cla'] =  ow_device_class or get_dirty_guess_class(c)
                    json_template_entity['unit_of_measurement'] = ow_device_unit or get_dirty_guess_units(c)

                    json_template_entity['val_tpl'] = ow_value_template or get_entity_value_template(c)
                    json_template_entity['stat_cla'] =  ow_state_class or get_entity_state_class(json_template_entity['dev_cla'])
                    json_template_entity['stat_t'] =  (config.hassio['mqtt_broker_hassio_queue'] + "/" + hassio_uid).lower()
                    mqtt.publish(config.hassio['mqtt_broker_hassio_discovery_queue'] + "/" + hassio_uid + "/config", json.dumps(json_template_entity), 0, True)
                continue

            except Exception:
                logger.warning(
                    f"FEMS Component or Channel not found or any other problem occured ({c})"
                )


    logger.info('End publish hassio dicovery')
    return