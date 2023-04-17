<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->
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
