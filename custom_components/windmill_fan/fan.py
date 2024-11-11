import logging
from homeassistant.components.fan import FanEntity

_LOGGER = logging.getLogger(__name__)

class WindmillFan(FanEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator):
        _LOGGER.debug("yo")
        #super().__init__(coordinator)
        self._is_on = False
        #self.coordinator = coordinator
        #_LOGGER.debug(coordinator.data)

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on
