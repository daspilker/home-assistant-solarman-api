"""Coordinator for Solarman API."""

from asyncio import timeout
from dataclasses import dataclass
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    ApiError,
    InvalidApplicationIdError,
    InvalidApplicationSecretError,
    InvalidDeviceSerialNumberError,
    InvalidEmailOrPasswordSecretError,
    SolarmanApiClient,
)
from .const import (
    CONF_DEVICE_SERIAL_NUMBER,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    LOGGER,
    MANUFACTURER,
)

type SolarmanConfigEntry = ConfigEntry[SolarmanData]


class SolarmanCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Solarman data."""

    config_entry: ConfigEntry
    device_serial_number: int
    device_name: str

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        client: SolarmanApiClient,
    ) -> None:
        """Initialize."""

        self.client = client
        self.device_serial_number = config_entry.data[CONF_DEVICE_SERIAL_NUMBER]
        self.device_name = config_entry.data[CONF_NAME]
        self.device_info = _get_device_info(self.device_serial_number, self.device_name)

        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Solarman API."""

        try:
            async with timeout(10):
                result = await self.client.get_data(self.device_serial_number)
        except (
            InvalidApplicationIdError,
            InvalidApplicationSecretError,
            InvalidEmailOrPasswordSecretError,
            InvalidDeviceSerialNumberError,
        ) as error:
            raise ConfigEntryAuthFailed(
                translation_domain=DOMAIN,
                translation_key="auth_failed",
                translation_placeholders={
                    "device": self.device_name,
                    "error": repr(error.status),
                },
            ) from error
        except ApiError as error:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_error",
                translation_placeholders={"error": repr(error.status)},
            ) from error

        return result


@dataclass
class SolarmanData:
    """Class for handling the data retrieval."""

    coordinator: SolarmanCoordinator


def _get_device_info(device_serial_number: int, name: str) -> DeviceInfo:
    """Get device info."""
    return DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, str(device_serial_number))},
        manufacturer=MANUFACTURER,
        name=name,
        configuration_url="https://globalapi.solarmanpv.com/device/v1.0/currentData",
    )
