"""Data update coordinator for TeamSpeak integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigEntryAuthFailed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import CannotConnect, InvalidAuth, TeamSpeakWebQueryClient

_LOGGER = logging.getLogger(__name__)


class TeamSpeakDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching TeamSpeak data."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: TeamSpeakWebQueryClient,
        config_entry: ConfigEntry,
        update_interval: int,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="TeamSpeak Server Info",
            update_interval=timedelta(seconds=update_interval),
            config_entry=config_entry,
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from TeamSpeak server."""
        try:
            # TeamSpeak WebQuery requires sequential requests using the same session
            # The server crashes if we create new sessions or close connections
            server_info = await self.client.get_server_info()
            client_list = await self.client.get_client_list()
            channel_list = await self.client.get_channel_list()
        except InvalidAuth as err:
            raise ConfigEntryAuthFailed("Invalid API key") from err
        except CannotConnect as err:
            raise UpdateFailed(f"Failed to connect to TeamSpeak server: {err}") from err
        else:
            return {
                "server_info": server_info,
                "client_list": client_list,
                "channel_list": channel_list,
            }
