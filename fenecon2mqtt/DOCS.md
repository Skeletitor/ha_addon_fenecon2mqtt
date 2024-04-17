# Home Assistant Add-on: Fenecon2Mqtt

Support forum: [hassio forum]

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
| mqtt_broker_port | number (mandatory) | 1883 | Port of MQTT broker |
| mqtt_broker_user | string (mandatory) | **_null_** | insert your own mqtt user |
| mqtt_broker_passwd | string (mandatory) | **_null_** | insert your own mqtt user password |
| mqtt*broker_keepalive | number (mandatory) | 60 | leave it at 60 seconds |
| mqtt_broker_hassio_discovery_queue| string (mandatory) | homeassistant/sensor/fenecon | HA's Mqtt discovery topic. _Change it if you know what you're doing_ |
| mqtt*broker_hassio_queue | string (mandatory) | fenecon | HA's Mqtt topic for sensor values. _Change it if you know what you're doing_ |
| sensor*overwrite | array of strings (values optional) | | options to overwrite HA sensor properties. _Use it if you know what you're doing._ [Sensor overwrite] |
| sensor*uid_prefix | string (mandatory) | fems- | prefix used for uid generation in HA. Changing the dafault will create new sensors in HA. _Change it if you know what you're doing_ |
| sensor_name_prefix | string (optional) | "FEMS: " | prefix used for name/friendly name generation in HA |

### Config options for Fenecon (FEMS)

| Config                | Type                         | (default)Values | Description                                                                                           |
| --------------------- | ---------------------------- | --------------- | ----------------------------------------------------------------------------------------------------- |
| fems_ip               | string (mandatory)           | **_null_**      | IP or DNS Name of Fenecon Home/FEMS                                                                   |
| fems_password         | string (mandatory)           | **_null_**      | Password of guest user [fems password]                                                                               |
| fems_request_channels | array of strings (mandatory) | a lot           | List of FEMS channels to subscribe. _Change it if you know what you're doing_ [FEMS request channels] |

### General options for Add-on

| Config    | Type             | (default)Values                               | Description      |
| --------- | ---------------- | --------------------------------------------- | ---------------- |
| log_level | list (mandatory) | CRITICAL\|ERROR\|WARNING\|INFO\|DEBUG\|NOTSET | Add-on Log Level |

## Special configuration options

### HA-`sensor_overwrite`

Using this config option gives you the ability to overwrite Homeassistant Sensor definitions. You can provide multiple strings as array. Any string must contain the following systax:

```
"channel;device_class;state_class;device_unit;value_template;name "
```

| key              | descrption                                                |
| ---------------- | --------------------------------------------------------- |
| `channel`        | (mandatory) is used as key to select the FEMS channel.    |
| `device_class`   | (optional) is used to define HA's sensor device_class     |
| `state_class`    | (optional) is used to define HA's sensor state_class      |
| `device_unit`    | (optional) is used to define HA's sensor unit (V,A,W,...) |
| `value_template` | (optional) is used to define HA's sensor value_template   |
| `name`           | (optional) is used to define HA's sensor friendly name    |

E.g. if you want to use an other friendly name in HA for a sensor:

```.csv
sensor_overwrite:
  - "fenecon/fems-_meta-Version;;;;;FEMS Version "
```

### Fenecon-`fems_request_channels`

Is uses to define which FEMS channels should be transfered to a HA sensor.
You can provide multiple strings as array. Any string must contain the following systax:

```
- "component/channel"
e.g.
- _meta/Version
- _sum/EssSoc
```

This Add-on pushes your local Fenecon FEMS configuration into a directory of your HA OS `/share/fenecon/fenecon_config.json`. All available channels are included.

> [!CAUTION]
> Take care what your doing here

> [!TIP]
> Use _sum/ProductionAcActivePower to get power values of external connected sources (e.g. inverters,...) 

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
