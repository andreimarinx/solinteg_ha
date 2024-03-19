from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

PREDEFINED_SENSORS = [
    {
        "name": "My Relay",
        "address": 100,
        "input_type": "holding",
        "slave": 247,
    },
    # Add more sensor definitions here
]


class MyModbusSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False  

    def __init__(self, client, name, register_address, input_type, slave):
        super().__init__(client)  # Assuming CoordinatorEntity implementation
        self._client = client
        self._name = name
        self._register_address = register_address
        self._input_type = input_type
        self._slave = slave

    @property
    def name(self):
        return self._name

    async def async_update(self) -> None:
        if self._input_type == "holding":
            result = self.coordinator.client.read_holding_registers(self._register_address, count=1, unit=self._slave)
        else:  # Assuming 'coil'
            result = self.coordinator.client.read_coils(self._register_address, count=1, unit=self._slave)

        if not result.isError():
            self._attr_native_value = result.registers[0]  # Or result.bits[0] for coils
        else:
            _LOGGER.error("Error reading Modbus data: %s", result)