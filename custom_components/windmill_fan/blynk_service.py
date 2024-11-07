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
        self.autofade_mapping = {
            "Disabled": 0,
            "Enabled": 1
        }
        self.speed_mapping = {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5
        }

    def return_key_from_value(dict, val):
        return list(dict.keys())[list(my_dict.values()).val])
    
    def _get_request_url(self, endpoint, params):
        query = urlencode(params)
        return f"{self.server}/{endpoint}?{query}"

    async def async_get_pin_value(self, pin):
        params = {'token': self.token}
        url = self._get_request_url(f'external/api/get', params) + f"&{pin}"

        def fetch():
            response = requests.get(url)

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
        params = {'token': self.token, pin: value}
        url = self._get_request_url(f'external/api/update', params)

        def fetch():
            response = requests.get(url)

            if response.status_code == 200:
                return response.text.strip()
            else:
                raise Exception(f"Failed to set pin value for {pin}")

        return await self.hass.async_add_executor_job(fetch)

    async def async_set_power(self, key):
        pin_value = self.power_mapping.get(key)
        _LOGGER.debug(f"Setting Power: {pin_value}")
        await self.async_set_pin_value('V0', pin_value)

    async def async_set_autofade(self, key):
        pin_value = self.autofade_mapping.get(key)
        _LOGGER.debug(f"Setting Autofade: {pin_value}")
        await self.async_set_pin_value('V1', pin_value)

    async def async_set_speed(self, key):
        pin_value = self.speed_mapping.get(key)
        _LOGGER.debug(f"Setting Speed: {pin_value}")
        await self.async_set_pin_value('V2', pin_value)

    async def async_get_power(self):
        pin_value = await self.async_get_pin_value('V0')
        _LOGGER.debug(f"Reported Power: {pin_value}")
        return return_key_from_value(self.power_mapping, pin_value)

    async def async_get_autofade(self):
        pin_value = await self.async_get_pin_value('V1')
        _LOGGER.debug(f"Reported Autofade: {pin_value}")
        return return_key_from_value(self.autofade_mapping, pin_value)

    async def async_get_speed(self):
        pin_value = await self.async_get_pin_value('V2')
        _LOGGER.debug(f"Reported Speed: {pin_value}")
        return return_key_from_value(self.speed_mapping, pin_value)

    async def async_get_mode(self):
        return 1
    
    async def async_get_fan(self):
        return 1
