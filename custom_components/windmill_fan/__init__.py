import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS, CONF_TOKEN, BASE_URL
from .blynk_service import BlynkService
from .coordinator import WindmillDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up Windmill Fan config entry")

    server = BASE_URL
    token = entry.data[CONF_TOKEN]
    
    _LOGGER.debug("**** Initializing the Blynk Service ****")
    blynk_service = BlynkService(hass, server, token)
    _LOGGER.debug("**** Starting the Coordinator ****")
    coordinator = WindmillDataUpdateCoordinator(hass, blynk_service)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator

    _LOGGER.debug("**** Calling Config Entry ****")
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.debug("**** Forwarding Config Entry to Fan setup ****")
    await hass.config_entries.async_forward_entry_setups(entry, ["fan"])

    return True
