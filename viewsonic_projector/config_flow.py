import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .const import DOMAIN, CONF_HOST, CONF_NAME

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): TextSelector(TextSelectorConfig(type=TextSelectorType.TEXT)),
        vol.Optional(CONF_NAME, default="ViewSonic Projector"): TextSelector(TextSelectorConfig(type=TextSelectorType.TEXT)),
    }
)

class ViewSonicProjectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ViewSonic Projector."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(entry):
        return ViewSonicProjectorOptionsFlow(entry)

class ViewSonicProjectorOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
