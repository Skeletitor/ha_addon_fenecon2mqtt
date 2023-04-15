<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

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
