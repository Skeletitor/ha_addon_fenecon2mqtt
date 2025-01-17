# Home Assistant Add-on: Fenecon2Mqtt

Support forum: [hassio forum]

---

## How to use

### Requirements

1. Homeassistant with a running Supervisor
2. Fenecon Home EnergyStorage System (Maybee FEMS only works too)logger_level
3. MQTT Addon 'Mosquitto broker' [mosquitto addon]

## Add-On documentation (Container configuration)

### Config options for Hassios MQTT broker

You have to change the **_null_** ones
| Config | Type | (default)Values | Description |
|--- |--- |--- |--- |
| mqtt\*broker\*host | string (mandatory) | **_null_** | IP of MQTT broker |
| mqtt\*broker*port | number (mandatory) | 1883 | Port of MQTT broker |
| mqtt_broker_user | string (mandatory) | \*\*\_null**\* | insert your own mqtt user |
| mqtt_broker_passwd | string (mandatory) | **\_null*\*\* | insert your own mqtt user password |
| sensor_name_prefix | string (optional) | "FEMS: " | prefix used for object name generation in HA |

### Config options for Fenecon (FEMS)

| Config        | Type               | (default)Values | Description                            |
| ------------- | ------------------ | --------------- | -------------------------------------- |
| fems_ip       | string (mandatory) | **_null_**      | IP or DNS Name of Fenecon Home/FEMS    |
| fems_password | string (mandatory) | **_null_**      | Password of guest user [fems password] |

### Config options for Fenecon Channels (FEMS)

**_fems_channels_** is a collection of multiple objects. It is utilized to specify the channels to import from FEMS and allows for the modification of default values for certain sensor attributes in Home Assistant.
Each item(object) in this collection consists of the following elements:

| Config         | Type               | (default)Values | Description                                                                               |
| -------------- | ------------------ | --------------- | ----------------------------------------------------------------------------------------- |
| channel        | string (mandatory) | **_null_**      | channel ID in FEMS                                                                        |
| name           | string             | **_null_**      | Sensor name in Homeassistant                                                              |
| icon           | string             | **_null_**      | Sensor icon in Homeassistant, Use icon picket to get mdi:xys value which cna be used here |
| device_class   | string             | **_null_**      | Sensor device class in Homeassistant                                                      |
| state_class    | string             | **_null_**      | Sensor state class in Homeassistant                                                       |
| device_unit    | string             | **_null_**      | Sensor unit in Homeassistant                                                              |
| value_template | string             | **_null_**      | Sensor value template in Homeassistant                                                    |

**_language_**

Languafge of the default Sensor names. Supported are German (DE) and Engish (EN)

### General options for Add-on

| Config    | Type             | (default)Values                               | Description      |
| --------- | ---------------- | --------------------------------------------- | ---------------- |
| log_level | list (mandatory) | CRITICAL\|ERROR\|WARNING\|INFO\|DEBUG\|NOTSET | Add-on Log Level |

---

## Default configuration

The default configuration for this add-on appears as follows:

