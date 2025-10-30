"""TeamSpeak WebQuery API Client."""

from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError, ClientSession

from homeassistant.exceptions import HomeAssistantError


class TeamSpeakWebQueryClient:
    """Client for TeamSpeak WebQuery API."""

    def __init__(
        self,
        host: str,
        port: int,
        server_id: int,
        api_key: str,
        session: ClientSession,
    ) -> None:
        """Initialize the TeamSpeak WebQuery client."""
        self.host = host
        self.port = port
        self.server_id = server_id
        self.api_key = api_key
        self.session = session
        self.base_url = f"http://{host}:{port}/{server_id}"

    async def _request(self, endpoint: str) -> dict[str, Any]:
        """Make a request to the TeamSpeak WebQuery API."""
        url = f"{self.base_url}/{endpoint}"
        params = {"api-key": self.api_key}

        try:
            async with asyncio.timeout(10):
                # TeamSpeak WebQuery requires using the same session for all requests
                # Creating new sessions or closing connections crashes the server
                response = await self.session.post(url, params=params)
                response.raise_for_status()
                data = await response.json()
        except TimeoutError as err:
            raise CannotConnect("Timeout connecting to TeamSpeak server") from err
        except ClientError as err:
            raise CannotConnect(f"Error connecting to TeamSpeak server: {err}") from err
        except Exception as err:
            raise CannotConnect(f"Unexpected error: {err}") from err

        # Check API response status
        status = data.get("status", {})
        if status.get("code", 0) != 0:
            error_msg = status.get("message", "Unknown error")
            # Common error codes
            if status.get("code") == 3329:  # Invalid API key
                raise InvalidAuth(f"Invalid API key: {error_msg}")
            raise CannotConnect(f"API error: {error_msg}")

        return data

    async def test_connection(self) -> dict[str, Any]:
        """Test the connection and return server info."""
        data = await self._request("serverinfo")
        body = data.get("body", [])
        if not body:
            raise CannotConnect("Empty response from server")
        return body[0]

    async def get_server_info(self) -> dict[str, Any]:
        """Get server information."""
        data = await self._request("serverinfo")
        body = data.get("body", [])
        if not body:
            raise CannotConnect("Empty server info response")
        return body[0]

    async def get_client_list(self) -> list[dict[str, Any]]:
        """Get list of connected clients."""
        data = await self._request("clientlist")
        return data.get("body", [])

    async def get_channel_list(self) -> list[dict[str, Any]]:
        """Get list of channels."""
        data = await self._request("channellist")
        return data.get("body", [])


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
