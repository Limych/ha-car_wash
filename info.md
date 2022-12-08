{% if prerelease %}
### NB!: This is a Beta version!
{% endif %}
{% if (version_installed.split(".")[0:2] | join | int) < 15 %}
### ATTENTION! Breaking changes!

The mechanism for specifying the unique ID of sensors has been changed. To prevent duplicate sensors from being created, add option `unique_id: __legacy__` to the settings of already available sensors. For more information, see the component's documentation.
{% endif %}

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacs-shield]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![Support me on Patreon][patreon-shield]][patreon]

[![Community Forum][forum-shield]][forum]

_This component checks the weather forecast for several days in advance and concludes whether it is worth washing the car now._

![example][exampleimg]

## Features:

- Can use any weather provider for calculations;
- It takes into account various unusual weather conditions;
- It takes into account possible pollution of the car from melted snow even in fine weather conditions.

{% if not installed %}
## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Car Wash".

{% endif %}
## Useful Links

- [Documentation][component]
- [Report a Bug][report_bug]
- [Suggest an idea][suggest_idea]

<p align="center">* * *</p>
I put a lot of work into making this repo and component available and updated to inspire and help others! I will be glad to receive thanks from you — it will give me new strength and add enthusiasm:
<p align="center"><br>
<a href="https://www.patreon.com/join/limych?" target="_blank"><img src="http://khrolenok.ru/support_patreon.png" alt="Patreon" width="250" height="48"></a>
<br>or&nbsp;support via Bitcoin or Etherium:<br>
<a href="https://sochain.com/a/mjz640g" target="_blank"><img src="http://khrolenok.ru/support_bitcoin.png" alt="Bitcoin" width="150"><br>
16yfCfz9dZ8y8yuSwBFVfiAa3CNYdMh7Ts</a>
</p>

***

[component]: https://github.com/Limych/ha-car_wash
[commits-shield]: https://img.shields.io/github/commit-activity/y/Limych/ha-car_wash.svg?style=popout
[commits]: https://github.com/Limych/ha-car_wash/commits/dev
[hacs-shield]: https://img.shields.io/badge/HACS-Default-orange.svg?style=popout
[hacs]: https://hacs.xyz
[exampleimg]: https://github.com/Limych/ha-car_wash/raw/dev/example.jpg
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
[patreon-shield]: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3DLimych%26type%3Dpatrons&style=popout
[patreon]: https://www.patreon.com/join/limych
