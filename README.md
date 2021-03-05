*Please :star: this repo if you find it useful*

# Car Wash Binary Sensor for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE.md)

[![hacs][hacs-shield]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Community Forum][forum-shield]][forum]

_This component checks the weather forecast for several days in advance and concludes whether it is worth washing the car now._

![example][exampleimg]

> **_Note_**:\
> You can find a real example of using this component in [my Home Assistant configuration](https://github.com/Limych/HomeAssistantConfiguration).

I also suggest you [visit the support topic][forum] on the community forum.

## Installation

### Install from HACS (recommended)

1. Have [HACS][hacs] installed, this will allow you to easily manage and track updates.
1. Search for "Car Wash".
1. Click Install below the found integration.

... then if you want to use `configuration.yaml` to configure sensor...
1. Add `car_wash` sensor to your `configuration.yaml` file. See configuration examples below.
1. Restart Home Assistant

### Manual installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `car_wash`.
1. Download file `car_wash.zip` from the [latest release section][releases-latest] in this repository.
1. Extract _all_ files from this archive you downloaded in the directory (folder) you created.

... then if you want to use `configuration.yaml` to configure sensor...
1. Add `car_wash` sensor to your `configuration.yaml` file. See configuration examples below.
1. Restart Home Assistant

### Configuration Examples

```yaml
# Example configuration.yaml entry
binary_sensor:
  - platform: car_wash
    weather: weather.gismeteo_daily
```

This sensor should work with any weather provider in any of it settings. But please note that the sensor cannot see further than the weather provider shows. Therefore, it is recommended to set the `daily` mode in the weather provider settings. If necessary, you can configure a separate weather provider instance especially for this sensor.

> **_Note_**:\
> Unfortunately, the binary sensor can show only two states — “on” and “off”.
> In the case of this sensor, “on” should be interpreted as *“it is worth washing the car”*, and “off” — as *“you should not wash the car”*.

<p align="center">* * *</p>
I put a lot of work into making this repo and component available and updated to inspire and help others! I will be glad to receive thanks from you — it will give me new strength and add enthusiasm:
<p align="center"><br>
<a href="https://www.patreon.com/join/limych?" target="_blank"><img src="http://khrolenok.ru/support_patreon.png" alt="Patreon" width="250" height="48"></a>
<br>or&nbsp;support via Bitcoin or Etherium:<br>
<a href="https://sochain.com/a/mjz640g" target="_blank"><img src="http://khrolenok.ru/support_bitcoin.png" alt="Bitcoin" width="150"><br>
16yfCfz9dZ8y8yuSwBFVfiAa3CNYdMh7Ts</a>
</p>

### Configuration Variables

**weather:**\
  _(string) (Required)_\
  Weather provider entity ID.

**name:**\
  _(string) (Optional) (Default value: 'Car Wash')_\
  Name to use in the frontend.

**days:**\
  _(integer) (Optional) (Default value: 2)_\
  The number of days how far forward the sensor looks for the weather forecast.

## Usage examples

Follow the link to see example how you can use [this sensor in automations](https://community.home-assistant.io/t/car-wash-binary-sensor/110046/20).

## Track updates

You can automatically track new versions of this component and update it by [HACS][hacs].

## Troubleshooting

To enable debug logs use this configuration:
```yaml
# Example configuration.yaml entry
logger:
  default: info
  logs:
    custom_components.car_wash: debug
```
... then restart HA.

## Contributions are welcome!

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We have set up a separate document containing our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Authors & contributors

The original setup of this component is by [Andrey "Limych" Khrolenok](https://github.com/Limych).

For a full list of all authors and contributors,
check [the contributor's page][contributors].

## License

creative commons Attribution-NonCommercial-ShareAlike 4.0 International License

See separate [license file](LICENSE.md) for full text.

***

[component]: https://github.com/Limych/ha-car_wash
[commits-shield]: https://img.shields.io/github/commit-activity/y/Limych/ha-car_wash.svg?style=popout
[commits]: https://github.com/Limych/ha-car_wash/commits/master
[hacs-shield]: https://img.shields.io/badge/HACS-Default-orange.svg?style=popout
[hacs]: https://hacs.xyz
[exampleimg]: https://github.com/Limych/ha-car_wash/raw/master/example.jpg
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=popout
[forum]: https://community.home-assistant.io/t/car-wash-binary-sensor/110046
[license]: https://github.com/Limych/ha-car_wash/blob/main/LICENSE.md
[license-shield]: https://img.shields.io/badge/license-Creative_Commons_BY--NC--SA_License-lightgray.svg?style=popout
[maintenance-shield]: https://img.shields.io/badge/maintainer-Andrey%20Khrolenok%20%40Limych-blue.svg?style=popout
[releases-shield]: https://img.shields.io/github/release/Limych/ha-car_wash.svg?style=popout
[releases]: https://github.com/Limych/ha-car_wash/releases
[releases-latest]: https://github.com/Limych/ha-car_wash/releases/latest
[user_profile]: https://github.com/Limych
[report_bug]: https://github.com/Limych/ha-car_wash/issues/new?template=bug_report.md
[suggest_idea]: https://github.com/Limych/ha-car_wash/issues/new?template=feature_request.md
[contributors]: https://github.com/Limych/ha-car_wash/graphs/contributors
