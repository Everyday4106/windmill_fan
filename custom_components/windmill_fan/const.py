"""Constants for Windmill Air Fan   ."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "WindmillAirFan"
DOMAIN = "windmillairfan"
VERSION = "1.0.0"
PLATFORMS = ["fan"]
UPDATE_INTERVAL = 60
CONF_TOKEN = "token"
BASE_URL = "https://dashboard.windmillair.com"