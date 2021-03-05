#
#  Copyright (c) 2019-2021, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
#
"""
The Car Wash binary sensor.

For more details about this platform, please refer to the documentation at
https://github.com/Limych/ha-car_wash/
"""

# Base component constants
NAME = "Car Wash"
DOMAIN = "car_wash"
VERSION = "1.2.17.dev0"
ISSUE_URL = "https://github.com/Limych/ha-car_wash/issues"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have ANY issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

# Icons

# Device classes

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH]

# Configuration and options
CONF_WEATHER = "weather"
CONF_DAYS = "days"

# Defaults
DEFAULT_NAME = "Car Wash"
DEFAULT_DAYS = 2

# Attributes


BAD_CONDITIONS = [
    "lightning-rainy",
    "rainy",
    "pouring",
    "snowy",
    "snowy-rainy",
    "hail",
    "exceptional",
]
