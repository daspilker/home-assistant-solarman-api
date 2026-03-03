"""Sensors for data from Solarman API ."""

from __future__ import annotations

from typing import Any
from datetime import datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import ATTRIBUTION, load_profile, LOGGER
from .coordinator import SolarmanConfigEntry, SolarmanCoordinator

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = ()


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SolarmanConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add Solarman entities from a config_entry."""
    coordinator: SolarmanCoordinator = entry.runtime_data.coordinator

    profile_name = entry.data["profile"]
    profile_data = await hass.async_add_executor_job(load_profile, hass, profile_name)

    if profile_data is None:
        LOGGER.info(f"Unable to load the profile {profile_name}")
        return

    sensors: list[SolarmanSensor] = []
    for sensor_conf in profile_data["sensors"]:
        api_key = sensor_conf.pop("key")
        datetime_format = sensor_conf.pop("datetime_format", None)
        description = SensorEntityDescription(
            key=api_key,
            **sensor_conf
        )

        sensors.append(SolarmanSensor(coordinator, description, datetime_format=datetime_format))

    async_add_entities(sensors)


# Coordinator is used to centralize the data updates
PARALLEL_UPDATES = 0


class SolarmanSensor(CoordinatorEntity[SolarmanCoordinator], SensorEntity):
    """Define an Solarman entity."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True
    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: SolarmanCoordinator,
        description: SensorEntityDescription,
        datetime_format=None,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self.entity_description = description
        self._sensor_data = self._get_sensor_data(coordinator.data, description.key)
        self._attr_unique_id = (
            f"{coordinator.device_serial_number}-{description.key}".lower()
        )
        self._attr_device_info = coordinator.device_info
        self._datetime_format = datetime_format

    @property
    def native_value(self) -> str | int | float | datetime | None:
        """Return the state."""
        if self._sensor_data is None:
            return None
        return self._sensor_data["value"]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._sensor_data = self._get_sensor_data(
            self.coordinator.data, self.entity_description.key, self._datetime_format
        )
        self.async_write_ha_state()

    @staticmethod
    def _parse_datetime_string(value: str, datetime_format: str) -> datetime | None:
        try:
            # Parse string to naive datetime
            naive_dt = datetime.strptime(value, datetime_format)
            # Convert to HA-aware UTC datetime
            return dt_util.as_utc(naive_dt)
        except ValueError:
            return None

    @staticmethod
    def _get_sensor_data(
        sensors: dict[str, Any],
        key: str,
        datetime_format: str = None,
    ) -> dict[str, Any] | None:
        """Get sensor data."""
        datalist: list[dict[str, Any]] = sensors["dataList"]

        for data in datalist:
            if data["key"] == key:
                if datetime_format is not None:
                    LOGGER.debug(f"Key {key} will be parsed as a datetime object with {datetime_format}")
                    ha_dt = SolarmanSensor._parse_datetime_string(data["value"], datetime_format)
                    if ha_dt is not None:
                        data["value"] = ha_dt
                        return data

                    # Attempt to fix the time zone value if it's in invalid format
                    dt_str = str(data["value"])
                    parts = dt_str.split(' ')
                    offset = parts[-1]
                    if len(offset.replace('-', '').replace('+', '')) == 1:
                        parts[-1] = offset[0] + '0' + offset[1:] + '00'
                    fixed_dt_str = " ".join(parts)
                    if dt_str != fixed_dt_str:
                        ha_dt = SolarmanSensor._parse_datetime_string(fixed_dt_str, datetime_format)
                        if ha_dt is not None:
                            data["value"] = ha_dt
                            return data

                return data

        LOGGER.error(f"Key {key} not found in the API response")
        return None