```
  hassio:
    mqtt_broker_host: null
    mqtt_broker_port: 1883
    mqtt_broker_user: null
    mqtt_broker_passwd: null
    sensor_name_prefix: "FEMS: "
  fenecon:
    fems_ip: null
    fems_password: null
  fems_channels:
//    - channel: FEMS channel name
//      name: Human readable Name (optional)
//      icon: custom mid:ICON
//      device_class: custom device class (optional)
//      state_class: custom state class (optional)
//      device_unit: custom device unit (optional)
//      value_template: custom value template (optional)
    - channel: _sum/ConsumptionActiveEnergy
    - channel: _sum/ConsumptionActivePower
    - channel: _sum/ConsumptionActivePowerL1
    - channel: _sum/ConsumptionActivePowerL2
    - channel: _sum/ConsumptionActivePowerL3
    - channel: _sum/EssActivePower
    - channel: _sum/EssActivePowerL1
    - channel: _sum/EssActivePowerL2
    - channel: _sum/EssActivePowerL3
    - channel: _sum/EssDcChargeEnergy
    - channel: _sum/EssDcDischargeEnergy
    - channel: _sum/EssSoc
    - channel: _sum/GridActivePower
    - channel: _sum/GridActivePowerL1
    - channel: _sum/GridActivePowerL2
    - channel: _sum/GridActivePowerL3
    - channel: _sum/GridBuyActiveEnergy
    - channel: _sum/GridMaxActivePower
    - channel: _sum/GridMinActivePower
    - channel: _sum/GridMode
    - channel: _sum/GridSellActiveEnergy
    - channel: _sum/ProductionActiveEnergy
    - channel: _sum/ProductionActivePower
    - channel: _sum/ProductionDcActualPower
    - channel: _sum/ProductionMaxActivePower
    - channel: _sum/State
    - channel: battery0/Soh
    - channel: battery0/Tower0NoOfCycles
    - channel: battery0/Tower0PackVoltage
      device_unit: "V"
      value_template: "{{value | int /10}}"
    - channel: batteryInverter0/AirTemperature
    - channel: batteryInverter0/ArmFmVersion
    - channel: batteryInverter0/BmsPackTemperature
    - channel: batteryInverter0/DspFmVersionMaster
    - channel: batteryInverter0/RadiatorTemperature
    - channel: batteryInverter0/TotalBackUpLoadPower
    - channel: charger0/ActualPower
    - channel: charger0/Current
    - channel: charger0/State
    - channel: charger0/Voltage
      device_unit: "V"
      value_template: "{{value | int /1000}}"
    - channel: charger1/ActualPower
    - channel: charger1/Current
    - channel: charger1/State
    - channel: charger1/Voltage
      device_unit: "V"
      value_template: "{{value | int /1000}}"
    - channel: ess0/Capacity
    - channel: ess0/DcDischargePower
  log_level: INFO
  language: EN
```

---

## Special configuration options

Getting channels:
This Add-on pushes your local Fenecon FEMS configuration into a directory of your HA OS `/share/fenecon/fenecon_config.json`. All available components ~~and channels ~~ are included. Channels are missing since FEMS 2024.06._
As a workaround you can do a REST API call and get a List of all available channels (Thx:[rest call channels]): curl -s http://x:user@FEMS-IP:80/rest/channel/._/.\* -o channel-names.txt

> [!CAUTION]
> Take care what your doing here

> [!TIP]
> Use \_sum/ProductionAcActivePower to get power values of external connected sources (e.g. inverters,...)

---

## Users and passwords

HA's mqtt broker is able to authenticate against HA's user management. So we need to add an user to HA.

### HA Mosquitto user and permissions

You need a user and password to connect to HA's mqtt broker. You're reponsible to add a user and provide teh needes permission! This add-on can't do that for you.

**_To add a HA user:_**

HA dashboard -> configuration -> persons (select users after the page loaded)

Add a new local user there (Take care, a user not a person!). This user don't need admin permissions. Note down the mqtt_username and mqtt_password. You'll need it in Add-On and mqtt broker configuration

**_Provide the mqtt broker permissions:_**

The new created user needs now permissions to write Data to two mqtt topics. The first permission (see below) is used to transmit data. The second one is to transmit device and entity data to use HA's autodiscovery feature.

ssh to /share/mosquitto.

Add the following code in your acl file to provide the user permissions to the default mqqt topic's. [mosquitto addon acl]

> [!NOTE]
> Take care, you'll have to change these entries if you change the topics in container config. Replace the "<< USERNAME >>" with your newly created username.

```
user <<USERNAME>>
topic readwrite fenecon/#

user <<USERNAME>>
topic readwrite homeassistant/sensor/fenecon/#
```

### Fenecon user and permissions

You'll need Fenecons (OpenEMS) guest user password: [fems password]

[mosquitto addon]: https://github.com/home-assistant/addons/tree/master/mosquitto
[mosquitto addon acl]: https://github.com/home-assistant/addons/blob/master/mosquitto/DOCS.md#access-control-lists-acls
[sensor overwrite]: #ha-sensor_overwrite
[fems request channels]: #fenecon-fems_request_channels
[fems password]: https://letmegooglethat.com/?q=fenecon+guest+user+password
[hassio forum]: https://community.home-assistant.io/t/add-on-fenecon2mqtt-connect-fenecon-home-openems-energy-storage-systems-to-homeassistant/561823
[rest call channels]: https://community.home-assistant.io/t/add-on-fenecon2mqtt-connect-fenecon-home-openems-energy-storage-systems-to-homeassistant/561823/36
