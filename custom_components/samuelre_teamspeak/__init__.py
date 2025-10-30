"""The TeamSpeak Server Info integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CannotConnect, TeamSpeakWebQueryClient
from .const import CONF_API_KEY, CONF_SERVER_ID
from .coordinator import TeamSpeakDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

type TeamSpeakConfigEntry = ConfigEntry[TeamSpeakDataUpdateCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: TeamSpeakConfigEntry) -> bool:
    """Set up TeamSpeak Server Info from a config entry."""
    # Create API client
    session = async_get_clientsession(hass)
    client = TeamSpeakWebQueryClient(
        host=entry.data[CONF_HOST],
        port=entry.data[CONF_PORT],
        server_id=entry.data[CONF_SERVER_ID],
        api_key=entry.data[CONF_API_KEY],
        session=session,
    )

    # Test connection before setting up
    try:
        await client.test_connection()
    except CannotConnect as err:
        raise ConfigEntryNotReady(
            f"Unable to connect to TeamSpeak server: {err}"
        ) from err

    # Create coordinator
    coordinator = TeamSpeakDataUpdateCoordinator(
        hass=hass,
        client=client,
        config_entry=entry,
        update_interval=entry.data[CONF_SCAN_INTERVAL],
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator in runtime data
    entry.runtime_data = coordinator

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: TeamSpeakConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
