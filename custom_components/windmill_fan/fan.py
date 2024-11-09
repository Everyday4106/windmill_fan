import logging
from homeassistant.components.fan import FanEntity, FanEntityFeature

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN
from .blynk_service import BlynkService
from .coordinator import WindmillDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class WindmillFan(FanEntity):
    """Representation of a Windmill Fan"""
    
    def __init__(self, coordinator):
        """Initialize the fan device."""
        _LOGGER.debug("yo")
        _LOGGER.debug(coordinator.data)
        self._attr_name = "Windmill Fan"

        #homeassistant.helpers.device_registry.format_mac
        #find the MAC via a "discovery handler"
        #self._attr_unique_id = "123456"
        #self._attr_unique_id = f"{DOMAIN}_{entity_description.key}"
        #self._attr_device_info = DeviceInfo(
        #    identifiers={(DOMAIN, self.unique_id)},
        #    name= "Windmill Fan",
        #    manufacturer="Windmill"
        #)
        self._attr_supported_features = (
            FanEntityFeature.SET_SPEED |
            FanEntityFeature.TURN_ON |
            FanEntityFeature.TURN_OFF
        )
        self._is_on = False
        self._speed_count = 5
        self._autofade = False
        self._speed = 1
        _LOGGER.debug(self._is_on || self._autofade || self._speed)
        
        # update values based on the Coordinator
        self._is_on = coordinator.data["power"]
        self._autofade = coordinator.data["autofade"]
        self._speed = coordinator.data["speed"]
        _LOGGER.debug(self._is_on || self._autofade || self._speed)
        
        #percentage	int | None	0	The current speed percentage. Must be a value between 0 (off) and 100.
        #_LOGGER.debug(f"Setup WindmillFan entity: {self.entity_description.name}")
