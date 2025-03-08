import socket
import logging
import voluptuous as vol # type: ignore
import asyncio
import time
from datetime import timedelta
from homeassistant.components.media_player import MediaPlayerEntity # type: ignore
from homeassistant.components.media_player.const import MediaPlayerEntityFeature, MediaPlayerState # type: ignore
import homeassistant.helpers.config_validation as cv # type: ignore
from homeassistant.helpers.event import async_track_time_interval # type: ignore
from homeassistant.helpers.entity import DeviceInfo # type: ignore
from .const import DOMAIN, CMD_LIST, STATUS_LIST, CONF_HOST, CONF_NAME, SOURCE_STATES, PROJECTOR_MODELS, INTERVALS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    projector = ViewSonicProjector(hass, config_entry)
    hass.data[DOMAIN][config_entry.entry_id]["projector"] = projector
    async_add_entities([projector], True)
    async_track_time_interval(hass, 
                              projector.async_update, 
                              timedelta(seconds=INTERVALS['update'] if not config_entry.data.get("reduce traffic", False) else INTERVALS['slow_update']))

class ViewSonicProjector(MediaPlayerEntity):
    def __init__(self, hass, config_entry):
        self.hass = hass
        self._entry_id = config_entry.entry_id
        self._host = config_entry.data[CONF_HOST]
        self._name = config_entry.data.get(CONF_NAME, "ViewSonic Projector")
        self._model = config_entry.data.get("model", "unknown")
        self._attr_unique_id = f"viewsonic_{self._host.replace('.', '_')}"
        self._attr_state = MediaPlayerState.STANDBY
        self._attr_volume_level = None
        self._attr_is_volume_muted = None
        self._attr_source = None
        self._attr_source_list = PROJECTOR_MODELS[self._model]
    
        self._max_vol = 20
        self._connection_est = None
        self._timeouts = 0
        self._max_timeouts = 5

        self._state_change = None
        self._state_change_start = None

        self._reduce_traffic = config_entry.data.get("reduce traffic", False)
        self._round_robin = 0

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def supported_features(self):
        return (
            MediaPlayerEntityFeature.TURN_ON |
            MediaPlayerEntityFeature.TURN_OFF |
            MediaPlayerEntityFeature.VOLUME_SET |
            MediaPlayerEntityFeature.SELECT_SOURCE |
            MediaPlayerEntityFeature.VOLUME_MUTE
        )

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=self._name,
            manufacturer="ViewSonic",
            model=self._model,  # Uses the selected model from config_flow
            connections={(DOMAIN, self._host)},
        )
    
    @property
    def icon(self):
        """Return a custom icon based on power state."""
        if self._attr_state == MediaPlayerState.ON:
            return "mdi:projector"  # Custom icon when ON
        return "mdi:projector-off"  # Custom icon when OFF
    
    @property
    def is_connected(self):
        """Returns true if socket connection is active"""
        return self._sock is not None and self._connection_est is not None

    @property
    def round_robin(self) -> int:
        _max = 2

        rtn = self._round_robin

        self._round_robin += 1
        if self._round_robin > _max:
            self._round_robin = 0

        return rtn

    async def async_turn_on(self):
        await self._send_command(CMD_LIST['pwr_on'])
        self._attr_state = MediaPlayerState.ON
        self._state_change = 'on'
        self._state_change_start = time.time()
    
    async def async_turn_off(self):
        await self._send_command(CMD_LIST['pwr_off'])
        self._attr_state = MediaPlayerState.OFF
        self._state_change = 'off'
        self._state_change_start = time.time()
    
    async def async_set_volume_level(self, volume: float):
        """Volume level of the media player (0..1)."""
        # convert volume to command level
        cmd_vol = int(volume) * self._max_vol
        cmd_string = CMD_LIST['vol_set'] + bytes([cmd_vol, cmd_vol + 137])
        await self._send_command(cmd_string)
        self._attr_volume_level = volume

    async def async_mute_volume(self, mute: bool):
        await self._send_command(CMD_LIST['mute_on' if mute else 'mute_off'])
        self._attr_is_volume_muted = mute
    
    async def async_select_source(self, source: str):
        await self._send_command(CMD_LIST[f'src_{source}'])
        self._attr_source = source
    
    async def async_update(self, now=None):
        """Poll the projector for updates."""

        # Get the power state
        await self.async_update_power()

        # if the projector is on, wait 2 seconds then do one of three state checks
        if self._attr_state == MediaPlayerState.ON:
            if self._reduce_traffic:
                await asyncio.sleep(INTERVALS['slow_command'])
                match self.round_robin:
                    case 0:
                        await self.async_update_volume()
                    case 1:
                        await self.async_update_mute()
                    case 2:
                        await self.async_update_source()
            else:
                await asyncio.sleep(INTERVALS['command'])
                await self.async_update_volume()
                await asyncio.sleep(INTERVALS['command'])
                await self.async_update_mute()
                await asyncio.sleep(INTERVALS['command'])
                await self.async_update_source()
        
        # update connection binary sensor
        if self.hass and self.hass.data[DOMAIN][self._entry_id]["connection"] is not None:
            await self.hass.data[DOMAIN][self._entry_id]["connection"].async_update()

    async def async_update_source(self):
        source_status = await self._send_command(CMD_LIST['src?'])  # Query projector source status
        if source_status:
            try:
                self._attr_source = SOURCE_STATES[source_status[7]]
            except IndexError:
                if self._process_response(source_status):
                    self._attr_source = None
                else:
                    _LOGGER.warning(f'Source status not found in response. Response: {self._bytes_to_readable_string(source_status)}')
            except KeyError:
                _LOGGER.warning(f'Source status not matched. Status: {self._bytes_to_readable_string(source_status)}')

    async def async_update_mute(self):
        mute_status = await self._send_command(CMD_LIST['mute?'])  # Query projector mute status
        if mute_status:
            mute_output = self._process_response(mute_status)
            if mute_output:
                match mute_output:
                    case 'off':
                        self._attr_is_volume_muted = False
                    case 'on':
                        self._attr_is_volume_muted = True
            else:
                _LOGGER.warning(f'Unknown mute status. Response: {self._bytes_to_readable_string(mute_status)}')

    async def async_update_volume(self):
        vol_status = await self._send_command(CMD_LIST['volume?'])  # Query projector volume status
        if vol_status:
            try:
                vol_status = vol_status[7]
                self._attr_volume_level = vol_status / self._max_vol
            except IndexError:
                if self._process_response(vol_status):
                    self._attr_volume_level = None
                else:
                    _LOGGER.warning(f'Volume status not found in response. Response: {self._bytes_to_readable_string(vol_status)}')

    async def async_update_power(self):
        pwr_status = await self._send_command(CMD_LIST['pwr?'])  # Query projector power status
        if pwr_status:
            pwr_output = self._process_response(pwr_status)
            if pwr_output:
                match pwr_output:
                    case 'off':
                        if not (self._state_change == 'on' and (time.time() - self._state_change_start) < 60.0):
                            self._attr_state = MediaPlayerState.OFF
                            self._state_change = None
                            self._state_change_start = None
                    case 'on':
                        if not (self._state_change == 'off' and (time.time() - self._state_change_start) < 60.0):
                            self._attr_state = MediaPlayerState.ON
                            self._state_change = None
                            self._state_change_start = None

    async def _connect(self):
        """Ensure a persistent connection to the projector."""
        if not hasattr(self, "_sock") or self._sock is None:
            try:
                self._sock = socket.create_connection((self._host, 4661), timeout=INTERVALS["timeout"])
                self._connection_est = time.time()
            except Exception as e:
                _LOGGER.error(f'Failed to connect to projector: {e}')
                self._sock = None
                self._connection_est = None
        else:
            _LOGGER.info(f'Socket already open - {self._connection_est}')
    
    async def _send_command(self, command):
        """Send a command using the persistent connection."""
        await self._connect()  # Ensure the connection exists
        if not self._sock:
            return None

        try:
            self._sock.sendall(command)
            response = self._sock.recv(1024)
            self._timeouts = 0
            return response
        except Exception as e:
            if str(e) == 'timed out':
                _LOGGER.warning(f'Command ({self._bytes_to_readable_string(command)}) timed out')
                self._timeouts += 1
                if self._timeouts > self._max_timeouts:
                    _LOGGER.error(f'Maximum Timeouts Encounters. Reestablish connection.')
                    self._sock = None  # Mark connection as lost
                    self._connection_est = None
            else:
                _LOGGER.error(f'Socket error on command ({self._bytes_to_readable_string(command)}): {e}')
                self._sock = None  # Mark connection as lost
                self._connection_est = None
            
            return None

    def _process_response(self, response):
        return STATUS_LIST.get(response, False)
    
    def _bytes_to_readable_string(self, bytes):
        if bytes is not None:
            return ' '.join([ format(d, '#04x') for d in bytes ])
        else:
            return ''

    async def async_will_remove_from_hass(self):
        """Close the persistent connection when removing the entity."""
        if hasattr(self, "_sock") and self._sock:
            self._sock.close()
            self._sock = None
            self._connection_est = None

