"""Siemens PAC2200 Home Assistant integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant

from .const import CONF_DELAY, CONF_SCAN_INTERVAL, CONF_SLAVE, DEFAULT_DELAY, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import PAC2200Coordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PAC2200 from a config entry."""
    scan_interval = int(entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    ))
    delay = int(entry.options.get(
        CONF_DELAY,
        entry.data.get(CONF_DELAY, DEFAULT_DELAY),
    ))

    coordinator = PAC2200Coordinator(
        hass=hass,
        host=entry.data[CONF_HOST],
        port=int(entry.data[CONF_PORT]),
        slave=int(entry.data[CONF_SLAVE]),
        delay=delay,
        scan_interval=scan_interval,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
