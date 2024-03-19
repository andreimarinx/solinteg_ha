import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.modbus.const import (
       CONF_HOST, 
       CONF_PORT,
       CONF_TYPE,
)
from homeassistant.config_entries import ConfigFlow

from pymodbus.client.sync import ModbusTcpClient

from .const import DOMAIN
from .sensor import PREDEFINED_SENSORS  

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Modbus integration from a config entry."""
    config = entry.data
    client = ModbusTcpClient(
        host=config[CONF_HOST],
        port=config[CONF_PORT],
    )

    async def async_add_entities(add_entities: AddEntitiesCallback) -> None:
        entities = []
        for sensor_config in PREDEFINED_SENSORS:
            sensor = MyModbusSensor(
                client,
                sensor_config["name"],
                sensor_config["address"],
                sensor_config.get("input_type", "coil"), 
                sensor_config.get("slave", 1)  
            )
            entities.append(sensor)
        add_entities(entities)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True