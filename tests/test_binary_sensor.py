"""The test for the binary sensor platform."""
# pylint: disable=redefined-outer-name
import pytest
from homeassistant.components.weather import (
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_FORECAST,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_WEATHER_TEMPERATURE,
)
from homeassistant.const import (
    CONF_NAME,
    CONF_PLATFORM,
    STATE_OFF,
    STATE_ON,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest import raises
from pytest_homeassistant_custom_component.common import assert_setup_component

from custom_components.car_wash.binary_sensor import CarWashBinarySensor
from custom_components.car_wash.const import CONF_WEATHER, DOMAIN, ICON

TEST_UNIQUE_ID = "test_id"
TEST_NAME = "test_name"
TEST_WEATHER = "weather.test_monitored"
TEST_DAYS = 2

TEST_CONFIG = {
    CONF_PLATFORM: DOMAIN,
    CONF_NAME: "test",
    CONF_WEATHER: "weather.test_monitored",
}


@pytest.fixture()
async def mock_weather(hass: HomeAssistant):
    """Mock weather entity."""
    assert await async_setup_component(
        hass,
        "weather",
        {
            "weather": {
                "platform": "template",
                "name": "test_monitored",
                "condition_template": "{{ 0 }}",
                "temperature_template": "{{ 0 }}",
                "humidity_template": "{{ 0 }}",
            }
        },
    )
    await hass.async_block_till_done()


async def test_entity_initialization(hass: HomeAssistant):
    """Test sensor initialization."""
    entity = CarWashBinarySensor(None, TEST_NAME, TEST_WEATHER, TEST_DAYS)

    assert entity.unique_id is None

    entity = CarWashBinarySensor("__legacy__", TEST_NAME, TEST_WEATHER, TEST_DAYS)

    assert entity.unique_id == "car_wash-test_monitored"

    entity = CarWashBinarySensor(TEST_UNIQUE_ID, TEST_NAME, TEST_WEATHER, TEST_DAYS)

    assert entity.unique_id == TEST_UNIQUE_ID
    assert entity.name == TEST_NAME
    assert entity.device_class == f"{DOMAIN}__"
    assert entity.should_poll is False
    assert entity.available is False
    assert entity.is_on is None
    assert entity.icon is ICON


async def test_async_setup_platform(hass: HomeAssistant, mock_weather):
    """Test platform setup."""
    with assert_setup_component(1, "binary_sensor"):
        assert await async_setup_component(
            hass,
            "binary_sensor",
            {
                "binary_sensor": TEST_CONFIG,
            },
        )
    await hass.async_block_till_done()

    await hass.async_start()
    await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.test")
    assert state is not None
    assert state.state == STATE_ON

    hass.states.async_set(
        "weather.test_monitored", ATTR_CONDITION_RAINY, {ATTR_FORECAST: {}}
    )
    await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.test")
    assert state is not None
    assert state.state == STATE_OFF


# pylint: disable=protected-access
async def test__temp2c():
    """Test temperature conversions."""
    assert CarWashBinarySensor._temp2c(10, TEMP_CELSIUS) == 10
    assert round(CarWashBinarySensor._temp2c(10, TEMP_FAHRENHEIT), 2) == -12.22
    assert CarWashBinarySensor._temp2c(None, TEMP_CELSIUS) is None


async def test_async_update(hass: HomeAssistant, mock_weather):
    """Test platform setup."""
    entity = CarWashBinarySensor(
        TEST_UNIQUE_ID, TEST_NAME, "weather.nonexistent", TEST_DAYS
    )
    entity.hass = hass
    with raises(HomeAssistantError):
        await entity.async_update()

    entity = CarWashBinarySensor(TEST_UNIQUE_ID, TEST_NAME, TEST_WEATHER, TEST_DAYS)
    entity.hass = hass
    assert entity.is_on is None

    hass.states.async_set("weather.test_monitored", None)
    with raises(HomeAssistantError):
        await entity.async_update()

    hass.states.async_set(
        "weather.test_monitored", ATTR_CONDITION_RAINY, {ATTR_FORECAST: []}
    )
    await entity.async_update()
    assert entity.is_on is False

    today = dt_util.start_of_local_day()
    today_ts = int(today.timestamp() * 1000)
    day = days = 86400000

    hass.states.async_set(
        "weather.test_monitored",
        ATTR_CONDITION_SUNNY,
        {
            ATTR_FORECAST: [
                {
                    ATTR_FORECAST_TIME: int(today_ts - day),
                },
                {
                    ATTR_FORECAST_TIME: today,
                    ATTR_FORECAST_PRECIPITATION: "null",
                },
                {
                    ATTR_FORECAST_TIME: int(today_ts + 3 * days),
                },
            ]
        },
    )
    await entity.async_update()
    assert entity.is_on is True

    hass.states.async_set(
        "weather.test_monitored",
        ATTR_CONDITION_SUNNY,
        {
            ATTR_FORECAST: [
                {
                    ATTR_FORECAST_TIME: today,
                    ATTR_FORECAST_PRECIPITATION: 1,
                },
            ]
        },
    )
    await entity.async_update()
    assert entity.is_on is False

    hass.states.async_set(
        "weather.test_monitored",
        ATTR_CONDITION_SUNNY,
        {
            ATTR_FORECAST: [
                {
                    ATTR_FORECAST_TIME: today,
                    ATTR_FORECAST_CONDITION: ATTR_CONDITION_RAINY,
                },
            ]
        },
    )
    await entity.async_update()
    assert entity.is_on is False

    hass.states.async_set(
        "weather.test_monitored",
        ATTR_CONDITION_SUNNY,
        {
            ATTR_WEATHER_TEMPERATURE: 0,
            ATTR_FORECAST: [
                {
                    ATTR_FORECAST_TIME: today,
                },
                {
                    ATTR_FORECAST_TIME: int(today_ts + day),
                    ATTR_FORECAST_TEMP_LOW: -1,
                    ATTR_FORECAST_TEMP: -1,
                },
                {
                    ATTR_FORECAST_TIME: int(today_ts + 2 * days),
                    ATTR_FORECAST_TEMP_LOW: 1,
                },
            ],
        },
    )
    await entity.async_update()
    assert entity.is_on is False

    hass.states.async_set(
        "weather.test_monitored",
        ATTR_CONDITION_SUNNY,
        {
            ATTR_WEATHER_TEMPERATURE: -1,
            ATTR_FORECAST: [
                {
                    ATTR_FORECAST_TIME: today,
                },
                {
                    ATTR_FORECAST_TIME: int(today_ts + day),
                    ATTR_FORECAST_TEMP: 1,
                },
            ],
        },
    )
    await entity.async_update()
    assert entity.is_on is False
