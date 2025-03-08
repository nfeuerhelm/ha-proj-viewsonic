"""ViewSonic Projector Integration."""
import logging
from homeassistant.config_entries import ConfigEntry # type: ignore
from homeassistant.core import HomeAssistant # type: ignore

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up ViewSonic Projector from a config entry."""
    
    def_data_dict = {
        "projector": None,
        "connection": None
    }
    _LOGGER.debug(f'Entry ID: {config_entry.entry_id}')
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(config_entry.entry_id, def_data_dict)

    # Ensure async_forward_entry_setup is awaited
    await hass.config_entries.async_forward_entry_setups(config_entry, ["media_player", "binary_sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    unload_ok = await hass.config_entries.async_unload_platforms(config_entry, ["media_player", "binary_sensor"])
    
    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id, None)

    return unload_ok
