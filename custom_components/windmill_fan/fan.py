import logging
from homeassistant.components.fan import FanEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

class WindmillFan(FanEntity):
  _attr_has_entity_name = True
  _attr_name = None
  
  def __init__(self):
    _LOGGER.debug(f"setting up the fan entity...")
    self._is_on = False
    self._attr_device_info = DeviceInfo(
      identifiers={(DOMAIN, self.unique_id)},
      name= "Windmill Fan",
      manufacturer="Windmill"
    )
    self._attr_unique_id = f"{DOMAIN}_{entity_description.key}"
    
    @property
    def is_on(self):
      """If the fan is currently on or off."""
      return self._is_on
    
    def turn_on(self, **kwargs):
      """Turn the fan on."""
      self._is_on = True

    def turn_off(self, **kwargs):
      """Turn the fan off."""
      self._is_on = False
