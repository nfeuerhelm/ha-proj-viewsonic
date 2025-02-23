from homeassistant.const import CONF_HOST, CONF_NAME # type: ignore

DOMAIN = "viewsonic_projector"

PROJECTOR_MODELS = {
    "unknown":  "Unknown ViewSonic Projector",
    "ls510w": "ViewSonic LS510W",
    "ls510wh": "ViewSonic LS510WH",
    "ls560w": "ViewSonic LS560W",
    "ls560wh": "ViewSonic LS560WH",
    "ls610hdh": "ViewSonic LS610HDH",
    "ls610wh": "ViewSonic LS610WH",
    "ls832wu": "ViewSonic LS832WU",
    "pa504w": "ViewSonic PA504W",
    "pa700s": "ViewSonic PA700S",
    "pa700w": "ViewSonic PA700W",
    "pa700x": "ViewSonic PA700X",
    "ps502w": "ViewSonic PS502W",
    "ps502x": "ViewSonic PS502X",
    "px701-4ke": "ViewSonic PX701-4KE",
    "px704hd": "ViewSonic PX704HD",
    'px728-4k': "ViewSonic PX728-4K",
    "px748-4k": "ViewSonic PX748-4K",
    "px749-4k": "ViewSonic PX749-4K",
}

PROJECTOR_MODELS_LIST = [ key for key in PROJECTOR_MODELS.keys() ]

DEFAULT_HOST = ""
DEFAULT_PORT = 4661

CONF_HOST = "host"
CONF_NAME = "name"

CMD_LIST = {
    "pwr_on":    b'\x06\x14\x00\x04\x00\x34\x11\x00\x00\x5D',
    "pwr_off":   b'\x06\x14\x00\x04\x00\x34\x11\x01\x00\x5E',
    "pwr?":      b'\x07\x14\x00\x05\x00\x34\x00\x00\x11\x00\x5E',
    "mute_on":   b'\x06\x14\x00\x04\x00\x34\x14\x00\x01\x61',
    "mute_off":  b'\x06\x14\x00\x04\x00\x34\x14\x00\x00\x60',
    "mute?":     b'\x07\x14\x00\x05\x00\x34\x00\x00\x14\x00\x61',
    "volume?":   b'\x07\x14\x00\x05\x00\x34\x00\x00\x14\x03\x64',
    "vol_set":   b'\x06\x14\x00\x04\x00\x34\x13\x2A',
    "src_HDMI1": b'\x06\x14\x00\x04\x00\x34\x13\x01\x03\x63',
    "src_HDMI2": b'\x06\x14\x00\x04\x00\x34\x13\x01\x07\x67',
    "src_USB-C": b'\x06\x14\x00\x04\x00\x34\x13\x01\x0F\x6F',
    "src?":      b'\x07\x14\x00\x05\x00\x34\x00\x00\x13\x01\x61'
}

STATUS_LIST = {
    b'\x03\x14\x00\x00\x00\x14':             'cmd_ack',
    b'\x00\x14\x00\x00\x00\x14':             'cmd_unavailable',
    b'\x05\x14\x00\x03\x00\x00\x00\x01\x18': 'on',
    b'\x05\x14\x00\x03\x00\x00\x00\x00\x17': 'off',
    b'\x05\x14\x00\x03\x00\x00\x00\x02\x19': 'pwr_warming',
    b'\x05\x14\x00\x03\x00\x00\x00\x03\x1A': 'pwr_cooling',
}
