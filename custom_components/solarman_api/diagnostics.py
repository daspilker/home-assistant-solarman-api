"""Diagnostics support for Solarman."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant

from .const import CONF_APP_SECRET
from .coordinator import SolarmanConfigEntry, SolarmanData

TO_REDACT = {CONF_EMAIL, CONF_PASSWORD, CONF_APP_SECRET}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: SolarmanConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    solarman_data: SolarmanData = config_entry.runtime_data

    return {
        "entry_data": async_redact_data(dict(config_entry.data), TO_REDACT),
        "data": solarman_data.coordinator.data,
    }
