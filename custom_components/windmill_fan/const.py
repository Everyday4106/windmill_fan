"""Constants for Windmill Fan."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Windmill Fan"
DOMAIN = "windmill_fan"
VERSION = "1.0.0"
UPDATE_INTERVAL = 60
CONF_TOKEN = "token"
CONF_TITLE = "Windmill fan auth token"
BASE_URL = "https://dashboard.windmillair.com"
