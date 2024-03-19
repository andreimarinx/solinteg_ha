from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

PREDEFINED_SENSORS = [
    {
        "name": "my_relay",
        "address": 100,
        "device_class": "door",
        "input_type": "coil",
        "scan_interval": 15,
        "slave": 1,
        "slave_count": 0,
        "unique_id": "my_relay"
    }
]

class MyModbusSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False  # Assuming your setup uses a coordinator

    def __init__(self, coordinator, name, address, input_type, slave):
        super().__init__(coordinator)
        self._name = name
        self._address = address
        self._input_type = input_type
        self._slave = slave