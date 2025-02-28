from homeassistant.const import CONF_HOST, CONF_NAME # type: ignore

DOMAIN = "viewsonic_projector"

PROJECTOR_MODELS = {
    "unknown": [
        "Component",
        "Composite",
        "DVI",
        "HDMI1",
        "HDMI2",
        "HDMI3",
        "HDMI4/MHL",
        "HDbaseT",
        "LAN/WiFi",
        "S-Video",
        "SmartSystem",
        "USB-C",
        "USB1",
        "USB2",
        "USBDisplay",
        "VGA1",
        "VGA2"
    ],
    "ls510w": [
        "HDMI1",
        "VGA1"
    ],
    "ls510wh": [
        "HDMI1",
    ],
    "ls560w": [
        "HDMI1",
        "VGA1"
    ],
    "ls560wh": [
        "HDMI1",
    ],
    "ls610hdh": [
        "HDMI1",
        "HDMI2"
    ],
    "ls610wh": [
        "HDMI1",
        "HDMI2"
    ],
    "ls832wu": [
        "HDMI1",
        "HDMI2",
        "VGA1"
    ],
    "pa504w": [
        "Composite",
        "HDMI1",
        "HDMI2",
        "VGA1",
    ],
    "pa700s": [
        "HDMI1",
        "HDMI2",
        "USB1",
        "VGA1"
    ],
    "pa700w": [
        "HDMI1",
        "HDMI2",
        "USB1",
        "VGA1"
    ],
    "pa700x": [
        "HDMI1",
        "HDMI2",
        "USB1",
        "VGA1"
    ],
    "ps502w": [
        "HDMI1",
        "HDMI2",
        "USB1",
        "VGA1"
    ],
    "ps502x": [
        "HDMI1",
        "HDMI2",
        "USB1",
        "VGA1"
    ],
    "px701-4ke": [
        "HDMI1",
        "HDMI2"
    ],
    "px704hd": [
        "HDMI1",
        "HDMI2"
    ],
    'px728-4k': [
        'HDMI1', 
        'HDMI2', 
        'USB-C',
    ],
    "px748-4k": [
        'HDMI1', 
        'HDMI2', 
        'USB-C',
    ],
    "px749-4k": [
        'HDMI1', 
        'HDMI2', 
        'USB-C',
    ],
}

PROJECTOR_MODELS_LIST = [ key for key in PROJECTOR_MODELS.keys() ]

DEFAULT_HOST = ""
DEFAULT_PORT = 4661

CONF_HOST = "host"
CONF_NAME = "name"

CMD_LIST = {
    "pwr_on":          b'\x06\x14\x00\x04\x00\x34\x11\x00\x00\x5D',
    "pwr_off":         b'\x06\x14\x00\x04\x00\x34\x11\x01\x00\x5E',
    "pwr?":            b'\x07\x14\x00\x05\x00\x34\x00\x00\x11\x00\x5E',
    "mute_on":         b'\x06\x14\x00\x04\x00\x34\x14\x00\x01\x61',
    "mute_off":        b'\x06\x14\x00\x04\x00\x34\x14\x00\x00\x60',
    "mute?":           b'\x07\x14\x00\x05\x00\x34\x00\x00\x14\x00\x61',
    "vol_set":         b'\x06\x14\x00\x04\x00\x34\x13\x2A',
    "volume?":         b'\x07\x14\x00\x05\x00\x34\x00\x00\x14\x03\x64',
    "src_VGA1":        b'\x06\x14\x00\x04\x00\x34\x13\x01\x00\x60',
    "src_VGA2":        b'\x06\x14\x00\x04\x00\x34\x13\x01\x08\x68',
    "src_HDMI1":       b'\x06\x14\x00\x04\x00\x34\x13\x01\x03\x63',
    "src_HDMI2":       b'\x06\x14\x00\x04\x00\x34\x13\x01\x07\x67',
    "src_HDMI3":       b'\x06\x14\x00\x04\x00\x34\x13\x01\x09\x69',
    "src_HDMI4/MHL":   b'\x06\x14\x00\x04\x00\x34\x13\x01\x0e\x6e',
    "src_Composite":   b'\x06\x14\x00\x04\x00\x34\x13\x01\x05\x65',
    "src_S-Video":     b'\x06\x14\x00\x04\x00\x34\x13\x01\x06\x66',
    "src_DVI":         b'\x06\x14\x00\x04\x00\x34\x13\x01\x0A\x6A',
    "src_Component":   b'\x06\x14\x00\x04\x00\x34\x13\x01\x0B\x6B',
    "src_HDbaseT":     b'\x06\x14\x00\x04\x00\x34\x13\x01\x0C\x6C',
    "src_USB-C":       b'\x06\x14\x00\x04\x00\x34\x13\x01\x0F\x6F',
    "src_USB1":        b'\x06\x14\x00\x04\x00\x34\x13\x01\x1A\x7A',
    "src_USB2":        b'\x06\x14\x00\x04\x00\x34\x13\x01\x1C\x7C',
    "src_USBDisplay":  b'\x06\x14\x00\x04\x00\x34\x13\x01\x1E\x7E',
    "src_LAN/WiFi":    b'\x06\x14\x00\x04\x00\x34\x13\x01\x1B\x7B',
    "src_SmartSystem": b'\x06\x14\x00\x04\x00\x34\x13\x01\x10\x70',
    "src?":            b'\x07\x14\x00\x05\x00\x34\x00\x00\x13\x01\x61'
}

STATUS_LIST = {
    b'\x03\x14\x00\x00\x00\x14':             'cmd_ack',
    b'\x00\x14\x00\x00\x00\x14':             'cmd_unavailable',
    b'\x05\x14\x00\x03\x00\x00\x00\x00\x17': 'off',
    b'\x05\x14\x00\x03\x00\x00\x00\x01\x18': 'on',
    b'\x05\x14\x00\x03\x00\x00\x00\x02\x19': 'pwr_warming',
    b'\x05\x14\x00\x03\x00\x00\x00\x03\x1A': 'pwr_cooling',
# Most other status are read here   ^^
}

SOURCE_STATES = { 
    0:  'VGA1',
    3:  'HDMI1', 
    5:  'Composite',
    6:  'S-Video',
    7:  'HDMI2', 
    8:  'VGA2',
    9:  'HDMI3',
    10: 'DVI',
    11: 'Component',
    12: 'HDbaseT',
    14: 'HDMI4/MHL',
    15: 'USB-C',
    16: 'SmartSystem',
    26: 'USB1',
    27: 'LAN/WiFi',
    28: 'USBDisplay',
    30: 'USB2',
}
