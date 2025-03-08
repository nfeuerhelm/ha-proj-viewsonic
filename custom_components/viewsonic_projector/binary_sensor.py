from homeassistant.components.binary_sensor import BinarySensorEntity # type: ignore
from homeassistant.helpers.entity import Entity # type: ignore
from homeassistant.helpers.update_coordinator import CoordinatorEntity # type: ignore

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the binary sensor based on the media player state."""
    projector = hass.data[DOMAIN][config_entry.entry_id]["projector"]
    connection = ProjectorConnectionSensor(projector)
    hass.data[DOMAIN][config_entry.entry_id]["connection"] = connection
    async_add_entities([connection], True)

class ProjectorConnectionSensor(BinarySensorEntity):
    """Binary sensor to indicate projector connection status."""

    def __init__(self, projector):
        """Initialize the sensor."""
        self._projector = projector
        self._attr_name = f"{projector.name} Connection"
        self._attr_device_class = "connectivity"  # Shows a network connection icon
        self._attr_unique_id = f"{projector.unique_id}_connection"
        self._attr_is_on = None

    @property
    def is_on(self):
        """Return True if the projector is connected."""
        return self._attr_is_on

    async def async_update(self):
        """Manually update the connection status from the projector."""
        self._attr_is_on = self._projector.is_connected
