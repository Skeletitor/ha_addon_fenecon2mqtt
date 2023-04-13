#!/usr/bin/python3
import json
import config

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

def get_entity_class(unit):
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
    return def_cla

def publish_hassio_discovery(mqtt, fenecon_config, version):
    print(' ** start publish hassio dicovery **')
    # manage all different Fenecon devices in one Hassio device, publish device
    #json_template_device['dev']['sw'] = version
    #mqtt.publish(config.hassio['mqtt_broker_hassio_discovery_queue'] + "config", json.dumps(json_template_device))

    i = 0
    for c in config.fenecon['request_channels']:
        component, channel = c.split('/')
        hassio_uid = str(f"fems-{c}").replace("/", "_")
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

        json_template_entity['name'] = c
        json_template_entity['uniq_id'] = hassio_uid
        json_template_entity['unit_of_meas'] = fenecon_config['result']['payload']['result']['components'][component]['channels'][channel]['unit']
        json_template_entity['val_tpl'] = "{{value}}"
        json_template_entity['dev_cla'] =  get_entity_class(json_template_entity['unit_of_meas'])
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

    print(' ** end publish hassio dicovery **')
    return