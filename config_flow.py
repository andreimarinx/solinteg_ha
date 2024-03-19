

from homeassistant import config_entries
from .const import DOMAIN

class ModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Validate user input and handle errors if any
            return self.async_create_entry(title="Modbus Integration", data=user_input)
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("type"): vol.In(["tcp", "udp"]),
                vol.Required("host"): str,
                vol.Required("port", default=502): int
            })
        )
