"""The Modbus Integration."""
import logging

from sensor import async_setup_sensors

_LOGGER = logging.getLogger(__name__)
DOMAIN = "solinteg_ha"

async def async_setup(hass, config):
    """Set up the Modbus integration."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass, entry):
    """Set up Modbus from a config entry."""
    # Store Modbus IP and port in hass.data
    hass.data[DOMAIN]["modbus_ip"] = entry.data["modbus_ip"]
    hass.data[DOMAIN]["modbus_port"] = entry.data["modbus_port"]

    # Set up sensors
    await async_setup_sensors(hass)

    return True
