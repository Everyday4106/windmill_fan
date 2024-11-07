import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS, CONF_TOKEN, BASE_URL
from .blynk_service import BlynkService
from .coordinator import WindmillDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up the Windmill fan config entry")

    server = BASE_URL
    token = entry.data[CONF_TOKEN]

    blynk_service = BlynkService(hass, server, token)
    coordinator = WindmillDataUpdateCoordinator(hass, blynk_service)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Unloading the Windmill fan config entry")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop("coordinator")

    return unload_ok
