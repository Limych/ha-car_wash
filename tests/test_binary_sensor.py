"""The test for the binary sensor platform."""

# pylint: disable=redefined-outer-name
from typing import Final
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.components.weather import (
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_WEATHER_TEMPERATURE,
    SERVICE_GET_FORECASTS,
    WeatherEntityFeature,
)
from homeassistant.components.weather import (
    DOMAIN as WEATHER_DOMAIN,
)
from homeassistant.const import (
    ATTR_SUPPORTED_FEATURES,
    CONF_PLATFORM,
    CONF_TYPE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, ServiceRegistry, SupportsResponse
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_mock_service

from custom_components.car_wash.binary_sensor import (
    CarWashBinarySensor,
    async_setup_platform,
)
from custom_components.car_wash.const import CONF_WEATHER, DOMAIN, ICON

MOCK_ENTITY: Final = DOMAIN + ".test"
MOCK_UNIQUE_ID: Final = "test_id"
MOCK_NAME: Final = "test_name"
MOCK_WEATHER_ENTITY_NAME: Final = "test"
MOCK_WEATHER_ENTITY: Final = WEATHER_DOMAIN + "." + MOCK_WEATHER_ENTITY_NAME
MOCK_DAYS: Final = 2

MOCK_CONFIG: Final = {
    CONF_PLATFORM: DOMAIN,
    CONF_WEATHER: MOCK_WEATHER_ENTITY,
}


@pytest.fixture
def default_sensor(hass: HomeAssistant):
    """Create an AverageSensor with default values."""
    entity = CarWashBinarySensor(
        MOCK_UNIQUE_ID, MOCK_NAME, MOCK_WEATHER_ENTITY, MOCK_DAYS
    )
    entity.hass = hass
    return entity


@pytest.mark.parametrize(
    ("uid", "expected_uid"),
    [
        (None, None),
        ("__legacy__", DOMAIN + "-" + MOCK_WEATHER_ENTITY_NAME),
        (MOCK_UNIQUE_ID, MOCK_UNIQUE_ID),
    ],
)
async def test_entity_initialization(hass: HomeAssistant, uid, expected_uid):
    """Test sensor initialization."""
    entity = CarWashBinarySensor(uid, MOCK_NAME, MOCK_WEATHER_ENTITY, MOCK_DAYS)

    assert entity.unique_id == expected_uid
    assert entity.name == MOCK_NAME
    assert entity.device_class == f"{DOMAIN}__"
    assert entity.should_poll is False
    assert entity.available is False
    assert entity.is_on is None
    assert entity.icon is ICON


async def test_async_setup_platform(hass: HomeAssistant):
    """Test platform setup."""
    async_add_entities = MagicMock()

    await async_setup_platform(hass, MOCK_CONFIG, async_add_entities, None)
    assert async_add_entities.called


# pylint: disable=protected-access
@pytest.mark.parametrize(
    ("temp1", "temp2"),
    [(0, -17.78), (10, -12.22), (20, -6.67), (30, -1.11), (40, 4.44), (50, 10)],
)
async def test__temp2c(temp1, temp2):
    """Test temperature conversions."""
    assert CarWashBinarySensor._temp2c(temp1, UnitOfTemperature.CELSIUS) == temp1
    assert (
        round(CarWashBinarySensor._temp2c(temp1, UnitOfTemperature.FAHRENHEIT), 2)
        == temp2
    )
    assert CarWashBinarySensor._temp2c(None, UnitOfTemperature.CELSIUS) is None


async def test_async_update_fail(hass: HomeAssistant):
    """Test component update fail."""
    entity = CarWashBinarySensor(
        MOCK_UNIQUE_ID, MOCK_NAME, WEATHER_DOMAIN + ".nonexistent", MOCK_DAYS
    )
    entity.hass = hass
    with pytest.raises(HomeAssistantError):
        await entity.async_update()


async def test_async_update_forecast_fail(hass: HomeAssistant, default_sensor):
    """Test sensor update on forecast fail."""
    async_mock_service(
        hass,
        WEATHER_DOMAIN,
        SERVICE_GET_FORECASTS,
        supports_response=SupportsResponse.OPTIONAL,
    )

    with pytest.raises(HomeAssistantError, match="Unable to find an entity"):
        await default_sensor.async_update()

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        "State",
        attributes={
            ATTR_WEATHER_TEMPERATURE: -1,
        },
    )

    with pytest.raises(HomeAssistantError, match="doesn't support any forecast"):
        await default_sensor.async_update()

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        "State",
        attributes={
            ATTR_WEATHER_TEMPERATURE: -1,
            ATTR_SUPPORTED_FEATURES: "unexpected",
        },
    )

    with pytest.raises(TypeError):
        await default_sensor.async_update()


