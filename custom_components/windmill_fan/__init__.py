import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS, CONF_TOKEN, BASE_URL
from .blynk_service import BlynkService
from .coordinator import WindmillDataUpdateCoordinator
from .fan import WindmillFan

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up Windmill Fan config entry")

    server = BASE_URL
    token = entry.data[CONF_TOKEN]
    
    blynk_service = BlynkService(hass, server, token)
    coordinator = WindmillDataUpdateCoordinator(hass, blynk_service)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator
    
    # Fetch the current values for the fan
    #await coordinator.async_config_entry_first_refresh()

    #await blynk_service.async_set_power(1)
    
    #async_add_entities(
    #    WindmillFan(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    #)
    
    return True
