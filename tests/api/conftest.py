from __future__ import annotations

from unittest import mock

import aiohttp
import pytest


@pytest.fixture(scope="function", autouse=True)
def disable_org_verification() -> None:
    with mock.patch("aiohttp.ClientSession", spec=aiohttp.ClientSession) as mock_client_session:
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session
        mock_request = mock.AsyncMock(spec=aiohttp.client._RequestContextManager)
        mock_session.get.return_value = mock_request
        mock_request.__aenter__.return_value = mock.NonCallableMock(spec=aiohttp.client.ClientResponse, status=200)

        yield
