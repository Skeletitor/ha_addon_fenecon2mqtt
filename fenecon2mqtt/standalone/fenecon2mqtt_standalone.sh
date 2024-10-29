#!/bin/bash

if [ ! -f /data/options.json ]; then
    mkdir -p /data/
    cat << EOF > /data/options.json
{
    "hassio": {
        "mqtt_broker_host": <YOUR_MQTT_BROKER>,
        "mqtt_broker_port": 1883,
        "mqtt_broker_user": null,
        "mqtt_broker_passwd": null,
        "mqtt_broker_keepalive": 60,
        "mqtt_broker_hassio_discovery_queue": "homeassistant/sensor/fenecon",
        "mqtt_broker_hassio_queue": "fenecon",
        "sensor_overwrite": [
            "channel;device_class;state_class;device_unit;value_template;name "
        ],
        "sensor_uid_prefix": "fems-",
        "sensor_name_prefix": "FEMS: "
    },
    "fenecon": {
        "fems_ip": <YOUR_FEMS_IP>,
        "fems_password": "user",
        "fems_request_channels": [
            "_sum/ConsumptionActiveEnergy",
            "_sum/ConsumptionActivePower",
            "_sum/ConsumptionActivePowerL1",
            "_sum/ConsumptionActivePowerL2",
            "_sum/ConsumptionActivePowerL3",
            "_sum/ConsumptionMaxActivePower",
            "_sum/EssActivePower",
            "_sum/EssActivePowerL1",
            "_sum/EssActivePowerL2",
            "_sum/EssActivePowerL3",
            "_sum/EssDcChargeEnergy",
            "_sum/EssDcDischargeEnergy",
            "_sum/EssSoc",
            "_sum/GridActivePower",
            "_sum/GridActivePowerL1",
            "_sum/GridActivePowerL2",
            "_sum/GridActivePowerL3",
            "_sum/GridBuyActiveEnergy",
            "_sum/GridMaxActivePower",
            "_sum/GridMinActivePower",
            "_sum/GridMode",
            "_sum/GridSellActiveEnergy",
            "_sum/ProductionActiveEnergy",
            "_sum/ProductionActivePower",
            "_sum/ProductionDcActualPower",
            "_sum/ProductionMaxActivePower",
            "_sum/State",
            "battery0/Soh",
            "battery0/Tower0NoOfCycles",
            "battery0/Tower0PackVoltage",
            "batteryInverter0/AirTemperature",
            "batteryInverter0/ArmFmVersion",
            "batteryInverter0/BmsPackTemperature",
            "batteryInverter0/DspFmVersionMaster",
            "batteryInverter0/DspFmVersionSlave",
            "batteryInverter0/RadiatorTemperature",
            "charger0/ActualPower",
            "charger0/ActualPower",
            "charger0/Current",
            "charger0/State",
            "charger0/Voltage",
            "charger1/ActualPower",
            "charger1/ActualPower",
            "charger1/Current",
            "charger1/State",
            "charger1/Voltage",
            "charger1/Voltage",
            "ess0/Capacity",
            "ess0/DcDischargePower"
        ]
    },
    "log_level": "INFO"
}
EOF
fi

if [ -n "${MQTT_HOST}" ]; then
    sed -i "s/^\(\s*\"mqtt_broker_host\"\s*:\s*\).*/\1\"${MQTT_HOST}\",/" /data/options.json
fi
if [ -n "${MQTT_PORT}" ]; then
    sed -i "s/^\(\s*\"mqtt_broker_port\"\s*:\s*\).*/\1${MQTT_PORT},/" /data/options.json
fi
if [ -n "${MQTT_USER}" ]; then
    sed -i "s/^\(\s*\"mqtt_broker_user\"\s*:\s*\).*/\1\"${MQTT_USER}\",/" /data/options.json
fi
if [ -n "${MQTT_PASSWORD}" ]; then
    sed -i "s/^\(\s*\"mqtt_broker_passwd\"\s*:\s*\).*/\1\"${MQTT_PASSWORD}\",/" /data/options.json
fi
if [ -n "${FEMS_IP}" ]; then
    sed -i "s/^\(\s*\"fems_ip\"\s*:\s*\).*/\1\"${FEMS_IP}\",/" /data/options.json
fi
if [ -n "${FEMS_PASSWORD}" ]; then
    sed -i "s/^\(\s*\"fems_password\"\s*:\s*\).*/\1\"${FEMS_PASSWORD:-user}\",/" /data/options.json
fi

python3 /usr/bin/fenecon2mqtt/Fenecon2Mqtt.py