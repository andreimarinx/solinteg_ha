import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import DOMAIN

class MyModbusFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Handle the data from the config form and set up the connection
            # ...
            return self.async_create_entry(title="My Modbus", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=502): int
        })
        return self.async_show_form(step_id="user", data_schema=schema)
