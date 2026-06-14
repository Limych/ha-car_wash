"""Tests for the Car Wash config flow."""

from typing import Final

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.car_wash.const import CONF_DAYS, CONF_WEATHER, DOMAIN

MOCK_NAME: Final = "test_name"
MOCK_UNIQUE_ID: Final = "test_id"
MOCK_WEATHER_ENTITY: Final = "weather.test"
MOCK_DAYS: Final = 2

MOCK_CONFIG: Final = {
    CONF_NAME: MOCK_NAME,
    CONF_UNIQUE_ID: MOCK_UNIQUE_ID,
    CONF_WEATHER: MOCK_WEATHER_ENTITY,
    CONF_DAYS: MOCK_DAYS,
}


async def test_config_flow(hass: HomeAssistant):
    """Test the config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == config_entries.FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    assert result["type"] == config_entries.FlowResultType.CREATE_ENTRY
    assert result["title"] == MOCK_NAME
    assert result["data"] == MOCK_CONFIG


async def test_config_flow_duplicate_weather_entity(hass: HomeAssistant):
    """Test duplicate weather entity entries are rejected."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=MOCK_NAME,
        data=MOCK_CONFIG,
        source=config_entries.SOURCE_USER,
        unique_id=MOCK_WEATHER_ENTITY,
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data=MOCK_CONFIG,
    )

    assert result["type"] == config_entries.FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_options_flow(hass: HomeAssistant):
    """Test the options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=MOCK_NAME,
        data=MOCK_CONFIG,
        source=config_entries.SOURCE_USER,
        unique_id=MOCK_WEATHER_ENTITY,
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == config_entries.FlowResultType.FORM
    assert result["step_id"] == "init"

    options = {
        **MOCK_CONFIG,
        CONF_NAME: "updated_name",
        CONF_DAYS: 3,
    }
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input=options
    )

    assert result["type"] == config_entries.FlowResultType.CREATE_ENTRY
    assert result["data"] == options


async def test_options_flow_duplicate_weather_entity(hass: HomeAssistant):
    """Test the options flow rejects duplicate weather entities."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=MOCK_NAME,
        data=MOCK_CONFIG,
        source=config_entries.SOURCE_USER,
        unique_id=MOCK_WEATHER_ENTITY,
    )
    entry.add_to_hass(hass)

    duplicate_weather = "weather.duplicate"
    duplicate_entry = MockConfigEntry(
        domain=DOMAIN,
        title="duplicate",
        data={
            **MOCK_CONFIG,
            CONF_WEATHER: duplicate_weather,
            CONF_UNIQUE_ID: "duplicate_id",
        },
        source=config_entries.SOURCE_USER,
        unique_id=duplicate_weather,
    )
    duplicate_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            **MOCK_CONFIG,
            CONF_WEATHER: duplicate_weather,
        },
    )

    assert result["type"] == config_entries.FlowResultType.FORM
    assert result["errors"] == {CONF_WEATHER: "already_configured"}
