from __future__ import annotations

from unittest import mock

import aiohttp
import pytest

import plugbear


class TestPlugBear:
    @mock.patch("aiohttp.ClientSession", spec=aiohttp.ClientSession)
    async def test_init(self, mock_client_session) -> None:
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session
        mock_request = mock.AsyncMock(spec=aiohttp.client._RequestContextManager)
        mock_session.get.return_value = mock_request
        mock_request.__aenter__.return_value = mock.NonCallableMock(spec=aiohttp.client.ClientResponse, status=200)

        api_key = "some-api-key"
        await plugbear.PlugBear.init(api_key=api_key)
        mock_session.get.assert_called_once_with("https://plugbear.io/api/sdk/verify")

    @mock.patch("aiohttp.ClientSession", spec=aiohttp.ClientSession)
    async def test_init_fail_on_401(self, mock_client_session) -> None:
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session
        mock_request = mock.AsyncMock(spec=aiohttp.client._RequestContextManager)
        mock_session.get.return_value = mock_request
        mock_request.__aenter__.return_value = mock.NonCallableMock(spec=aiohttp.client.ClientResponse, status=401)

        api_key = "some-api-key"
        with pytest.raises(plugbear.UnauthorizedOrganization):
            await plugbear.PlugBear.init(api_key=api_key)
        mock_session.get.assert_called_once_with("https://plugbear.io/api/sdk/verify")
