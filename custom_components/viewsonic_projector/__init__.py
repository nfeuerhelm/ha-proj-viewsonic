"""ViewSonic Projector Integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ViewSonic Projector from a config entry."""
    
    hass.data.setdefault(DOMAIN, {})

    # Ensure async_forward_entry_setup is awaited
    await hass.config_entries.async_forward_entry_setups(entry, ["media_player"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "media_player")
