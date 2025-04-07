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
        "sensor_name_prefix": "FEMS: "
    },
    "fenecon": {
        "fems_ip": <YOUR_FEMS_IP>,
        "fems_password": "user",
    },
    "sensor_language": "EN",
    "fems_channels": [
        {
          "channel":  "_sum/ConsumptionActiveEnergy"
        },
        {
          "channel":  "_sum/ConsumptionActivePower"
        },
        {
          "channel":  "_sum/ConsumptionActivePowerL1"
        },
        {
          "channel":  "_sum/ConsumptionActivePowerL2"
        },
        {
          "channel": " _sum/ConsumptionActivePowerL3"
        },
        {
          "channel":  "_sum/ConsumptionMaxActivePower"
        },
        {
          "channel":  "_sum/EssActivePower"
        },
        {
          "channel":  "_sum/EssActivePowerL1"
        },
        {
          "channel":  "_sum/EssActivePowerL2"
        },
        {
          "channel":  "_sum/EssActivePowerL3"
        },
        {
          "channel":  "_sum/EssDcChargeEnergy"
        },
        {
          "channel":  "_sum/EssDcDischargeEnergy"
        },
        {
          "channel":  "_sum/EssDischargePower"
        },
        {
          "channel":  "_sum/EssSoc"
        },
        {
          "channel":  "_sum/GridActivePower"
        },
        {
          "channel": " _sum/GridActivePowerL1"
        },
        {
          "channel":  "_sum/GridActivePowerL2"
        },
        {
          "channel":  "_sum/GridActivePowerL3"
        },
        {
          "channel": " _sum/GridBuyActiveEnergy"
        },
        {
          "channel":  "_sum/GridMaxActivePower"
        },
        {
          "channel": " _sum/GridMinActivePower"
        },
        {
          "channel":  "_sum/GridMode"
        },
        {
          "channel": " _sum/GridSellActiveEnergy"
        },
        {
          "channel":  "_sum/ProductionActiveEnergy"
        },
        {
          "channel": " _sum/ProductionActivePower"
        },
        {
          "channel": " _sum/ProductionDcActualPower"
        },
        {
          "channel": " _sum/ProductionMaxActivePower"
        },
        {
          "channel": " _sum/State"
        },
        {
          "channel":  "battery0/Soh"
        },
        {
          "channel":  "battery0/Tower0NoOfCycles"
        },
        {
          "channel": " battery0/Tower0PackVoltage"
        },
        {
          "channel":  "batteryInverter0/AirTemperature"
        },
        {
          "channel":  "batteryInverter0/ArmFmVersion"
        },
        {
          "channel":  "batteryInverter0/BmsPackTemperature"
        },
        {
          "channel":  "batteryInverter0/DspFmVersionMaster"
        },
        {
          "channel":  "batteryInverter0/DspFmVersionSlave"
        },
        {
          "channel":  "batteryInverter0/RadiatorTemperature"
        },
        {
          "channel":  "charger0/ActualPower"
        },
        {
          "channel":  "charger0/Current"
        },
        {
          "channel":  "charger0/State"
        },
        {
          "channel":  "charger0/Voltage",
          "device_unit": "V",
          "value_template": "{{value | int /10}}",
          "icon": "mdi:air-filter"
        },
        {
          "channel": " charger1/ActualPower"
        },
        {
          "channel":  "charger1/Current"
        },
        {
          "channel":  "charger1/State"
        },
        {
          "channel":  "charger1/Voltage"
        },
        {
          "channel":  "charger1/Voltage"
        },
        {
          "channel":  "ess0/Capacity"
        },
        {
          "channel":  "ess0/DcDischargePower"
        }
    ],
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