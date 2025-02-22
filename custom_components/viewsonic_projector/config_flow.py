import logging
import voluptuous as vol # type: ignore
from homeassistant import config_entries # type: ignore
from homeassistant.core import callback # type: ignore
from homeassistant.helpers.selector import selector, TextSelector, TextSelectorConfig, TextSelectorType # type: ignore

from .const import DOMAIN, CONF_HOST, CONF_NAME, PROJECTOR_MODELS_LIST

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): TextSelector(TextSelectorConfig(type=TextSelectorType.TEXT)),
        vol.Required(CONF_NAME, default="ViewSonic Projector"): TextSelector(TextSelectorConfig(type=TextSelectorType.TEXT)),
        vol.Required("model", default="unknown"): selector({"select": {"options": PROJECTOR_MODELS_LIST, "mode": "dropdown"}}),
    }
)

class ViewSonicProjectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ViewSonic Projector."""

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
    """Handle options flow for ViewSonic Projector."""

    def __init__(self, entry):
        """Initialize options flow."""
        self.entry = entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional(
                    "host",
                    default=self.entry.options.get("host", self.entry.data["host"]),
                ): str,
                vol.Optional(
                    "model",
                    default=self.entry.options.get("model", self.entry.data.get("model", "unknown")),
                ): selector({"select": {"options": PROJECTOR_MODELS_LIST, "mode": "dropdown"}}),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)

