# Home Assistant Add-on repository for Fenecon2Mqtt

### *Retirement announcement for Fenecon2MQTT add-on*

### When’s the retirement party?
>Fenecon2MQTT will officially kick back and sip piña coladas starting June 12, 2025. After that, no more updates or support, folks!
### Where to go?
>Hop on over to the [HA-OpenEMS](https://community.home-assistant.io/t/ha-openems-fems-and-openems-integration/852706) integration for all your energy management needs. It’s the new kid on the block, and it’s ready to rock your Home Assistant setup.
### Got questions?
>Check out the [HA-OpenEMS](https://community.home-assistant.io/t/ha-openems-fems-and-openems-integration/852706) docs or swing by the community forums to chat with other smart home nerds.

Thanks for all the love you’ve shown Fenecon2MQTT over the years. 

It’s been a wild ride, but it’s time for this add-on to retire and let [HA-OpenEMS](https://community.home-assistant.io/t/ha-openems-fems-and-openems-integration/852706) take the spotlight. Let’s raise a virtual toast to new beginnings! 🥂

## Add-ons

This repository contains the following add-ons

### [Fenecon2Mqtt](./fenecon2mqtt)
![Build State][build-state-shield]
![CodeQL][codeql-state-badge]

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

_Add-on is based on Hassios example add-on and Alpine Python images. Thank you very much (Hassio Devs) for you excelent work!_

<!--

Notes to developers after forking or using the github template feature:
- While developing comment out the 'image' key from 'example/config.yaml' to make the supervisor build the addon
  - Remember to put this back when pushing up your changes.
- When you merge to the 'main' branch of your repository a new build will be triggered.
  - Make sure you adjust the 'version' key in 'example/config.yaml' when you do that.
  - Make sure you update 'example/CHANGELOG.md' when you do that.
  - The first time this runs you might need to adjust the image configuration on github container registry to make it public
  - You may also need to adjust the github Actions configuration (Settings > Actions > General > Workflow > Read & Write)
- Adjust the 'image' key in 'example/config.yaml' so it points to your username instead of 'home-assistant'.
  - This is where the build images will be published to.
- Rename the example directory.
  - The 'slug' key in 'example/config.yaml' should match the directory name.
- Adjust all keys/url's that points to 'home-assistant' to now point to your user/fork.
- Share your repository on the forums https://community.home-assistant.io/c/projects/9
- Do awesome stuff!
 -->

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[build-state-shield]: https://img.shields.io/github/actions/workflow/status/Skeletitor/ha_addon_fenecon2mqtt/builder.yaml?branch=main
[codeql-state-badge]: https://github.com/Skeletitor/ha_addon_fenecon2mqtt/workflows/CodeQL/badge.svg
