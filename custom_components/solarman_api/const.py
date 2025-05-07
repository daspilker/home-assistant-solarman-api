"""Constants for the Solarman integration."""

from datetime import timedelta
import logging
from typing import Final

LOGGER = logging.getLogger(__package__)

DOMAIN = "solarman_api"

CONF_APP_ID: Final = "app_id"
CONF_APP_SECRET: Final = "app_secret"
CONF_DEVICE_SERIAL_NUMBER: Final = "device_serial_number"

ATTRIBUTION = "Data provided by Solarman API"
MANUFACTURER: Final = "Solarman"

DEFAULT_SCAN_INTERVAL = timedelta(minutes=5)
