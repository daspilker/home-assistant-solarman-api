"""Constants for the Solarman integration."""

import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import os
from datetime import timedelta
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import EntityCategory
from homeassistant.util.yaml import load_yaml
from typing import Final

LOGGER = logging.getLogger(__package__)

DOMAIN = "solarman_api"

CONF_APP_ID: Final = "app_id"
CONF_APP_SECRET: Final = "app_secret"  # noqa: S105
CONF_DEVICE_SERIAL_NUMBER: Final = "device_serial_number"
CONF_PROFILE: Final = "profile"

ATTRIBUTION = "Data provided by Solarman API"
MANUFACTURER: Final = "Solarman"

DEFAULT_SCAN_INTERVAL = timedelta(minutes=2)

# Schema for a single sensor entry in our profile YAML
SENSOR_ENTRY_SCHEMA = vol.Schema({
    vol.Required("key"): cv.string,
    vol.Required("name"): cv.string,
    # Validates against HA's allowed device classes (voltage, energy, etc.)
    vol.Optional("device_class"): vol.Coerce(SensorDeviceClass),
    # Validates against allowed state classes (measurement, total, etc.)
    vol.Optional("state_class"): vol.Coerce(SensorStateClass),
    vol.Optional("native_unit_of_measurement"): cv.string,
    vol.Optional("suggested_display_precision"): cv.positive_int,
    vol.Optional("icon"): cv.icon,
    vol.Optional("datetime_format"): cv.string,
    vol.Optional("entity_category"): vol.Coerce(EntityCategory),
    vol.Optional("entity_registry_enabled_default", default=True): cv.boolean,
})

# The overall structure of our profile file
PROFILE_SCHEMA = vol.Schema({
    vol.Required("sensors"): vol.All(cv.ensure_list, [SENSOR_ENTRY_SCHEMA]),
})

def get_profile_list(hass):
    """Scan the profiles directory for .yaml files."""
    path = os.path.join(os.path.dirname(__file__), "profiles")
    if not os.path.exists(path):
        LOGGER.debug(f"{path} not found.")
        return []

    # Return filenames without the .yaml extension
    return [f[:-5] for f in os.listdir(path) if f.endswith(".yaml")]

def load_profile(hass, profile_name):
    """Load a specific profile from the profiles directory."""
    path = os.path.join(os.path.dirname(__file__), "profiles", f"{profile_name}.yaml")
    if not os.path.isfile(path):
        LOGGER.debug(f"File {path} not found.")
        return None

    try:
        content = load_yaml(path)
        return PROFILE_SCHEMA(content) # Validates against our schema
    except Exception as e:
        LOGGER.debug(f"Exception occurred: {e}")
        return None
