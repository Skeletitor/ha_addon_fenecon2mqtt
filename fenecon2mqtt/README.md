# Home Assistant Add-on: Fenecon2Mqtt

![Build State][build-state-shield]
![CodeQL][codeql-state-badge]
[![License][license-shield]](LICENSE.md)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

This add-on connects to Fenecon Home (FEMS) websocket and subscribes to the configured channels. This data is pushed to Hassio integrated mqtt broker. All sensors(entities) are added autmatically.

![fenecon2mqtt_img](https://github.com/Skeletitor/ha_addon_fenecon2mqtt/blob/main/fenecon2mqtt/logo.png?raw=true)

Thanks goes to [@benniju] who gives the idea of using websocket.

## Requirements

1. Homeassistant with a running Supervisor
2. Fenecon Home EnergyStorage System (tested with [Fenecon Home 10]. I guess [OpenEMS] based solutions work too)
3. MQTT Addon 'Mosquitto broker' [Mosquitto addon]

## Quick Setup

1. MQTT configuration
   - Add local user in homeassistant for mqtt broker authentication
   - Provide user permisson to write to the mqtt topic (e.g share/mosquitto/acl.conf)
2. Fenecon Home (FEMS) configuration
   - Nothing, ensure that the local IP and Port (1883) is reachalbe from Hassio
3. Addon configuration
   - Install
   - Replace all "null" values in addon configuration
   - Start addon

## Documentation

[Doc link]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[license-shield]: https://img.shields.io/github/license/Skeletitor/ha_addon_fenecon2mqtt
[build-state-shield]: https://img.shields.io/github/actions/workflow/status/Skeletitor/ha_addon_fenecon2mqtt/builder.yaml?branch=main
[codeql-state-badge]: https://github.com/Skeletitor/ha_addon_fenecon2mqtt/workflows/CodeQL/badge.svg
[mosquitto addon]: (https://github.com/home-assistant/addons/tree/master/mosquitto)
[@benniju]: https://github.com/benniju
[doc link]: ./DOCS.md
[fenecon home 10]: https://fenecon.de/fenecon-home-10/
[openems]: https://openems.io/
