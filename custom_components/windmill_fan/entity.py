import logging

from homeassistant.components.fan import FanEntity, FanEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

class WindmillFan(CoordinatorEntity, FanEntity):
    """Representation of a Windmill Fan device."""

    def __init__(self, coordinator, entity_description: FanEntityDescription):
        """Initialize the fan device."""
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

    @property
    def unique_id(self):
        """Return a unique ID for the entity."""
        return f"{DOMAIN}_{self.entity_description.key}"

    @property
    def name(self):
        """Return the name of the entity."""
        return self.entity_description.name

    @property
    def is_on(self):
        return self.coordinator.data.get("power")

    async def async_turn_on(self):
        """Turn on the device."""
        await self.coordinator.blynk_service.async_set_power(True)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn off the device."""
        await self.coordinator.blynk_service.async_set_power(False)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()

    async def async_update(self):
        """Update the fan entity."""
        _LOGGER.debug("Executing async_update in WindmillFan")
        await super().async_update()
        self._attr_is_on = self.coordinator.data.get("power")
        _LOGGER.debug(f"Updated power state: {self._attr_is_on}")
