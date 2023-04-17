# Home Assistant Add-on: Fenecon2Mqtt

## How to use

### Requirements

1. Homeassistant with a running Supervisor
2. Fenecon Home EnergyStorage System (Maybee FEMS only works too)logger_level
3. MQTT Addon 'Mosquitto broker' [mosquitto addon]

## Add-On documentation (Container configration)
### Config options for Hassios MQTT broker
You have to change the **_highlighted_** ones
| Config   | Type | (default)Values      | Description      |
|---    |---    |---    |---    |
| mqtt_broker_host | string (mandatory) | **_null_** | IP of MQTT broker |
| mqtt_broker_port | number (mandatory) | 1883 | Port of MQTT broker |
| mqtt_broker_user | string (mandatory) | **_null_** | insert your own mqtt user |
| mqtt_broker_passwd | string (mandatory) | **_null_** | insert your own mqtt user password |
| mqtt_broker_keepalive | number (mandatory) | 60 | leave it at 60 seconds |
| mqtt_broker_hassio_discovery_queue| string (mandatory) | homeassistant/sensor/fenecon | HA's Mqtt discovery topic. _Change it if you know what you're doing_ |
| mqtt_broker_hassio_queue | string (mandatory) | fenecon | HA's Mqtt topic for sensor values. _Change it if you know what you're doing_ |
| sensor_overwrite | array of strings (values optional) | -"channel;device_class;state_class;device_unit;value_template" -"battery0/Tower0PackVoltage;voltage;measurement;V;{{value}}" | options to overwrite HA sensor properties. Use it if you know what you're doing |
| sensor_uid_prefix | string (mandatory) | fems- | prefix used for uid generation in HA. Changing the dafault will create new sensors in HA. _Change it if you know what you're doing_ |
| sensor_name_prefix | string (optional) | "FEMS: " | prefix used for name/friendly name generation in HA |
  
### Config options for Fenecon (FEMS)
| Config   | Type | (default)Values      | Description      |
|---    |---    |---    |---    |
| fems_ip | string (mandatory) | **_null_** | IP or DNS Name of Fenecon Home/FEMS |
| fems_password | string (mandatory) | **_null_** | Password of guest user |
| fems_request_channels | array of strings (mandatory) | a lot | List of all FEMS channels to subscribe. _Change it if you know what you're doing_ |
### General options for Add-on 
| Config   | Type | (default)Values      | Description      |
|---    |---    |---    |---    |
| log_level | list (mandatory) | CRITICAL\|ERROR\|WARNING\|INFO\|DEBUG\|NOTSET  | Add-on Log Level |

## TODO

- Apparmor configuration
- Fenecon Version state update on the fly. This works only when add-on restarts atm.

[mosquitto addon]: (https://github.com/home-assistant/addons/tree/master/mosquitto)