async def test_async_update(hass: HomeAssistant, default_sensor):
    """Test component update."""
    assert default_sensor.is_on is None

    hass.states.async_set(MOCK_WEATHER_ENTITY, None)

    with pytest.raises(HomeAssistantError):
        await default_sensor.async_update()

    hass.states.async_set(MOCK_WEATHER_ENTITY, "State")

    with pytest.raises(HomeAssistantError):
        await default_sensor.async_update()

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        "State",
        attributes={
            ATTR_WEATHER_TEMPERATURE: -1,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_DAILY
            | WeatherEntityFeature.FORECAST_TWICE_DAILY
            | WeatherEntityFeature.FORECAST_HOURLY,
        },
    )

    with patch.object(ServiceRegistry, "async_call") as call:
        await default_sensor.async_update()
        assert call.call_args.args[2][CONF_TYPE] == "daily"

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        "State",
        attributes={
            ATTR_WEATHER_TEMPERATURE: -1,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_TWICE_DAILY
            | WeatherEntityFeature.FORECAST_HOURLY,
        },
    )

    with patch.object(ServiceRegistry, "async_call") as call:
        await default_sensor.async_update()
        assert call.call_args.args[2][CONF_TYPE] == "twice_daily"

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        "State",
        attributes={
            ATTR_WEATHER_TEMPERATURE: -1,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_HOURLY,
        },
    )

    with patch.object(ServiceRegistry, "async_call") as call:
        await default_sensor.async_update()
        assert call.call_args.args[2][CONF_TYPE] == "hourly"

    today = dt_util.start_of_local_day()
    today_ts = int(today.timestamp() * 1000)
    day = days = 86400000

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        ATTR_CONDITION_RAINY,
        attributes={
            ATTR_WEATHER_TEMPERATURE: 12,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_DAILY,
        },
    )
    async_mock_service(
        hass,
        WEATHER_DOMAIN,
        SERVICE_GET_FORECASTS,
        response={MOCK_WEATHER_ENTITY: {"forecast": []}},
    )

    await default_sensor.async_update()
    assert default_sensor.is_on is False

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        ATTR_CONDITION_SUNNY,
        attributes={
            ATTR_WEATHER_TEMPERATURE: 12,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_DAILY,
        },
    )
    async_mock_service(
        hass,
        WEATHER_DOMAIN,
        SERVICE_GET_FORECASTS,
        response={
            MOCK_WEATHER_ENTITY: {
                "forecast": [
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
            }
        },
    )

    await default_sensor.async_update()
    assert default_sensor.is_on is True

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        ATTR_CONDITION_SUNNY,
        attributes={
            ATTR_WEATHER_TEMPERATURE: 12,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_DAILY,
        },
    )
    async_mock_service(
        hass,
        WEATHER_DOMAIN,
        SERVICE_GET_FORECASTS,
        response={
            MOCK_WEATHER_ENTITY: {
                "forecast": [
                    {
                        ATTR_FORECAST_TIME: today,
                        ATTR_FORECAST_PRECIPITATION: 1,
                    },
                ]
            }
        },
    )

    await default_sensor.async_update()
    assert default_sensor.is_on is False

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        ATTR_CONDITION_SUNNY,
        attributes={
            ATTR_WEATHER_TEMPERATURE: 12,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_DAILY,
        },
    )
    async_mock_service(
        hass,
        WEATHER_DOMAIN,
        SERVICE_GET_FORECASTS,
        response={
            MOCK_WEATHER_ENTITY: {
                "forecast": [
                    {
                        ATTR_FORECAST_TIME: today,
                        ATTR_FORECAST_CONDITION: ATTR_CONDITION_RAINY,
                    },
                ]
            }
        },
    )

    await default_sensor.async_update()
    assert default_sensor.is_on is False

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        ATTR_CONDITION_SUNNY,
        attributes={
            ATTR_WEATHER_TEMPERATURE: 12,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_DAILY,
        },
    )
    async_mock_service(
        hass,
        WEATHER_DOMAIN,
        SERVICE_GET_FORECASTS,
        response={
            MOCK_WEATHER_ENTITY: {
                "forecast": [
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
                ]
            }
        },
    )

    await default_sensor.async_update()
    assert default_sensor.is_on is False

    hass.states.async_set(
        MOCK_WEATHER_ENTITY,
        ATTR_CONDITION_SUNNY,
        attributes={
            ATTR_WEATHER_TEMPERATURE: -1,
            ATTR_SUPPORTED_FEATURES: WeatherEntityFeature.FORECAST_DAILY,
        },
    )
    async_mock_service(
        hass,
        WEATHER_DOMAIN,
        SERVICE_GET_FORECASTS,
        response={
            MOCK_WEATHER_ENTITY: {
                "forecast": [
                    {
                        ATTR_FORECAST_TIME: today,
                    },
                    {
                        ATTR_FORECAST_TIME: int(today_ts + day),
                        ATTR_FORECAST_TEMP: 1,
                    },
                ]
            }
        },
    )

    await default_sensor.async_update()
    assert default_sensor.is_on is False
