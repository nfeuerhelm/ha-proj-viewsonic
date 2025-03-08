# Home Assistant Custom Integration - ViewSonic Projector

![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square) 
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/nfeuerhelm/ha-proj-viewsonic)
![GitHub License](https://img.shields.io/github/license/nfeuerhelm/ha-proj-viewsonic)

![GitHub Release](https://img.shields.io/github/v/release/nfeuerhelm/ha-proj-viewsonic?sort=semver&display_name=tag)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nfeuerhelm/ha-proj-viewsonic/hacs.yaml?branch=main&label=HACS%20Validate)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nfeuerhelm/ha-proj-viewsonic/hassfest.yaml?branch=main&label=hassfest%20Validate)


## Overview
This is a custom integration for Home Assistant that adds support for control of networked ViewSonic Projectors using RS-232/LAN Control Protocol Specification V1.5. It allows you to control your network connected ViewSonic project - powering it on/off, changing source, and adjusting volume. This integration provides a Home Assistant `media_player` device and entity.

## Prerequisits
- A working version of [Home Assistant](https://www.home-assistant.io/)
- A supported ViewSonic Projector
    - One of: ls510w, ls510wh, ls560w, ls560wh, ls610hdh, ls610wh, ls832wu, pa504w, pa700s, pa700w, pa700x, ps502w, ps502x, px701-4ke, px704hd, px728-4k, px748-4k, px749-4k
    - Use 'unknown' for other ViewSonic projectors supporting the RS-232/LAN Control Protocol Specification V1.5
    - Projectors supporting older versions of the RS-232/LAN Control Protocol Specification may work using 'unknown' but your milage may vary
    - **Pro9 series projectors are not supported**
    - _Let me know with [an issue](https://github.com/nfeuerhelm/ha-proj-viewsonic/issues/new) if you confirm this works with your projector model_
- A working network connection between Home Assistant and your supported projector

_Note: For full functionality, make sure to enable `Standby LAN Control` found in `ADVANCED` → `LAN Control Settings` or similar menu location._

## Home Assistant Device Features
- `media_player` entity
  - Actions: 
    - power control (`media_player.turn_on`, `media_player.turn_off`)
    - volume control (`media_player.volume_set`, `media_player.volume_up`, `media_player.volume_down`)
    - mute control (`media_player.volume_mute`)
    - source set (`media_player.select_source`)
  - State: power status
  - Attribures:
    - volume level (`volume_level`)
    - mute state (`is_volume_muted`)
    - source selection (`source`)
    - source list (`source_list`)
- `binary_sensor` entity
  - State: connection status

## Installation
### Manual Installation
1. Download the latest release from the [Releases](https://github.com/nfeuerhelm/ha-proj-viewsonic/releases) page.
2. Extract the contents and copy the `viewsonic_projector` directory into the `/config/custom_components/` directory on your Home Assistant instance.
3. Restart Home Assistant.

### HACS Installation
1. Add this repository as a custom repository in HACS. \
  [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=nfeuerhelm&repository=ha-proj-viewsonic&category=integration)
2. Search for "ViewSonic Projector" and install it.
3. Restart Home Assistant.

## Configuration
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=viewsonic_projector)
1. Go to `Settings` → `Devices & Services` → `Add Integration`.
2. Search for "ViewSonic Projector" and select it. 
3. Follow the on-screen instructions to set up the integration.

Alternatively, you can configure it manually in `configuration.yaml`:
```yaml
viewsonic_projector:
  - host: "192.168.x.x"
    name: "My Projector" # Optional; default: "Viewsonic Projector"
    model: "px749-4k" # Optional; default: "Unknown"
    reduce_traffic: False # Optional; default: False
```

_Note: You need to restart Home Assistant Core after changing the reduce traffice setting for it to take effect._

## Contributing
Contributions are welcome! Please submit issues and pull requests via [GitHub](https://github.com/nfeuerhelm/ha-proj-viewsonic).

## License
This project is licensed under the [MIT License](LICENSE).

## Credits
Developed by [@nfeuerhelm](https://github.com/nfeuerhelm) based on [ViewSonic Standards](./RS-232%20LAN%20Control%20Protocol%20Specification%20V1.5.pdf).

## Trademark Legal Notices
All product names, trademarks and registered trademarks in this repository, are property of their respective owners. All product information in this repository is used by the project for identification purposes only.

The use of these names, trademarks and brands appearing in this repository, do not imply endorsement.
