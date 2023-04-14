# Home Assistant Add-on: Fenecon2Mqtt

![Build State][build-state-shield]
[![License][license-shield]](LICENSE.md)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

This add-on connects to Fenecon Home (FEMS) websocket and subscribes to the configured channels. This data is pushed to Hassio integrated mqtt broker. All sensors(entities) are added autmatically.

Thanks goes to @benniju who gives the idea of using websocket.

## Requirements

1. Homeassistant with a running Supervisor
2. Fenecon Home EnergyStorage System (Maybee FEMS only works too)
3. MQTT Addon 'Mosquitto broker' [Mosquitto addon]

## Quick Setup

1. MQTT configuration
   - Add local user in homeassistant for mqtt broker authentication
   - Provide user permisson to write to the mqtt topic (e.g share/mosquitto/acl.conf)
2. Fenecon Home (FEMS) configuration
   - Noting, ensure that the local IP and Port (1883) is reachalbe from Hassio
3. Addon configuration
   - Install
   - Replace all "<< \* >>" marked data in addon configuration
   - Start addon

##

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[license-shield]: https://img.shields.io/github/license/Skeletitor/hassio_addons
[build-state-shield]: https://img.shields.io/github/actions/workflow/status/Skeletitor/hassio_addons/builder.yaml?branch=main
[mosquitto addon]: (https://github.com/home-assistant/addons/tree/master/mosquitto)
