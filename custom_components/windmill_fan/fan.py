import logging
from homeassistant.components.fan import FanEntity, FanEntityDescription

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN
from .blynk_service import BlynkService
from .coordinator import WindmillDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class WindmillFan(CoordinatorEntity, FanEntity):
    """Representation of a Windmill Fan"""
    
    def __init__(self, coordinator, entity_description: FanEntityDescription):
        """Initialize the climate device."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_name = "Windmill Fan"
        self._attr_unique_id = f"{DOMAIN}_{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name= "Windmill Fan",
            manufacturer="Windmill"
        )
        self._attr_supported_features = (
            ClimateEntityFeature.SET_SPEED |
            ClimateEntityFeature.TURN_ON |
            ClimateEntityFeature.TURN_OFF
        )
        self._is_on = False
        _LOGGER.debug(f"Setup WindmillFan entity: {self.entity_description.name}")
