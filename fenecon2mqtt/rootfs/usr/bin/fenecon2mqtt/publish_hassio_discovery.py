#!/usr/bin/python3
import json
import config
import logging

logger = logging.getLogger(__name__)

json_template_device = {
        "name":"Fenecon Home",
        "uniq_id":"fenecon",
        "stat_t": "",
        "val_tpl":"",
        "ops" : "",
        "dev":{
            "name":"Fenecon Home",
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
        "stat_t": "",
        "unit_of_meas": "",
        "stat_cla": "measurement",
        "dev_cla": "",
        "val_tpl": "",
        "dev":{
            "ids":[
                "fenecon_home"
            ]
        }
    }

def get_entity_device_class(unit):
    logger = logging.getLogger(__name__)
    def_cla = "None"
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
    return def_cla

def get_entity_state_class(device_class):
    logger = logging.getLogger(__name__)
    state_class = None
    if device_class == "energy":
        state_class = "total_increasing"
    else:
        state_class = "measurement"
    return state_class

def get_entity_device_unit(fenecon_unit):
    logger = logging.getLogger(__name__)
    return fenecon_unit

def get_entity_value_template(value_template):
    logger = logging.getLogger(__name__)
    return value_template

def get_hassio_overwrite(channel, config):
    logger = logging.getLogger(__name__)
    overwrite_channel = None
    overwrite_device_class = None
    overwrite_state_class = None
    overwrite_device_unit = None
    overwrite_value_template = None
    #"channel;device_class;state_class;device_unit;value_template"
    for overwrite in config:
        try:
            overwrite_channel, overwrite_device_class, overwrite_state_class, overwrite_device_unit, overwrite_value_template = overwrite.split(';')
        except Exception:
            logger.warning(f"ERROR: Hassio overwrite can not be parsed ({overwrite})")
            continue
        if channel == overwrite_channel:
            logger.info('Hassio sensor overwrite found')
            return overwrite_device_class, overwrite_state_class, overwrite_device_unit, overwrite_value_template
    return None, None, None, None

def publish_hassio_discovery(mqtt, fenecon_config, version):
    logger = logging.getLogger(__name__)
    logger.info('start publish hassio dicovery')

    i = 0
    for c in config.fenecon['fems_request_channels']:
        component, channel = c.split('/')
        hassio_uid = str(f"{config.hassio['sensor_uid_prefix']}{c}").replace("/", "-")
        #logger.info(hassio_uid)
        # Data structure fenecon_config
        #  fenecon_config.result.payload.result.components.[_sum/ess0/charger0/...].channels.[ConsumptionActivePowerL2/name...]
        # Data structure config
        #  _sum/ConsumptionActivePowerL2

        # check if channel is available
        try:
            if not(isinstance(fenecon_config['result']['payload']['result']['components'][component]['channels'][channel], dict)):
                print(f"ERROR: configured channel is not available in Fenecon system configuration ({c})")
                continue
        except Exception:
            print(f"ERROR: configured channel is not available in Fenecon system configuration ({c})")
            continue

        # check for overwrites
        ow_device_class, ow_state_class, ow_device_unit, ow_value_template = get_hassio_overwrite(c, config.hassio['sensor_overwrite'])

        json_template_entity['name'] = str(f"FEMS: {c}")
        json_template_entity['uniq_id'] = hassio_uid
        #json_template_entity['unit_of_meas'] = get_entity_device_unit(fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['unit'])
        #json_template_entity['unit_of_meas'] = ow_device_unit if ow_device_unit else get_entity_device_unit(fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['unit'])
        json_template_entity['unit_of_meas'] = ow_device_unit or get_entity_device_unit(fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['unit'])
        #json_template_entity['val_tpl'] = get_entity_value_template("{{value}}")
        #json_template_entity['val_tpl'] = ow_value_template if ow_value_template else get_entity_value_template("{{value}}")
        json_template_entity['val_tpl'] = ow_value_template or get_entity_value_template("{{value}}")
        #json_template_entity['dev_cla'] =  get_entity_device_class(json_template_entity['unit_of_meas'])
        #json_template_entity['dev_cla'] =  ow_device_class if ow_device_class else get_entity_device_class(json_template_entity['unit_of_meas'])
        json_template_entity['dev_cla'] =  ow_device_class or get_entity_device_class(json_template_entity['unit_of_meas'])
        #json_template_entity['stat_cla'] =  get_entity_state_class(json_template_entity['dev_cla'])
        #json_template_entity['stat_cla'] =  ow_state_class if ow_state_class else get_entity_state_class(json_template_entity['dev_cla'])
        json_template_entity['stat_cla'] =  ow_state_class or get_entity_state_class(json_template_entity['dev_cla'])
        json_template_entity['stat_t'] =  config.hassio['mqtt_broker_hassio_queue'] + "/" + hassio_uid

        #print(config.hassio['mqtt_broker_hassio_discovery_queue'] + hassio_uid + "/config")
        if c == "_sum/State":
            json_template_device['dev']['sw'] = version
            json_template_device['ops'] = fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['text']
            json_template_device['stat_t'] =  config.hassio['mqtt_broker_hassio_queue'] + "/" + hassio_uid
            json_template_device['val_tpl'] = "{{value}}"
            mqtt.publish(config.hassio['mqtt_broker_hassio_discovery_queue'] + "/config", json.dumps(json_template_device))
        else:
            #print(json_template_entity)
            mqtt.publish(config.hassio['mqtt_broker_hassio_discovery_queue'] +"/" + hassio_uid + "/config", json.dumps(json_template_entity))

    logger.info('end publish hassio dicovery')
    return