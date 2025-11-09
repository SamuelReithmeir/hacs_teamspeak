# TeamSpeak Server Info Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

Monitor your TeamSpeak server directly from Home Assistant! This integration provides real-time information about your TeamSpeak server using the WebQuery API.

## Features

- 🎯 **7 Sensor Entities** tracking key server metrics
- 👥 **Client Monitoring** with detailed client list attributes
- 📊 **Bandwidth Tracking** for sent and received data
- ⏱️ **Server Uptime** monitoring
- 🔄 **Configurable Update Interval**
- 🎨 **Device-based Organization** - all sensors grouped under one device per virtual server

## Sensors

| Sensor                 | Description                      | Device Class | Attributes                           |
| ---------------------- | -------------------------------- | ------------ | ------------------------------------ |
| **Clients Online**     | Number of connected clients      | -            | Client list, Query clients count     |
| **Channels**           | Number of channels on the server | -            | Full channel list                    |
| **Uptime**             | Server uptime in seconds         | Duration     | -                                    |
| **Max Clients**        | Maximum allowed clients          | -            | -                                    |
| **Bandwidth Received** | Incoming bandwidth (bytes/sec)   | Data Rate    | Total bytes, Last minute average     |
| **Bandwidth Sent**     | Outgoing bandwidth (bytes/sec)   | Data Rate    | Total bytes, Last minute average     |
| **Server Status**      | Current server status            | -            | Server name, version, platform, port |

## Prerequisites

### TeamSpeak Server Requirements

1. **WebQuery API enabled** on your server
2. **API Key** for authentication

## Installation

### HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. Add this repository as a custom repository in HACS:
   - Click on HACS in the sidebar
   - Click on "Integrations"
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add `https://github.com/SamuelReithmeir/teamspeak_status_sensors` as repository
   - Select "Integration" as category
   - Click "Add"
3. Click "Install" on the TeamSpeak Server Info card
4. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page][releases]
2. Extract the `custom_components/samuelre_teamspeak` folder
3. Copy it to your Home Assistant's `custom_components` directory
4. Restart Home Assistant

## Configuration

### Via Home Assistant UI (Recommended)

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **TeamSpeak Server Info**
4. Enter your configuration:
   - **Host**: IP address or hostname of your TeamSpeak server
   - **WebQuery Port**: Port where WebQuery is running (default: 10080)
   - **Virtual Server ID**: The ID of your virtual server (usually 1)
   - **API Key**: Your WebQuery API key
   - **Scan Interval**: How often to update (in seconds, default: 60)

## Usage Examples

### Automation: Notify When Server is Full

```yaml
automation:
  - alias: "TeamSpeak Server Full Alert"
    trigger:
      - platform: template
        value_template: "{{ states('sensor.teamspeak_server_clients_online') | int >= states('sensor.teamspeak_server_max_clients') | int }}"
    action:
      - service: notify.mobile_app
        data:
          message: "TeamSpeak server is full!"
```

### Template: Display Active Clients

```yaml
sensor:
  - platform: template
    sensors:
      ts_active_users:
        friendly_name: "Active TeamSpeak Users"
        value_template: >
          {% set clients = state_attr('sensor.teamspeak_server_clients_online', 'client_list') %}
          {{ clients | map(attribute='client_nickname') | join(', ') if clients else 'None' }}
```


## Troubleshooting

### Connection Errors

1. **Verify WebQuery is enabled**: Check your TeamSpeak server configuration
2. **Test API access**: Use curl to test the API:
   ```bash
   curl -X POST http://YOUR_SERVER_IP:10080/1/serverinfo \
     -H "x-api-key: YOUR_API_KEY"
   ```
3. **Check firewall**: Ensure port 10080 (or your custom port) is accessible
4. **Verify credentials**: Make sure the API key is correct and has proper permissions

### Integration Not Showing Up

1. Clear browser cache
2. Restart Home Assistant
3. Check `home-assistant.log` for errors related to `samuelre_teamspeak`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

- 🐛 [Report a bug][issues]
- 💡 [Request a feature][issues]
- 💬 [Ask a question][issues]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Developed by [@SamuelReithmeir](https://github.com/SamuelReithmeir)

## Disclaimer

This integration is not officially affiliated with or endorsed by TeamSpeak Systems GmbH.

---

**If you like this integration, please give it a ⭐ on GitHub!**

[releases-shield]: https://img.shields.io/github/release/SamuelReithmeir/teamspeak_status_sensors.svg
[releases]: https://github.com/SamuelReithmeir/teamspeak_status_sensors/releases
[license-shield]: https://img.shields.io/github/license/SamuelReithmeir/teamspeak_status_sensors.svg
[issues]: https://github.com/SamuelReithmeir/teamspeak_status_sensors/issues
