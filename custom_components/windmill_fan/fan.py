import logging
from homeassistant.components.fan import FanEntity, FanEntityFeature

from .const import DOMAIN
from .coordinator import WindmillDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class WindmillFan(FanEntity):
    """Representation of a Windmill Fan"""
  
      def __init__(self, coordinator):
        """Initialize the fan device."""
        _LOGGER.debug("yo")
        
