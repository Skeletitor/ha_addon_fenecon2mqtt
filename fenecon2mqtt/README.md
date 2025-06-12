# Home Assistant Add-on: Fenecon2Mqtt

![Build State][build-state-shield]
![CodeQL][codeql-state-badge]
[![License][license-shield]](LICENSE.md)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]


### *Retirement announcement for Fenecon2MQTT add-on*

### When’s the retirement party?
>Fenecon2MQTT will officially kick back and sip piña coladas starting June 12, 2025. After that, no more updates or support, folks!
### Where to go?
>Hop on over to the [HA-OpenEMS](https://community.home-assistant.io/t/ha-openems-fems-and-openems-integration/852706) integration for all your energy management needs. It’s the new kid on the block, and it’s ready to rock your Home Assistant setup.
### Got questions?
>Check out the [HA-OpenEMS](https://community.home-assistant.io/t/ha-openems-fems-and-openems-integration/852706) docs or swing by the community forums to chat with other smart home nerds.

Thanks for all the love you’ve shown Fenecon2MQTT over the years. 

It’s been a wild ride, but it’s time for this add-on to retire and let [HA-OpenEMS](https://community.home-assistant.io/t/ha-openems-fems-and-openems-integration/852706) take the spotlight. Let’s raise a virtual toast to new beginnings! 🥂

---

This add-on connects to Fenecon Home (FEMS) websocket and subscribes to the configured channels. This data is pushed to Hassio integrated mqtt broker. All sensors(entities) are added autmatically.

![fenecon2mqtt_img](https://github.com/Skeletitor/ha_addon_fenecon2mqtt/blob/main/fenecon2mqtt/logo.png?raw=true)

Thanks goes to [@benniju] who gives the idea of using websocket.

## Support forum
Support forum: [hassio forum]

## Requirements

1. Homeassistant with a running Supervisor
2. Fenecon Home EnergyStorage System. Tested with [Fenecon Home 10] and [Heckert Symphon-E] (thanks to 'skeal'). I guess [OpenEMS] based solutions work too.
3. MQTT Addon 'Mosquitto broker' [Mosquitto addon]

## Quick Setup

1. MQTT configuration
   - Add local user in homeassistant for mqtt broker authentication [doc link user]
   - Provide user permisson to write to the mqtt topic (e.g homeassistant/sensor/fenecon/# and fenecon/#)
2. Fenecon Home (FEMS) configuration
   - Nothing, ensure that the local IP and Port (1883) is reachalbe from Hassio
3. Addon configuration
   - Install
   - Replace all "null" values in addon configuration
   - Start addon
   - Enable Watchdog

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
[doc link user]: https://github.com/Skeletitor/ha_addon_fenecon2mqtt/blob/main/fenecon2mqtt/DOCS.md#users-and-passwords
[fenecon home 10]: https://fenecon.de/fenecon-home-10/
[openems]: https://openems.io/
[Heckert Symphon-E]: https://www.heckertsolar.com/symphon-e/
[hassio forum]: https://community.home-assistant.io/t/add-on-fenecon2mqtt-connect-fenecon-home-openems-energy-storage-systems-to-homeassistant/561823
