import logging
from homeassistant.components.fan import FanEntity

_LOGGER = logging.getLogger(__name__)

class WindmillFan(FanEntity):
    """Representation of a Windmill Fan"""
  
      def __init__(self):
        """Initialize the fan device."""
        _LOGGER.debug("yo")
        
