from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_HOST, CONF_PORT

from pymodbus.client.sync import ModbusTcpClient  # Or ModbusSerialClient for RTU

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensors from a config entry."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]

    client = ModbusTcpClient(host, port) 
    await hass.async_add_executor_job(client.connect)

    devices = []
    devices.append(TotalPVPInputPowerSensor(client))
    async_add_devices(devices, True)


class TotalPVPInputPowerSensor(Entity):
    def __init__(self, client):
        self._client = client
        ...  # Other initialization

    def update(self):
        """Read data from the Modbus device"""
        result = self._client.read_holding_registers(11028, 2, unit=1)  
        if not result.isError():
            raw_value = result.registers[0] * 256 + result.registers[1]
            self._state = raw_value * 0.001  # Apply your scaling 
        else:
            self._state = None 