"""Config flow for the solarman integration."""

from __future__ import annotations

from asyncio import timeout
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_EMAIL, CONF_NAME, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    InvalidApplicationIdError,
    InvalidApplicationSecretError,
    InvalidDeviceSerialNumberError,
    SolarmanApiClient,
    SolarmanError,
)
from .const import CONF_APP_ID, CONF_APP_SECRET, CONF_DEVICE_SERIAL_NUMBER, DOMAIN


class SolarmanFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Solarman."""

    VERSION = 1

    device_serial_number: str

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            async with timeout(10):
                client = SolarmanApiClient(
                    session,
                    user_input[CONF_EMAIL],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_APP_ID],
                    user_input[CONF_APP_SECRET],
                )
                try:
                    await client.get_data(user_input[CONF_DEVICE_SERIAL_NUMBER])
                except InvalidApplicationIdError as error:
                    errors[CONF_APP_ID] = error.status
                except InvalidApplicationSecretError as error:
                    errors[CONF_APP_SECRET] = error.status
                except InvalidDeviceSerialNumberError as error:
                    errors[CONF_DEVICE_SERIAL_NUMBER] = error.status
                except SolarmanError as error:
                    errors["base"] = error.status
                else:
                    await self.async_set_unique_id(
                        str(user_input[CONF_DEVICE_SERIAL_NUMBER])
                    )
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=user_input[CONF_NAME], data=user_input
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default="Solarman API"): str,
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_APP_ID): str,
                    vol.Required(CONF_APP_SECRET): str,
                    vol.Required(CONF_DEVICE_SERIAL_NUMBER): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Perform reauthentication upon an API authentication error."""
        self.device_serial_number = entry_data[CONF_DEVICE_SERIAL_NUMBER]
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauthentication dialog."""
        errors: dict[str, str] = {}
        if user_input:
            session = async_get_clientsession(self.hass)
            async with timeout(10):
                client = SolarmanApiClient(
                    session,
                    user_input[CONF_EMAIL],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_APP_ID],
                    user_input[CONF_APP_SECRET],
                )
                try:
                    await client.get_data(self.device_serial_number)
                except InvalidApplicationIdError as error:
                    errors[CONF_APP_ID] = error.status
                except InvalidApplicationSecretError as error:
                    errors[CONF_APP_SECRET] = error.status
                except SolarmanError as error:
                    errors["base"] = error.status
                else:
                    return self.async_update_reload_and_abort(
                        self._get_reauth_entry(),
                        data_updates={
                            CONF_EMAIL: user_input[CONF_EMAIL],
                            CONF_PASSWORD: user_input[CONF_PASSWORD],
                            CONF_APP_ID: user_input[CONF_APP_ID],
                            CONF_APP_SECRET: user_input[CONF_APP_SECRET],
                        },
                    )
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_APP_ID): str,
                    vol.Required(CONF_APP_SECRET): str,
                }
            ),
            errors=errors,
        )
