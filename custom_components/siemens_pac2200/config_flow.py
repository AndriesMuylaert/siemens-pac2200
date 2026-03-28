"""Config flow for Siemens PAC2200 integration."""
from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import (
    CONF_DELAY,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE,
    DEFAULT_DELAY,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SLAVE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


def _build_schema(defaults: dict) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_HOST, default=defaults.get(CONF_HOST, "")): TextSelector(
                TextSelectorConfig(type=TextSelectorType.TEXT)
            ),
            vol.Required(
                CONF_PORT, default=defaults.get(CONF_PORT, DEFAULT_PORT)
            ): NumberSelector(
                NumberSelectorConfig(min=1, max=65535, step=1, mode=NumberSelectorMode.BOX)
            ),
            vol.Required(
                CONF_SLAVE, default=defaults.get(CONF_SLAVE, DEFAULT_SLAVE)
            ): NumberSelector(
                NumberSelectorConfig(min=1, max=247, step=1, mode=NumberSelectorMode.BOX)
            ),
            vol.Required(
                CONF_DELAY, default=defaults.get(CONF_DELAY, DEFAULT_DELAY)
            ): NumberSelector(
                NumberSelectorConfig(min=0, max=30, step=1, mode=NumberSelectorMode.BOX)
            ),
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=defaults.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            ): NumberSelector(
                NumberSelectorConfig(min=5, max=3600, step=1, mode=NumberSelectorMode.BOX)
            ),
        }
    )


def _build_options_schema(defaults: dict) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(
                CONF_DELAY, default=defaults.get(CONF_DELAY, DEFAULT_DELAY)
            ): NumberSelector(
                NumberSelectorConfig(min=0, max=30, step=1, mode=NumberSelectorMode.BOX)
            ),
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=defaults.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            ): NumberSelector(
                NumberSelectorConfig(min=5, max=3600, step=1, mode=NumberSelectorMode.BOX)
            ),
        }
    )


async def _async_try_connect(host: str, port: int) -> str | None:
    """Test that a TCP connection can be opened. Returns error key or None."""
    import asyncio
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=5,
        )
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return None
    except Exception as exc:
        _LOGGER.debug("PAC2200 TCP connection test failed: %s", exc)
        return "cannot_connect"


class PAC2200ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Siemens PAC2200."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = str(user_input[CONF_HOST]).strip()
            port = int(user_input[CONF_PORT])
            slave = int(user_input[CONF_SLAVE])
            delay = int(user_input[CONF_DELAY])
            scan_interval = int(user_input[CONF_SCAN_INTERVAL])

            await self.async_set_unique_id(f"{host}:{port}:{slave}")
            self._abort_if_unique_id_configured()

            error = await _async_try_connect(host, port)
            if error:
                errors["base"] = error
            else:
                return self.async_create_entry(
                    title=f"PAC2200 @ {host}",
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        CONF_SLAVE: slave,
                        CONF_DELAY: delay,
                        CONF_SCAN_INTERVAL: scan_interval,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema(user_input or {}),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> PAC2200OptionsFlow:
        return PAC2200OptionsFlow()


class PAC2200OptionsFlow(config_entries.OptionsFlow):
    """Handle options for Siemens PAC2200."""

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    CONF_DELAY: int(user_input[CONF_DELAY]),
                    CONF_SCAN_INTERVAL: int(user_input[CONF_SCAN_INTERVAL]),
                },
            )

        defaults = {
            CONF_DELAY: self.config_entry.options.get(
                CONF_DELAY,
                self.config_entry.data.get(CONF_DELAY, DEFAULT_DELAY),
            ),
            CONF_SCAN_INTERVAL: self.config_entry.options.get(
                CONF_SCAN_INTERVAL,
                self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            ),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=_build_options_schema(defaults),
        )
