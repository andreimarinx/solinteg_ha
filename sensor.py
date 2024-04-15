import asyncio
from pymodbus.client import ModbusTcpClient
from homeassistant.helpers.entity import Entity

DOMAIN = "solinteg_ha"
import logging

_LOGGER = logging.getLogger(__name__)

async def read_modbus_sensors(client, sensors, hass):
    """Read Modbus sensors and update Home Assistant states."""
    while True:
        for sensor in sensors:
            sensor_name = sensor["name"]
            address = sensor["address"]
            unit_of_measurement = sensor["unit_of_measurement"]
            scale = sensor["scale"]
            slave_id = sensor["slave_id"]
            count = sensor["count"]

            # Read sensor value from Modbus device
            result = client.read_holding_registers(address, count, unit=slave_id)
            if result.isError():
                _LOGGER.error("Error reading sensor %s: %s", sensor_name, result)
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

        # Wait for 15 seconds before reading sensors again
        await asyncio.sleep(15)

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
            "slave_id": 247,
            "count": 2
        },
        {
            "name": "Battery SOC",
            "address": 33000,
            "unit_of_measurement": "%",
            "scale": 0.01,
            "slave_id": 247,
            "count": 1
        },
        # Add more sensor definitions here if needed
    ]

    # Start a background task to continuously read Modbus sensors
    hass.loop.create_task(read_modbus_sensors(client, sensors, hass))

    # Return True to indicate successful setup
    return True
