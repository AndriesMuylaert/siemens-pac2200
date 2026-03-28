"""DataUpdateCoordinator for Siemens PAC2200."""
from __future__ import annotations

import asyncio
import logging
import struct
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SENSOR_DEFINITIONS

_LOGGER = logging.getLogger(__name__)


def _decode_float32(registers: list[int]) -> float:
    """Convert two 16-bit Modbus registers to a float32 value."""
    raw = struct.pack(">HH", registers[0], registers[1])
    return struct.unpack(">f", raw)[0]


def _slave_kwarg(slave: int) -> dict:
    """Return the correct keyword argument for the installed pymodbus version.

    pymodbus <3.12 uses slave=, pymodbus >=3.12 renamed it to device_id=.
    We detect by inspecting the actual method signature at runtime.
    """
    import inspect
    from pymodbus.client.mixin import ModbusClientMixin

    sig = inspect.signature(ModbusClientMixin.read_holding_registers)
    if "slave" in sig.parameters:
        return {"slave": slave}
    if "device_id" in sig.parameters:
        return {"device_id": slave}
    # Fallback: pass as positional (first arg after address is slave/unit)
    _LOGGER.warning("Cannot detect pymodbus slave parameter name; trying slave=")
    return {"slave": slave}


class PAC2200Coordinator(DataUpdateCoordinator):
    """Polls all PAC2200 registers and caches the decoded values."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        slave: int,
        delay: int,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self._host = host
        self._port = port
        self._slave = slave
        self._delay = delay
        self._client = None
        self._slave_kwargs: dict | None = None

    async def _get_client(self):
        """Return a connected Modbus client, creating one if needed."""
        from pymodbus import FramerType
        from pymodbus.client import AsyncModbusTcpClient

        if self._client is None or not self._client.connected:
            self._client = AsyncModbusTcpClient(
                host=self._host,
                port=self._port,
                framer=FramerType.SOCKET,
                timeout=5,
            )
            await self._client.connect()
            if self._delay > 0:
                await asyncio.sleep(self._delay)

        if self._slave_kwargs is None:
            self._slave_kwargs = _slave_kwarg(self._slave)
            _LOGGER.debug("pymodbus slave kwarg resolved to: %s", self._slave_kwargs)

        return self._client

    async def _async_update_data(self) -> dict[str, float | None]:
        """Read all sensor registers."""
        try:
            client = await self._get_client()
        except Exception as exc:
            raise UpdateFailed(f"Connection to PAC2200 failed: {exc}") from exc

        data: dict[str, float | None] = {}

        for _name, uid, address, *_ in SENSOR_DEFINITIONS:
            try:
                result = await client.read_holding_registers(
                    address=address, count=2, **self._slave_kwargs
                )
                if result.isError():
                    _LOGGER.warning("Error reading register %s: %s", address, result)
                    data[uid] = None
                else:
                    data[uid] = _decode_float32(result.registers)
            except Exception as exc:
                _LOGGER.warning("Exception reading register %s: %s", address, exc)
                data[uid] = None

        return data
