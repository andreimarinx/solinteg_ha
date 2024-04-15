"""Support for Modbus sensors."""
from pymodbus.client import ModbusTcpClient
from homeassistant.helpers.entity import Entity
DOMAIN = "solinteg_ha"
import logging


_LOGGER = logging.getLogger(__name__)

async def async_setup_sensors(hass):
    """Set up Modbus sensors."""
    modbus_ip = hass.data[DOMAIN]["modbus_ip"]
    modbus_port = hass.data[DOMAIN]["modbus_port"]

    # Connect to Modbus device
    client = ModbusTcpClient(modbus_ip, port=modbus_port)
    client.connect()

    # Define sensor entities
    sensors = [
        {
            "name": "Total PV Input Power",
            "address": 11028,
            "unit_of_measurement": "kW",
            "scale": 0.001,
            "slave_id": 247
        },
        # Add more sensor definitions here if needed
    ]

    for sensor in sensors:
        sensor_name = sensor["name"]
        address = sensor["address"]
        unit_of_measurement = sensor["unit_of_measurement"]
        scale = sensor["scale"]
        slave_id = sensor["slave_id"]

        # Read sensor value from Modbus device
        result = client.read_holding_registers(11028, 2, slave=247)
        if result.isError():
            _LOGGER.error("Error reading sensor %s: %s", sensor_name, result)
            _LOGGER.error("Error reading sensor %s: %s", modbus_ip, modbus_port)
            continue

        # Calculate sensor value
        raw_value = result.registers[0]
        scaled_value = raw_value * scale

        # Create Home Assistant sensor entity
        hass.states.async_set(
            f"sensor.{sensor_name.lower().replace(' ', '_')}",
            scaled_value,
            {
                "friendly_name": sensor_name,
                "unit_of_measurement": unit_of_measurement,
                "icon": "mdi:solar-power",
            },
        )

    # Disconnect from Modbus device
    client.close()
