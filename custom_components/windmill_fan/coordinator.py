import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class WindmillDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Windmill API/Blynk."""

    def __init__(self, hass, blynk_service):
        _LOGGER.debug("Initialization")
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
            }
            _LOGGER.debug(f"Data fetched from Windmill: {data}")
            return data
        except Exception as err:
            _LOGGER.error(f"Error fetching data: {err}")
            raise UpdateFailed(f"Error fetching data: {err}")
