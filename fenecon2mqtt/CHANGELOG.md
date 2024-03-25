<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 0.2.13

- revert back

## 0.2.12

- moved to
  - paho_mqtt 2.0.0
  - rel 0.4.9.8
  - websocket_client 1.7.0

## 0.2.11

- Modified HA endity state class, entity device class, entity unit of measurement of FEMS entities without given units.
- Use FEMS entity name to set HA entity unit to "V" if FEMS entity type is integer. No need to use manual mapping anymore!
- Display user readable error message when FEMS password is wrong.

## 0.2.10

- Changed device name in Homeassistant. Devicenames should not match Entitynames in HA after 2024.2.0 version.
- updated paho_mqtt and websocket_client libraries

## 0.2.9

- Changed MQTT reconnect handling.
- Added more description when facing MQTT errors

## 0.2.8

- ignore Fenecons new unit Wh_Σ for energy values which was introduced in June 23

## 0.2.7

- pushed new dependencies
- added some sleeps while reconnecting

## 0.2.6

- Stop the addon if there is a problem with the connection to FEMS. Watchg can restart the whole addon to get a clean state.

## 0.2.5

- Test version. Let Watchdog do the reconnect if a failure occurs

## 0.2.4

- changed reconnect handling for websocket connection
- Fems version should be updated after reconnecttion

## 0.2.3

- switched mqtt client to clean sessions, we don't need persistant connections in mqtt broker
- changed mqtt initial connect behavior.
- changed file size of logfiles

## 0.2.2

- testing build pipeline

## 0.2.1

- updated documentation
- added codeql

## 0.2.0

- added option to use custom names for sensors
- fixed state_class for unknown sensors

## 0.1.9

- added some documentation
- changed device_class for 'unknown' devices
- renamed classes
- changed default values in add-on configuration

## 0.1.8

- fix bug in container config

## 0.1.7

- housekeeping of HA discovery topic. Old retained messages are purged.
- added custom prefix for HA sensor names in container config

## 0.1.6

- use retained mqtt messages, fixes entity dirconnect after Homeassistant restart

## 0.1.5

- fixed some typos
- added workaround for failing data publishing when restarting homeassistant

## 0.1.4

- switched to to correct state topic when publishing values

## 0.1.3

- changed reconnect handling for Mqtt and Feencon
- switched to logger. Logfiles under /share/fenecon/
- added custom prefix for hassion uid's in container config
- changed sensor uid's to be more hassio style like
- dump Fenecons configuration as json to /share/fenecon/fenecon_config.json

## 0.1.2

- ‼️ changed container configuration -> **redeploy addon do not not update**
- switched Hassio entity state class to total_increasing for energy values
- added temperature values in hassio
- added overwrite in container config to set your own sensor_device_class, sensor_state_class, sensor_device_unit and a value_template
- renamed Hassio sensors

## 0.1.1

- beta release

## 0.1.0

- first beta release

## 0.0.20

- development
