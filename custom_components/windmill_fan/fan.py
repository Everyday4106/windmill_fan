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
        
