"""Sensor platform for Siemens PAC2200."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_SLAVE, DOMAIN, SENSOR_DEFINITIONS
from .coordinator import PAC2200Coordinator

# Map device_class strings to HA SensorDeviceClass enum values
_DEVICE_CLASS_MAP = {
    "voltage": SensorDeviceClass.VOLTAGE,
    "current": SensorDeviceClass.CURRENT,
    "power": SensorDeviceClass.POWER,
    "apparent_power": SensorDeviceClass.APPARENT_POWER,
    "reactive_power": SensorDeviceClass.REACTIVE_POWER,
    "power_factor": SensorDeviceClass.POWER_FACTOR,
    "frequency": SensorDeviceClass.FREQUENCY,
    "energy": SensorDeviceClass.ENERGY,
}

_STATE_CLASS_MAP = {
    "measurement": SensorStateClass.MEASUREMENT,
    "total_increasing": SensorStateClass.TOTAL_INCREASING,
    "total": SensorStateClass.TOTAL,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PAC2200 sensor entities."""
    coordinator: PAC2200Coordinator = hass.data[DOMAIN][entry.entry_id]

    device_info = DeviceInfo(
        identifiers={(DOMAIN, f"{entry.data[CONF_HOST]}:{entry.data[CONF_PORT]}")},
        name=f"Siemens PAC2200 ({entry.data[CONF_HOST]})",
        manufacturer="Siemens",
        model="SENTRON PAC2200",
        configuration_url=f"http://{entry.data[CONF_HOST]}",
    )

    entities = [
        PAC2200Sensor(
            coordinator=coordinator,
            entry=entry,
            device_info=device_info,
            name=name,
            uid_suffix=uid_suffix,
            unit=unit,
            device_class=device_class,
            state_class=state_class,
        )
        for name, uid_suffix, _address, unit, device_class, state_class in SENSOR_DEFINITIONS
    ]

    async_add_entities(entities)


class PAC2200Sensor(CoordinatorEntity, SensorEntity):
    """A single PAC2200 measurement sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PAC2200Coordinator,
        entry: ConfigEntry,
        device_info: DeviceInfo,
        name: str,
        uid_suffix: str,
        unit: str | None,
        device_class: str,
        state_class: str,
    ) -> None:
        super().__init__(coordinator)
        self._uid_suffix = uid_suffix
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{uid_suffix}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = _DEVICE_CLASS_MAP.get(device_class)
        self._attr_state_class = _STATE_CLASS_MAP.get(state_class)
        self._attr_device_info = device_info
        self._attr_suggested_display_precision = 2

    @property
    def native_value(self):
        """Return the sensor reading from coordinator data."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self._uid_suffix)
        if value is None:
            return None
        # Round to 3 decimal places to avoid floating-point noise
        return round(value, 3)
