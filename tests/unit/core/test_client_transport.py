"""
Guard the transport used by vietstock.core.utils.client.

Cloudflare refuses some sources with a 403 based on the TLS/HTTP2 fingerprint, so
adding a Chrome User-Agent is not enough. Every request must go out through the
Chrome-impersonating curl_cffi session instead of plain requests.
"""

from __future__ import annotations

import json

import pytest
from curl_cffi import requests as curl_requests

from vietstock.core.utils import client
from vietstock.core.utils.client import send_request, send_request_text


@pytest.mark.unit
@pytest.mark.core
class TestClientTransport:
    """Requests are sent by the session that impersonates Chrome."""

    def test_session_impersonates_chrome(self):
        assert isinstance(client._SESSION, curl_requests.Session)
        assert client._SESSION.impersonate == "chrome"

    def test_get_and_post_go_through_the_session(self, monkeypatch, mock_response_factory):
        seen = []

        def _spy(url, **kwargs):
            seen.append((url, kwargs))
            return mock_response_factory(json_data={"ok": True})

        monkeypatch.setattr(client._SESSION, "get", _spy)
        monkeypatch.setattr(client._SESSION, "post", _spy)

        assert send_request("https://example.com/api", headers={}, params={"a": 1}) == {"ok": True}
        send_request("https://example.com/api", headers={}, method="POST", payload={"a": 1})

        assert seen[0][0] == "https://example.com/api"
        assert seen[0][1]["params"] == {"a": 1}
        assert json.loads(seen[1][1]["data"]) == {"a": 1}

    def test_text_response_goes_through_the_session(self, monkeypatch, mock_response_factory):
        monkeypatch.setattr(
            client._SESSION,
            "get",
            lambda url, **kwargs: mock_response_factory(text="<html>ok</html>"),
        )

        assert send_request_text("https://example.com/page", headers={}) == "<html>ok</html>"

    @pytest.mark.parametrize(
        "error",
        [
            curl_requests.errors.RequestsError("connection refused"),
            curl_requests.errors.CurlError("raw curl failure"),
        ],
    )
    def test_transport_error_becomes_connection_error(self, monkeypatch, error):
        def _fail(*args, **kwargs):
            raise error

        monkeypatch.setattr(client._SESSION, "get", _fail)

        with pytest.raises(ConnectionError):
            send_request("https://example.com/api", headers={})
