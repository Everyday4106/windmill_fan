#coordinator.py
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class WindmillDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Windmill API."""

    def __init__(self, hass, blynk_service):
        """Initialize."""
        _LOGGER.debug("2Starting data from Windmill Air Fan")
        self.blynk_service = blynk_service
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from Windmill Air Fan."""
        _LOGGER.debug("Fetching data from Windmill Air Fan")
        try:
            data = {
                "power": await self.blynk_service.async_get_power(),
                "autofade": await self.blynk_service.async_get_autofade(),
                "speed": await self.blynk_service.async_get_speed(),
            }
            _LOGGER.debug(f"Data fetched from Windmill Air Fan: {data}")
            return data
        except Exception as err:
            _LOGGER.error(f"Error fetching data: {err}")
            raise UpdateFailed(f"Error fetching data: {err}")
