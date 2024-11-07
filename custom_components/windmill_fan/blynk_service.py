import logging
import requests
from urllib.parse import urlencode

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

class BlynkService:
    def __init__(self, hass, server, token):
        self.hass = hass
        self.server = server
        self.token = token
        # Mapping of string values to pin values
        self.power_mapping = {
            "Off": 0,
            "On": 1
        }

    def _get_request_url(self, endpoint, params):
        query = urlencode(params)
        return f"{self.server}/{endpoint}?{query}"

    async def async_get_pin_value(self, pin):
        _LOGGER.debug(f"Getting pin value for pin {pin}")
        params = {'token': self.token}
        url = self._get_request_url(f'external/api/get', params) + f"&{pin}"
        _LOGGER.debug(f"Request URL: {url}")

        def fetch():
            response = requests.get(url)
            _LOGGER.debug(f"Response Status Code: {response.status_code}")
            _LOGGER.debug(f"Response Text: {response.text}")

            if response.status_code == 200:
                _LOGGER.debug(f"Response RAW: {response}")
                try:
                    if response.text.isdigit():
                        return int(response.text)
                    elif response.text.isalpha():
                        return response.text.strip()
                    else:
                        return response.json()[0]
                except (ValueError, IndexError) as e:
                    raise Exception(f"Failed to parse response for {pin}: {e}")
            else:
                raise Exception(f"Failed to get pin value for {pin}")

        return await self.hass.async_add_executor_job(fetch)

    async def async_set_pin_value(self, pin, value):
        _LOGGER.debug(f"Setting pin value for pin {pin} to {value}")
        params = {'token': self.token, pin: value}
        url = self._get_request_url(f'external/api/update', params)
        _LOGGER.debug(f"Request URL: {url}")

        def fetch():
            response = requests.get(url)
            _LOGGER.debug(f"Response Status Code: {response.status_code}")
            _LOGGER.debug(f"Response Text: {response.text}")

            if response.status_code == 200:
                return response.text.strip()
            else:
                raise Exception(f"Failed to set pin value for {pin}")

        return await self.hass.async_add_executor_job(fetch)

    async def async_set_power(self, value):
        pin_value = self.power_mapping.get(value, "0")
        await self.async_set_pin_value('V0', pin_value)

    async def async_get_power(self):
        pin_value = await self.async_get_pin_value('V0')
        _LOGGER.debug(f"Pin value received for power: {pin_value}")
        _LOGGER.debug(self.power_mapping.keys())
        _LOGGER.debug(self.power_mapping.values())
        if pin_value == 1:
            return "On"
        else:
            return "Off"
