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
        self.speed_mapping = {
            "1": 1
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5
        }
        self.autofade_mapping = {
            "Disabled": 0,
            "Enabled": 1
        }
        self.power_mapping = {
            "Off": 0,
            "On": 1
        }

    def _get_request_url(self, endpoint, params):
        query = urlencode(params)
        return f"{self.server}/{endpoint}?{query}"

    async def async_get_pin_value(self, pin):
        params = {'token': self.token}
        url = self._get_request_url(f'external/api/get', params) + f"&{pin}"

        def fetch():
            response = requests.get(url)

            if response.status_code == 200:
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
        params = {'token': self.token, pin: value}
        url = self._get_request_url(f'external/api/update', params)

        def fetch():
            response = requests.get(url)

            if response.status_code == 200:
                return response.text.strip()
            else:
                raise Exception(f"Failed to set pin value for {pin}")

        return await self.hass.async_add_executor_job(fetch)

    async def async_set_power(self, value):
        pin_value = self.power_mapping.get(value)
        await self.async_set_pin_value('V0', pin_value)

    async def async_set_autofade(self, value):
        pin_value = self.autofade_mapping.get(value)
        await self.async_set_pin_value('V1', pin_value)

    async def async_set_speed(self, value):
        pin_value = self.speed_mapping.get(value)
        await self.async_set_pin_value('V2', pin_value)

    async def async_get_power(self):
        pin_value = await self.async_get_pin_value('V0')
        # getting the Key from the Value in a single line
        return list(self.power_mapping.keys())[list(self.power_mapping.values()).index(pin_value)])
    
    async def async_get_autofade(self):
        pin_value = await self.async_get_pin_value('V1')
        # getting the Key from the Value in a single line
        return list(self.autofade_mapping.keys())[list(self.autofade_mapping.values()).index(pin_value)])

    async def async_get_speed(self):
        pin_value = await self.async_get_pin_value('V2')
        # getting the Key from the Value in a single line
        return list(self.speed_mapping.keys())[list(self.speed_mapping.values()).index(pin_value)])
