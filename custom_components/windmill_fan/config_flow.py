import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_TOKEN

class WindmillFanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Add a new fan"""
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return WindmillFanOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Windmill Fan authority token", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_TOKEN): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

class WindmillFanOptionsFlowHandler(config_entries.OptionsFlow):
    """Modify an existing fan"""
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Windmill Fan authority token", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_TOKEN, default=self.config_entry.data.get(CONF_TOKEN)): str,
        })

        return self.async_show_form(
            step_id="init", data_schema=schema, errors=errors
        )
