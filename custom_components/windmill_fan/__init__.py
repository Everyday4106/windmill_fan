import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS, CONF_TOKEN, BASE_URL
from .blynk_service import BlynkService
from .coordinator import WindmillDataUpdateCoordinator
from .fan import WindmillFan

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up the Windmill fan config entry")

    server = BASE_URL
    # Have the user enter the Auth Token which is needed by the API
    token = entry.data[CONF_TOKEN]

    # reference to the Windmill API via Blynk
    blynk_service = BlynkService(hass, server, token)

    # setup the coordinator to interface with the API
    coordinator = WindmillDataUpdateCoordinator(hass, blynk_service)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator

    # use the API to pull down the current values for the given Auth Token
    await coordinator.async_config_entry_first_refresh()

    # get a reference to the custom Windmill fan entity and initialize it with the values from the API
    #fan_entity = WindmillFan(coordinator)
    
    # add the Windmill Fan entity to Home Assistant
    #async_add_entities(
    #    WindmillFan(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    #)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Unloading the Windmill fan config entry")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop("coordinator")

    return unload_ok
