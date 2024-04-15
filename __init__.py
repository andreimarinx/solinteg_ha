import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
       hass.data.setdefault(DOMAIN, {})
       # ...
       await hass.async_add_executor_job(
           async_setup_entry, hass, config_entry, async_add_entities
       )
       return True
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # ... (Add unload logic if needed)
    return True
