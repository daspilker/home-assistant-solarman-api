"""Sensors for data from Solarman API ."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    PERCENTAGE
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .coordinator import SolarmanConfigEntry, SolarmanCoordinator

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="Et_ge0",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="total_production",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="Et_ge1",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="total_production_1",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="Et_ge2",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="total_production_2",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="Etdy_ge0",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="daily_production",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="Etdy_ge1",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="daily_production_1",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="Etdy_ge2",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="daily_production_2",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="AC1",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="ac_current",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="AF1",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="ac_output_frequency",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="APo_t1",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="ac_output_power",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="AV1",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="ac_voltage",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="DC1",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="dc_current_pv1",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="DP1",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="dc_power_pv1",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="DV1",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="dc_voltage_pv1",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="DC2",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="dc_current_pv2",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="DP2",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="dc_power_pv2",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="DV2",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="dc_voltage_pv2",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="AC_RDT_T1",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        translation_key="radiator_temp",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="DPi_t1",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="total_dc_input_power",
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="B_left_cap1",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        translation_key="battery_state_of_charge",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="S_P_TO",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="total_smartload_power",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="C_CAP",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        translation_key="bms_soc",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="BMS_B_V1",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        translation_key="bms_voltage",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="BMS_B_C1",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        translation_key="bms_current",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="B_V1",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        translation_key="battery_voltage",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="B_C1",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        translation_key="battery_current",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="B_P1",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="battery_power",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="PG_Pt1",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="total_grid_power",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="G_V_LN",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        translation_key="grid_voltage_l1l2",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="G_C_LN",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        translation_key="grid_current_l1l2",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="I_O_P_LN",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="inverter_output_power_l1l2",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="PV_D_P_G",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="pv_daily_power_generation",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="DP1",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="dc_power_pv1",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="DP2",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="dc_power_pv1",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="DP3",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        translation_key="dc_power_pv3",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="DC1",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        translation_key="dc_current_pv1",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="DC2",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        translation_key="dc_current_pv2",
        suggested_display_precision=1,
    ),
	SensorEntityDescription(
        key="DC3",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        translation_key="dc_current_pv3",
        suggested_display_precision=1,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SolarmanConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add Solarman entities from a config_entry."""
    coordinator: SolarmanCoordinator = entry.runtime_data.coordinator

    sensors: list[SolarmanSensor] = [
        SolarmanSensor(coordinator, description) for description in SENSOR_TYPES
    ]

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
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self.entity_description = description
        self._sensor_data = self._get_sensor_data(coordinator.data, description.key)
        self._attr_unique_id = (
            f"{coordinator.device_serial_number}-{description.key}".lower()
        )
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> str | int | float | None:
        """Return the state."""
        if self._sensor_data is None:
            return None
        return float(self._sensor_data["value"])

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._sensor_data = self._get_sensor_data(
            self.coordinator.data, self.entity_description.key
        )
        self.async_write_ha_state()

    @staticmethod
    def _get_sensor_data(
        sensors: dict[str, Any],
        key: str,
    ) -> dict[str, Any] | None:
        """Get sensor data."""
        datalist: list[dict[str, Any]] = sensors["dataList"]

        for data in datalist:
            if data["key"] == key:
                return data

        return None
