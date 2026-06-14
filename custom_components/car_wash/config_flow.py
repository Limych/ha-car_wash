#  Copyright (c) 2019-2021, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""Config flow for the Car Wash integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import CONF_DAYS, CONF_WEATHER, DEFAULT_DAYS, DEFAULT_NAME, DOMAIN


def _get_config_schema(config: dict[str, Any] | None = None) -> vol.Schema:
    """Return the schema for Car Wash configuration."""
    config = config or {}
    weather_field = (
        vol.Required(CONF_WEATHER, default=config[CONF_WEATHER])
        if CONF_WEATHER in config
        else vol.Required(CONF_WEATHER)
    )
    unique_id_field = (
        vol.Optional(CONF_UNIQUE_ID, default=config[CONF_UNIQUE_ID])
        if CONF_UNIQUE_ID in config
        else vol.Optional(CONF_UNIQUE_ID)
    )

    return vol.Schema(
        {
            weather_field: selector.EntitySelector(
                selector.EntitySelectorConfig(domain="weather")
            ),
            vol.Optional(
                CONF_NAME, default=config.get(CONF_NAME, DEFAULT_NAME)
            ): str,
            vol.Optional(
                CONF_DAYS, default=config.get(CONF_DAYS, DEFAULT_DAYS)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            unique_id_field: str,
        }
    )


def _normalize_config(config: dict[str, Any]) -> dict[str, Any]:
    """Return config with a stable entity unique ID."""
    data = dict(config)
    if not data.get(CONF_UNIQUE_ID):
        data[CONF_UNIQUE_ID] = f"{DOMAIN}-{data[CONF_WEATHER].split('.', 1)[1]}"
    return data


class CarWashConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Car Wash."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            weather_entity = user_input[CONF_WEATHER]
            for entry in self.hass.config_entries.async_entries(DOMAIN):
                config = {**entry.data, **entry.options}
                if config.get(CONF_WEATHER) == weather_entity:
                    return self.async_abort(reason="already_configured")

            await self.async_set_unique_id(weather_entity)
            self._abort_if_unique_id_configured()

            data = _normalize_config(user_input)
            return self.async_create_entry(
                title=data[CONF_NAME],
                data=data,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_get_config_schema(),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Create the options flow."""
        return CarWashOptionsFlowHandler(config_entry)


class CarWashOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Car Wash options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize Car Wash options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the Car Wash options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            weather_entity = user_input[CONF_WEATHER]
            for entry in self.hass.config_entries.async_entries(DOMAIN):
                if entry.entry_id == self._config_entry.entry_id:
                    continue

                config = {**entry.data, **entry.options}
                if config.get(CONF_WEATHER) == weather_entity:
                    errors[CONF_WEATHER] = "already_configured"
                    break
            else:
                return self.async_create_entry(
                    title="", data=_normalize_config(user_input)
                )

        return self.async_show_form(
            step_id="init",
            data_schema=_get_config_schema(
                {
                    **self._config_entry.data,
                    **self._config_entry.options,
                }
            ),
            errors=errors,
        )
