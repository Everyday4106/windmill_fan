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
        
        self.power_mapping = {
            False: 0,
            True: 1
        }
        self.autofade_mapping = {
            False: 0,
            True: 1
        }
        self.speed_mapping = {
            "Speed 1": 1,
            "Speed 2": 2,
            "Speed 3": 3,
            "Speed 4": 4,
            "Speed 5": 5,
        }

    def _get_request_url(self, endpoint, params):
        query = urlencode(params)
        return f"{self.server}/{endpoint}?{query}"

    async def async_get_pin_value(self, pin):
        _LOGGER.debug(f"Getting value for pin {pin}")
        params = {'token': self.token}
        url = self._get_request_url(f'external/api/get', params) + f"&{pin}"
        _LOGGER.debug(f"Request URL: {url}")

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
                raise Exception(f"Failed to get value for pin {pin}")

        return await self.hass.async_add_executor_job(fetch)

    async def async_set_pin_value(self, pin, value):
        _LOGGER.debug(f"Setting pin {pin} to {value}")
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
                raise Exception(f"Failed to set value for pin {pin}")

        return await self.hass.async_add_executor_job(fetch)

    async def async_set_power(self, value):
        pin_value = self.power_mapping.get(value, "0")
        _LOGGER.debug(f"Setting Power pin to {pin_value}")
        await self.async_set_pin_value('V0', pin_value)

    async def async_get_power(self) -> bool:
        pin_value = await self.async_get_pin_value('V0')
        _LOGGER.debug(f"Power is {pin_value}")
        if pin_value == 1:
            return True
        else:
            return False

    async def async_set_autofade(self, value):
        pin_value = self.power_mapping.get(value, "0")
        _LOGGER.debug(f"Setting AutoFade to {pin_value}")
        await self.async_set_pin_value('V1', pin_value)

    async def async_get_autofade(self) -> bool:
        pin_value = await self.async_get_pin_value('V1')
        _LOGGER.debug(f"Autofade is {pin_value}")
        if pin_value == 1:
            return True
        else:
            return False

    async def async_set_speed(self, value):
        pin_value = self.speed_mapping.get(value, "0")
        _LOGGER.debug(f"Setting speed to {pin_value}")
        await self.async_set_pin_value('V2', pin_value)

    async def async_get_speed(self):
        pin_value = await self.async_get_pin_value('V2')
        key_list = list(self.speed_mapping.keys())
        val_list = list(self.speed_mapping.values())
        speed = key_list[val_list.index(pin_value)]
        
        _LOGGER.debug(f"Pin ({pin_value}) is set to {speed}")
        return speed
