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
            False: 0,
            True: 1
        }
        self.autofade_mapping = {
            False: 0,
            True: 1
        }
        #speed is a number value: 1, 2, 3, 4, 5

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

    async def async_get_power(self):
        pin_value = await self.async_get_pin_value('V0')
        key = {i for i in self.power_mapping if self.power_mapping[i]==pin_value}.pop()
        return key

    async def async_set_autofade(self, value):
        pin_value = self.autofade_mapping.get(value)
        await self.async_set_pin_value('V1', pin_value)

    async def async_get_autofade(self):
        pin_value = await self.async_get_pin_value('V1')
        key = {i for i in self.autofade_mapping if self.autofade_mapping[i]==pin_value}.pop()
        return key

    async def async_set_speed(self, value):
        await self.async_set_pin_value('V2', value)

    async def async_get_speed(self):
        pin_value = await self.async_get_pin_value('V2')
        return pin_value
