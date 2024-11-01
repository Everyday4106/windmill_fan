#coordinator.py
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class WindmillDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, blynk_service):
        self.blynk_service = blynk_service
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        _LOGGER.debug("Fetching data from Windmill")
        try:
            data = {
                "power": await self.blynk_service.async_get_power(),
                "autofade": await self.blynk_service.async_get_autofade(),
                "speed": await self.blynk_service.async_get_speed(),
            }
            _LOGGER.debug(f"Data retrieved from Windmill: {data}")
            return data
        except Exception as err:
            _LOGGER.error(f"Error fetching data: {err}")
            raise UpdateFailed(f"Error fetching data: {err}")
